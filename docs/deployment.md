# Deployment

## Ringkasan

| | |
|---|---|
| Pemicu | Push ke `main`, atau tombol **Run workflow** di tab Actions (`workflow_dispatch`) |
| Workflow | `.github/workflows/deploy.yml` |
| Langkah | `npm ci` → `npm run validate` (Prettier, ESLint, Stylelint, `astro check`; gagal = tidak deploy) → `npm run build` → `rsync` isi `dist/` ke server lewat SSH |
| Tujuan | `prasetya@server.griv.co.id:public_html/prasetyawebworks.web.id/` |
| Durasi | sekitar 1 menit |
| Concurrency | Grup `deploy-cpanel`. Deploy berjalan satu per satu, tidak dibatalkan |

`rsync --delete` membuat folder di server **sama persis** dengan `dist/`. File yang dihapus dari project juga terhapus di server. Folder lain di `public_html/` (misalnya site preview) tidak tersentuh, karena target rsync hanya subfolder website.

Deploy memakai SSH karena hosting tidak menyediakan FTP. Lihat [ADR 0002](decisions/0002-deploy-ssh-rsync.md).

## Secret GitHub

Repo → **Settings → Secrets and variables → Actions → Repository secrets**.

| Nama | Isi |
|---|---|
| `SSH_PRIVATE_KEY` | Isi lengkap private key deploy (`-----BEGIN OPENSSH PRIVATE KEY-----` … `-----END …-----`) |

Host key server **dipatok di workflow** (`known_hosts` berisi kunci `ssh-ed25519` milik `server.griv.co.id`), jadi koneksi ke server palsu akan ditolak. Kalau hosting mengganti kunci server, perbarui baris itu:

```sh
ssh-keyscan -t ed25519 server.griv.co.id
```

Workflow memberi pesan error yang jelas untuk dua kasus umum: secret kosong, dan isi secret bukan private key yang valid.

### Membuat atau mengganti deploy key

1. Di komputer lokal:
   ```sh
   ssh-keygen -t ed25519 -N "" -C "github-actions-deploy" -f ~/.ssh/griv_deploy_ed25519
   ```
2. cPanel → **SSH Access → Manage SSH Keys → Import Key**. Isi nama dan paste **public key** (`.pub`) saja, lalu **Authorize**.
3. GitHub secret `SSH_PRIVATE_KEY` diisi dengan isi file **tanpa** `.pub`.
4. Uji dari lokal:
   ```sh
   ssh -i ~/.ssh/griv_deploy_ed25519 prasetya@server.griv.co.id 'echo ok'
   ```
5. Hapus atau *deauthorize* key lama di cPanel.

## Struktur server

```
/home/prasetya/public_html/
├── .htaccess                          ← pengarah domain utama (lihat di bawah)
├── prasetyawebworks.web.id/           ← website Astro, diisi oleh CI
└── preview.prasetyawebworks.web.id/   ← WordPress Multisite (document root subdomain preview)
```

Hosting mengunci document root domain utama di `public_html/` dan mewajibkan semua document root berada di dalamnya. Supaya setiap website punya folder sendiri, domain utama dilayani dari subfolder lewat `.htaccess` pengarah. Lihat [ADR 0003](decisions/0003-subfolder-router.md).

### `.htaccess` pengarah (`public_html/.htaccess`)

File ini **tidak ikut di-deploy CI** dan dipasang manual lewat cPanel File Manager. Isi lengkapnya ada di bagian [Isi `.htaccess` pengarah](#isi-htaccess-pengarah) di bawah. Itu satu-satunya salinan di luar server, jadi gunakan untuk memulihkan file kalau terhapus atau rusak. Fungsinya:

1. `/.well-known/` dilewatkan, supaya validasi SSL (AutoSSL / Let's Encrypt) tetap berjalan.
2. Akses langsung ke `/prasetyawebworks.web.id/…` dibalas **404**, supaya nama subfolder tidak terlihat.
3. Path folder tanpa garis miring diarahkan dengan menambah `/` (contoh `/en` → `/en/`), supaya redirect bawaan Apache tidak membocorkan path subfolder.
4. Semua request untuk `prasetyawebworks.web.id` dan `www.` diarahkan ke subfolder.
5. `RedirectMatch 404` untuk `/preview.prasetyawebworks.web.id`. Dipakai `mod_alias`, karena aturan rewrite WordPress di subfolder itu menimpa aturan rewrite dari induk.

File di server juga berisi blok `cPanel-generated` (PHP handler). **Jangan dihapus.** Aturan pengarah ditaruh di bawah blok itu.

Kalau menambah addon domain atau subdomain baru yang punya aturan rewrite sendiri (misalnya WordPress), tambahkan:

```apache
RedirectMatch 404 ^/<nama-folder>(/|$)
```

Perbarui juga isi di bagian [Isi `.htaccess` pengarah](#isi-htaccess-pengarah) supaya dokumen ini tetap sama dengan server.

### Isi `.htaccess` pengarah

Tempel di **bawah** blok `cPanel-generated` yang sudah ada di `public_html/.htaccess`:

```apache
# Router for public_html/ — NOT deployed by CI.
# Upload this file manually to public_html/.htaccess via cPanel File Manager.
#
# The host locks the main domain's document root to public_html/, so requests
# for the main domain are internally rewritten into its own subfolder:
#   public_html/prasetyawebworks.web.id/          <- Astro site (CI deploy target)
#   public_html/preview.prasetyawebworks.web.id/  <- WordPress multisite (own docroot)

# Keep the preview site reachable only through its own subdomain. Uses mod_alias
# because WordPress' own rewrite rules in that folder override ours.
RedirectMatch 404 ^/preview\.prasetyawebworks\.web\.id(/|$)

RewriteEngine On

# AutoSSL / ACME domain validation files live in public_html/.well-known/.
RewriteRule ^\.well-known/ - [L]

# Hide the subfolder name: direct requests to /prasetyawebworks.web.id/... return 404.
RewriteCond %{HTTP_HOST} ^(www\.)?prasetyawebworks\.web\.id$ [NC]
RewriteCond %{THE_REQUEST} \s/prasetyawebworks\.web\.id[/?\s] [NC]
RewriteRule ^ - [R=404,L]

# Add the trailing slash ourselves for directories (e.g. /en -> /en/), otherwise
# Apache's DirectorySlash redirect would leak the subfolder path into the URL.
RewriteCond %{HTTP_HOST} ^(www\.)?prasetyawebworks\.web\.id$ [NC]
RewriteCond %{REQUEST_URI} !^/prasetyawebworks\.web\.id/
RewriteCond %{DOCUMENT_ROOT}/prasetyawebworks.web.id/$1 -d
RewriteRule ^(.+[^/])$ /$1/ [R=301,L]

# Serve the main domain from its subfolder.
RewriteCond %{HTTP_HOST} ^(www\.)?prasetyawebworks\.web\.id$ [NC]
RewriteCond %{REQUEST_URI} !^/prasetyawebworks\.web\.id/
RewriteRule ^(.*)$ /prasetyawebworks.web.id/$1 [L]
```

## Domain, DNS, dan SSL

| | |
|---|---|
| Domain | `prasetyawebworks.web.id`, dibeli di IDwebhost (registrar: PT JC Indonesia / ResellerCamp) |
| Nameserver | `ns1.griv.co.id`, `ns2.griv.co.id` (diatur di panel IDwebhost) |
| DNS zone | Dikelola otomatis oleh cPanel GRIV |
| SSL | AutoSSL (Let's Encrypt), terbit dan diperpanjang otomatis |
| HTTPS | **Force HTTPS Redirect** aktif di cPanel → Domains |

Subdomain baru cukup dibuat di cPanel → Domains. DNS dan SSL-nya otomatis.

## Rollback

Website statis, jadi rollback cukup dengan men-deploy versi lama:

```sh
git revert <commit-yang-bermasalah>
git push origin main
```

Atau, untuk keadaan darurat: tab **Actions** → buka run deploy dari commit yang masih bagus → **Re-run all jobs**.

## Verifikasi setelah deploy

```sh
curl -s -o /dev/null -w '%{http_code}\n' https://prasetyawebworks.web.id/
curl -s -o /dev/null -w '%{http_code}\n' https://prasetyawebworks.web.id/templates/
```

Cek juga tampilan di HP. Browser menyimpan cache CSS dan favicon, jadi gunakan tab incognito.

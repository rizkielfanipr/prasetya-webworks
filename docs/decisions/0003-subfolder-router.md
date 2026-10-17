# 0003. Domain utama dilayani dari subfolder lewat `.htaccess` pengarah

- **Status:** Accepted
- **Tanggal:** 2026-10-16

## Konteks
cPanel mengunci document root domain utama di `public_html/`, dan mewajibkan document root subdomain atau addon domain berada **di dalam** `public_html/`. Kalau website Astro ditaruh langsung di `public_html/`, file-filenya bercampur dengan folder subdomain (`preview…`), dan folder subdomain itu bisa diakses lewat domain utama.

## Keputusan
Website utama berada di `public_html/prasetyawebworks.web.id/`. File `public_html/.htaccess` mengarahkan request domain utama ke subfolder itu, dan:
- mengecualikan `/.well-known/` untuk validasi SSL;
- membalas 404 untuk akses langsung ke nama subfolder;
- menambahkan garis miring akhir sendiri, supaya redirect bawaan Apache tidak membocorkan path subfolder;
- memblokir folder subdomain dari domain utama dengan `RedirectMatch 404` (`mod_alias`), karena rewrite WordPress di subfolder menimpa rewrite dari induk.

Isi file ada di [deployment.md](../deployment.md#isi-htaccess-pengarah) dan dipasang manual.

## Konsekuensi
- ✅ Setiap website punya folder sendiri, rapi dan mudah di-backup.
- ✅ Folder subdomain tidak bisa diakses lewat domain utama.
- ⚠️ File pengarah tidak dikelola CI. Kalau hilang atau salah, domain utama tidak bisa dibuka. Selalu samakan isinya dengan salinan di dokumentasi.
- ⚠️ Setiap subdomain atau addon domain baru yang punya rewrite sendiri butuh satu baris `RedirectMatch 404`.

# WordPress Preview (Live Preview Template)

Demo setiap template berjalan di **WordPress Multisite** pada `https://preview.prasetyawebworks.web.id`. Setiap template punya satu site dengan alamat `/template-<kode>/`, misalnya `/template-0001/`. Alasan pemilihan arsitektur ini ada di [ADR 0004](decisions/0004-wordpress-multisite-previews.md).

## Konfigurasi saat ini

| | |
|---|---|
| Lokasi file | `public_html/preview.prasetyawebworks.web.id/` |
| WordPress | 7.1.x, Multisite mode **subdirectory** (`SUBDOMAIN_INSTALL = false`) |
| Database | `prasetya_wpprev`, prefix tabel `pw7_` |
| PHP | **8.3** (cPanel → MultiPHP Manager, khusus domain preview). Plugin Template Kit Import butuh PHP 8.3 |
| Batas PHP | `upload_max_filesize 32M`, `post_max_size 64M`, `memory_limit 256M`, `max_execution_time 300` (cPanel → MultiPHP INI Editor) |
| Pengaturan Jaringan | Max upload file size 32768 KB, `zip` termasuk jenis berkas yang diizinkan, pendaftaran dinonaktifkan |
| Tema | **Hello Elementor**, aktif untuk jaringan |
| Plugin aktif jaringan | Elementor, Template Kit – Import (Envato) |
| Plugin terpasang (aktifkan per site sesuai kebutuhan kit) | Ultimate Addons for Elementor (UAE, dulu "Elementor Header & Footer Builder"), MetForm, ElementsKit Lite |
| Noindex | mu-plugin `network-noindex.php` di `wp-content/mu-plugins/` membuat semua site `noindex, nofollow` (isinya ada di bagian [mu-plugin noindex](#mu-plugin-noindex)) |
| Akses dari domain utama | Diblokir (404) oleh `.htaccess` pengarah. Lihat [deployment.md](deployment.md) |

`.htaccess` di folder preview berisi blok `cPanel-generated` (handler PHP dan nilai INI) **dan** aturan rewrite Multisite di antara `# BEGIN WordPress` dan `# END WordPress`. Kalau mengedit, jangan menghapus blok cPanel.

## Membuat satu live preview

Pakai file Excel acuan (`acuan-live-preview-template.xlsx`) untuk melihat nama file kit, daftar halaman, dan plugin yang dibutuhkan setiap kode.

### 1. Buat site
**Admin Jaringan → Situs → Tambah Situs Baru**
- Alamat situs: `template-<kode>` (contoh `template-0002`)
- Judul: nama template (contoh `Aleos`)

Lalu masuk ke dasbor site itu: **Situs Saya → template-XXXX → Dasbor**.

### 2. Tema dan plugin (di dalam site)
- **Tampilan → Tema:** aktifkan **Hello Elementor**. Site baru otomatis memakai tema blok bawaan, dan selama tema itu aktif, menu *Tampilan → Menu* tidak muncul.
- **Plugin:** aktifkan plugin yang tercantum di kolom *Plugin Dibutuhkan* di Excel, misalnya UAE dan MetForm. Plugin yang tidak dibutuhkan biarkan nonaktif.

### 3. Import kit
**Perkakas → Template Kit**, lalu upload ZIP kit dari folder `TEMPLATE FREE`.
- Klik **Import Template** pada **Global Kit Styles**. Langkah ini wajib, karena berisi warna dan font. Sebaiknya di-import paling awal.
- Import semua template lainnya (Header, Footer, Home, About, …). Template **404** boleh dilewati, karena memasangnya butuh Elementor Pro.
- Import hanya menyimpan desain ke library Elementor. Halamannya belum dibuat.

### 4. Buat halaman
Untuk setiap halaman (Home, About, Services, …):
1. **Laman → Tambah Baru**, isi judul, lalu **Edit with Elementor**.
2. Klik **ikon folder** → tab **My Templates** → **Insert** template yang sesuai. Pilih *Yes* kalau ditanya *apply settings*.
3. Klik ikon **Pengaturan Halaman** (ikon dokumen dengan roda gigi, di kiri atas editor):
   - **Hide Title:** aktif;
   - **Page Layout:** *Elementor Full Width*, jangan *Canvas*, karena header dan footer akan hilang.
4. **Terbitkan**.

### 5. Halaman depan
**Pengaturan → Membaca → Laman statis → Beranda: Home → Simpan.**
Setelah ini, `/template-XXXX/` langsung menampilkan Home, dan `/home/` dialihkan otomatis.

### 6. Menu
**Tampilan → Menu**
1. Buat menu `Main Menu` dan centang **Otomatis tambahkan laman**.
2. Tambahkan halaman-halaman lalu urutkan. Seret item ke kanan untuk membuat submenu.
3. **Simpan Menu**.

### 7. Header dan Footer
**UAE → Header & Footer → Tambah Baru**
1. Judul `Header`, **Jenis Template:** Header, **Tampilkan Di:** Seluruh Situs Web → Terbitkan → **Sunting dengan Elementor**.
2. Ikon folder → My Templates → Insert **Header**.
3. Klik widget menu navigasi, lalu pilih **Main Menu**.
4. Ganti gambar logo placeholder dan atur lebarnya → **Terbitkan**.
5. Ulangi untuk **Footer**.

### 8. Rapikan konten
Kit Envato memakai **gambar placeholder** (kotak abu-abu bergambar gunung). Ganti dengan foto berlisensi (Unsplash atau Pexels) supaya demo terlihat menarik.

### 9. Tayangkan di website
1. Buka `https://preview.prasetyawebworks.web.id/template-XXXX/` dan cek tampilan di desktop dan HP.
2. Tambahkan kodenya ke `src/data/live-previews.json` di repo, lalu push. Lihat [development.md](development.md).
3. Ubah status di Excel menjadi **Live** dan isi tanggalnya.

## Perawatan

- Update WordPress, tema, dan plugin secara rutin dari Admin Jaringan. Semua site ada di akun cPanel yang sama dengan website utama, jadi satu plugin yang rentan bisa berdampak ke semuanya.
- Pakai plugin sesedikit mungkin, dan hanya dari wordpress.org.
- **Jangan** memasang plugin atau tema bajakan (*nulled*).

## mu-plugin noindex

Simpan sebagai `public_html/preview.prasetyawebworks.web.id/wp-content/mu-plugins/network-noindex.php`. Plugin di folder `mu-plugins` langsung aktif di semua site, tanpa perlu diaktifkan.

```php
<?php
/**
 * Plugin Name: Network Noindex
 * Description: Keeps every site in the preview network out of search engines, including sites created later.
 *
 * Upload manually to public_html/preview.prasetyawebworks.web.id/wp-content/mu-plugins/
 */

defined( 'ABSPATH' ) || exit;

// Same effect as ticking "Discourage search engines" on every site:
// adds <meta name="robots" content="noindex, nofollow"> to every page.
add_filter( 'pre_option_blog_public', '__return_zero' );
```

## Opsional: tema default untuk site baru

Supaya site baru langsung memakai Hello Elementor, tambahkan ke `wp-config.php` (di atas baris *That's all, stop editing!*):

```php
define( 'WP_DEFAULT_THEME', 'hello-elementor' );
```

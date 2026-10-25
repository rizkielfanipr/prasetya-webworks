# Katalog Template

Katalog berisi **218 template Elementor** yang bisa dipakai **tanpa Elementor Pro**, dikelompokkan dalam 7 kategori. Website hanya menampilkan data dan thumbnail. File kit-nya disimpan di luar repo.

## Model data

`src/data/templates.json`, satu objek per template:

```json
{ "code": "0001", "name": "Agenci", "type": "Digital Marketing Agency", "category": "business-technology", "pages": 7, "thumbnail": true, "kit": "0001-agenci.zip" }
```

| Field | Arti |
|---|---|
| `code` | Kode 4 digit, **tetap dan unik**. Dipakai di kartu (`#0001`), pesan konsultasi, alamat site preview (`template-0001`), nama file kit, dan nama thumbnail |
| `name` | Nama template (dari judul kit) |
| `type` | Jenis bisnis (dari judul kit, berbahasa Inggris) |
| `category` | Slug kategori (lihat tabel di bawah) |
| `pages` | Jumlah halaman di kit |
| `thumbnail` | `true` kalau `public/images/templates/<code>.webp` ada |
| `kit` | Nama file ZIP kit di folder kit (lihat di bawah) |

`src/data/live-previews.json` berisi daftar kode yang sudah punya demo WordPress.

> **Jangan mengganti `code` template yang sudah ada.** Kode itu dipakai di URL demo, pesan klien, dan file kit.

## Kategori

| Slug (URL) | Label ID | Label EN | Isi asal (folder kit) |
|---|---|---|---|
| `business-technology` | Bisnis & Teknologi | Business & Technology | Business & Service, Finance & Law, Insurance, Industries, Tech & Apps, Farm & Agriculture |
| `creative-portfolio` | Kreatif & Portofolio | Creative & Portfolio | Creative & Design, Photography, Personal CV, Blog & Podcast |
| `food-lifestyle` | Kuliner & Gaya Hidup | Food & Lifestyle | Food & Drink, Fashion & Beauty, Shopping & E-commerce |
| `health-sports` | Kesehatan & Olahraga | Health & Sports | Health & Medical, Sport & Fitness |
| `property-construction` | Properti & Konstruksi | Property & Construction | Real Estate & Construction |
| `travel-events` | Travel & Acara | Travel & Events | Travel & Accommodation, Otomotive & Transport, Event & Entertainment, Wedding |
| `education-community` | Pendidikan & Komunitas | Education & Community | Education, Non Profit |

Label ada di `src/i18n/content.ts` (`templateCategories`). Urutan tab mengikuti urutan kunci di objek itu.

## Tampilan dan urutan

- Template yang ada di `live-previews.json` **tampil paling depan** di kategorinya, dengan tombol **Live preview**.
- Daftar "Semua" **diselang-seling antarkategori** supaya halaman pertama bervariasi.
- Home menampilkan 6 template per tab. Katalog menampilkan 12 per halaman.

## Thumbnail

- Lokasi: `public/images/templates/<code>.webp`, berukuran **640×400**, WebP kualitas 72, sekitar 15 KB.
- Sumber: screenshot halaman **Home** di dalam kit (template bertipe `single-home`), dipotong bagian atasnya dengan rasio 16:10.
- Template tanpa screenshot (saat ini #0021 Credice) ditampilkan dengan nama saja (`thumbnail: false`).

## File kit (di luar repo)

```
~/Downloads/500 Premium WordPress Elementor Template Kit/
├── TEMPLATE FREE/
│   ├── 0001-agenci.zip … 0218-plentiful.zip      ← 218 kit siap pakai, nama = kode
│   └── acuan-live-preview-template.xlsx          ← acuan kerja live preview
└── <folder kategori asli>/                        ← arsip 568 kit asli, termasuk yang butuh Elementor Pro
```

`acuan-live-preview-template.xlsx` berisi, untuk setiap kode: rute katalog, slug site WordPress, URL live preview, nama file kit, halaman yang perlu dibuat, plugin yang dibutuhkan, dan kolom status (Belum / Proses / Live / Ditunda).

### Lisensi

Kit berasal dari paket Envato Elements yang dijual ulang. Foto dan ilustrasi di dalamnya **tidak berlisensi** untuk dipakai di website klien. Ganti dengan foto berlisensi (Unsplash, Pexels, atau foto milik klien) sebelum website klien dipublikasikan.

## Menambah template baru

> **Catatan:** script yang dulu dipakai untuk membuat `templates.json` dan thumbnail dari file ZIP **belum ada di repo**. Sampai script itu ditambahkan ke `scripts/`, lakukan langkah ini secara manual.

1. **Pastikan kit tidak butuh Elementor Pro.** Buka `manifest.json` di dalam ZIP, lalu cek `required_plugins`.
2. **Beri kode berikutnya** (contoh `0219`), lalu ganti nama file ZIP menjadi `0219-<nama>.zip` dan simpan di folder `TEMPLATE FREE`.
3. **Buat thumbnail** dari screenshot Home di dalam kit (folder `screenshots/`), ukuran 640×400, potong dari atas, format WebP. Simpan sebagai `public/images/templates/0219.webp`.
4. **Tambahkan objek** ke `src/data/templates.json` dengan `category` memakai salah satu slug di atas.
5. Jalankan `npm run build`, lalu cek kartu baru di katalog.
6. Tambahkan baris baru di file Excel acuan.

## Membuat live preview

Lihat [wordpress-preview.md](wordpress-preview.md). Setelah demo siap, tambahkan kodenya ke `src/data/live-previews.json` dan ubah status di Excel menjadi **Live**.

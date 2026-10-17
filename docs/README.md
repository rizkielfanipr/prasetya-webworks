# Dokumentasi Prasetya Webworks

Indeks semua dokumentasi project. Baca sesuai kebutuhan.

## Untuk developer

| Dokumen | Isi |
|---|---|
| [architecture.md](architecture.md) | Gambaran sistem, struktur kode, rute, i18n, alur data |
| [development.md](development.md) | Setup lokal, perintah, konvensi kode (struktur, CSS, JS), tugas umum, pengujian |
| [deployment.md](deployment.md) | CI/CD, secret, struktur server, `.htaccess` pengarah, rollback |
| [troubleshooting.md](troubleshooting.md) | Masalah yang pernah terjadi beserta solusinya |

## Operasional

| Dokumen | Isi |
|---|---|
| [template-catalog.md](template-catalog.md) | Model data katalog template, kategori, kode, menambah template, thumbnail |
| [wordpress-preview.md](wordpress-preview.md) | Setup WordPress Multisite untuk live preview dan langkah membuat satu demo |

## Keputusan teknis

[decisions/](decisions/README.md) berisi **Architecture Decision Records (ADR)**: catatan singkat *kenapa* sebuah keputusan teknis diambil, supaya tidak perlu diperdebatkan ulang.

## Menjaga dokumentasi tetap benar

- Ubah dokumen **di commit yang sama** dengan perubahan kode yang memengaruhinya.
- Keputusan teknis baru yang mengubah arah (hosting, cara deploy, struktur rute) ditulis sebagai ADR baru. ADR lama tidak diedit, cukup ditandai *Superseded* dan diberi tautan ke ADR penggantinya.

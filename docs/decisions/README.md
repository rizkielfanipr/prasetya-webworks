# Architecture Decision Records (ADR)

Setiap ADR mencatat **satu** keputusan teknis: konteks, keputusan, dan konsekuensinya. Formatnya mengikuti [Michael Nygard](https://cognitect.com/blog/2011/11/15/documenting-architecture-decisions).

| No | Keputusan | Status |
|---|---|---|
| [0001](0001-static-astro-on-cpanel.md) | Website statis Astro di shared hosting cPanel | Accepted |
| [0002](0002-deploy-ssh-rsync.md) | Deploy lewat SSH + rsync dari GitHub Actions | Accepted |
| [0003](0003-subfolder-router.md) | Domain utama dilayani dari subfolder lewat `.htaccess` pengarah | Accepted |
| [0004](0004-wordpress-multisite-previews.md) | Live preview template memakai WordPress Multisite (subdirectory) | Accepted |
| [0005](0005-template-catalog-data.md) | Katalog dari kit tanpa Elementor Pro, dengan kode template tetap | Accepted |
| [0006](0006-english-urls.md) | Semua URL dan anchor berbahasa Inggris | Accepted |
| [0007](0007-component-structure.md) | Komponen per section, gaya di-scope, type check di CI | Accepted |
| [0008](0008-enforced-conventions.md) | Konvensi kode ditegakkan oleh alat dan AGENTS.md | Accepted |

## Menulis ADR baru

1. Salin format ADR yang ada, beri nomor berikutnya: `NNNN-judul-singkat.md`.
2. Isi **Konteks → Keputusan → Konsekuensi**. Cukup singkat.
3. Tambahkan baris ke tabel di atas.
4. Kalau keputusan baru menggantikan yang lama, ubah status ADR lama menjadi `Superseded by NNNN`. Jangan menghapusnya.

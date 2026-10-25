# ADR 0010 — Pemesanan dan konsultasi lewat WhatsApp

## Status

Accepted — 24 Oktober 2026

## Konteks

Modal paket sebelumnya membuka aplikasi email lewat `mailto:`. Di HP sering tidak ada aplikasi email yang tersetel, padahal calon pelanggan umumnya lebih cepat merespons lewat WhatsApp. Situs ini statis di cPanel (ADR 0001), jadi tidak ada backend untuk menyimpan pesanan.

## Keputusan

- Modal paket menyusun ringkasan pesanan (paket, harga, nama, bisnis, domain, email, WhatsApp, catatan) lalu membuka `https://wa.me/<site.whatsapp>?text=...` lewat `openWhatsApp()` di `src/scripts/whatsapp.ts`.
- Nomor tujuan ada di `site.whatsapp` (`src/config/site.ts`).
- Pemesan wajib mencentang persetujuan bahwa pesanan dikonfirmasi lewat WhatsApp. Pesanan baru dianggap sah setelah dikonfirmasi admin.
- Data paket (harga, ekstensi domain, revisi, estimasi) ada di `src/i18n/content.ts`. Tombol paket meneruskannya ke modal sebagai JSON di `data-package`.
- Form kontak di home dihapus dan diganti banner ajakan (`#contact`) dengan tombol ke `#packages` dan tautan konsultasi `wa.me`. Tombol "Pilih template" di home dan katalog membuka halaman form `/order/?template=<kode>` (3 langkah sesuai Cara Kerja), yang juga berakhir dengan ringkasan ke WhatsApp. `mailto.ts` dan `contact.ts` dihapus.

## Konsekuensi

- ✅ Tidak butuh backend. Pesanan langsung masuk ke chat yang dipakai tim sehari-hari.
- ⚠️ Pesanan tidak tercatat di sistem mana pun selain chat WhatsApp, dan tidak ada data analytics konversi.
- ⚠️ Pengunjung tanpa WhatsApp akan diarahkan ke WhatsApp Web.
- ⚠️ Nomor di `site.whatsapp` harus nomor bisnis asli sebelum deploy.

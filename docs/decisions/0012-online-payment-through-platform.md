# ADR 0012 — Pembayaran online lewat Prasetya Platform

## Status

Proposed — 1 November 2026

## Konteks

ADR 0010 mengarahkan semua pesanan ke WhatsApp karena situs ini statis dan tidak punya backend. Prasetya Platform kini menyediakan API pesanan dan pembayaran DOKU. Pemilik ingin pelanggan tetap bisa konsultasi dulu, tetapi juga bisa langsung bayar dari situs.

## Keputusan

- Setelah form dikirim, dialog menawarkan **Konsultasi dulu** (alur WhatsApp ADR 0010) atau **Langsung bayar** (pesanan dibuat di platform, lalu pelanggan diarahkan ke halaman bayar).
- Semua ini hanya aktif jika `PUBLIC_PLATFORM_API_URL` diisi saat build. Jika kosong, situs persis seperti ADR 0010, sehingga kode ini aman berada di `main` sebelum platform di-deploy.
- Harga di dialog diambil dari platform saat dialog dibuka. Harga di `content.ts` hanya untuk tampilan katalog dan bisa diambil dari API saat build pada pekerjaan berikutnya. Kode paket (`code`) bersifat permanen.
- Situs tidak pernah mengirim harga dan tidak pernah menyimpulkan status pembayaran. Halaman `/order/status/` hanya menampilkan jawaban `GET /orders/{reference}/payment-status`; kembali dari halaman bayar bukan bukti pembayaran.
- `sessionStorage` hanya menyimpan Idempotency-Key dan locale, agar refresh atau klik ulang tidak membuat pesanan kedua. Tidak ada data pembayaran yang disimpan di browser.
- Domain tidak dicek otomatis. Jika domain tidak tersedia, pelanggan bisa memilih domain lain; ini dinyatakan di dialog dan halaman status, dan dikerjakan lewat WhatsApp oleh tim.
- Jika platform tidak bisa dihubungi, tombol bayar nonaktif dan WhatsApp tetap berfungsi, sehingga pesanan tidak hilang.

## Konsekuensi

- ✅ Satu form untuk kedua alur, dan ADR 0010 tetap berlaku untuk pilihan konsultasi.
- ⚠️ Data pelanggan kini tersimpan di database platform. Kebijakan privasi perlu disiapkan sebelum go-live.
- ⚠️ Harga katalog dan harga platform bisa berbeda sampai katalog mengambil harga dari API. Dialog selalu menampilkan harga platform.
- ⚠️ Ganti domain setelah bayar masih manual dan belum tercatat di platform selain sebagai catatan admin.

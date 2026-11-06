# ADR 0013 — Cek ketersediaan domain lewat RDAP

## Status

Accepted — 4 November 2026.

## Konteks

Form pesanan (modal paket dan `/order/`) meminta nama domain yang diinginkan. Sebelumnya tidak ada pengecekan, sehingga pelanggan bisa membayar untuk domain yang ternyata sudah dipakai orang lain dan baru tahu saat admin mendaftarkannya. Situs ini statis (ADR 0001) dan belum memakai akun reseller domain, jadi tidak ada API registrar yang bisa dipanggil.

RDAP adalah layanan resmi registry untuk data pendaftaran domain dalam format JSON, gratis dan tanpa API key. Hasil tes 4 November 2026: `rdap.pandi.id` (.id, .my.id, .web.id) dan `rdap.verisign.com` (.com, .net) menjawab 200 untuk domain terdaftar dan 404 untuk yang belum, sekitar 0,2–0,4 detik, dengan `Access-Control-Allow-Origin: *` sehingga bisa dipanggil langsung dari browser.

## Keputusan

- `src/scripts/domain-check.ts` (`domainAvailability()`) memanggil RDAP langsung dari browser: registry resmi untuk ekstensi yang dijual (`id`, `com`, `net`), dan `rdap.org` sebagai cadangan untuk ekstensi lain.
- Jawaban `rdap.org` hanya dipakai kalau request benar-benar diteruskan ke registry (`response.redirected`). Untuk ekstensi yang tidak punya RDAP (misalnya `.co`), `rdap.org` menjawab 404 sendiri, yang kalau dibaca mentah akan terlihat "tersedia".
- Request dikirim tanpa header tambahan agar tetap *simple request* tanpa CORS preflight.
- `OrderFields` mengecek setelah pengunjung berhenti mengetik (500 ms) atau saat ekstensi berganti (mengamati `[data-domain-suffix]`). Status: kemungkinan tersedia, sudah dipakai, format tidak valid, atau belum bisa dicek.
- Nama yang sudah dipakai atau tidak valid memblokir pengiriman lewat `setCustomValidity()`. Kalau RDAP gagal dijangkau, pesanan **tetap bisa dikirim**, jadi gangguan registry tidak membuat pesanan hilang.
- Teks yang tampil "kemungkinan tersedia", karena 404 hanya berarti belum terdaftar. Nama yang dicadangkan registry atau baru dihapus tetap bisa gagal saat didaftarkan, jadi admin tetap memastikan sebelum membeli.
- `/order/` memakai `novalidate` dan memvalidasi sendiri saat kirim. Field domain ada di langkah 2, sedangkan ekstensi dipilih di langkah 3. Tanpa ini, browser memblokir kirim tanpa pesan karena field yang invalid tersembunyi. Sekarang pengunjung dibawa kembali ke langkah yang bermasalah.

## Konsekuensi

- ✅ Pelanggan tahu sebelum membayar kalau domainnya sudah dipakai, tanpa backend dan tanpa biaya.
- ⚠️ Bergantung pada layanan RDAP pihak ketiga tanpa jaminan uptime. Kalau nanti dibatasi, pindahkan pengecekan ke Prasetya Platform (dengan cache dan rate limit) atau ke API reseller domain.
- ⚠️ Browser mencatat request yang dijawab 404 sebagai error di konsol. Itu jawaban normal untuk domain yang belum terdaftar.
- ⚠️ Menambah ekstensi baru di paket: kalau registry-nya belum ada di `registries`, pengecekan lewat `rdap.org`. Tambahkan registry resminya kalau ekstensi itu sering dipakai.

# 0004. Live preview template memakai WordPress Multisite (subdirectory)

- **Status:** Accepted
- **Tanggal:** 2026-10-17

## Konteks
Calon klien perlu mencoba template sebagai website sungguhan sebelum memesan. Template berupa kit Elementor (WordPress). Paket hosting tidak mengizinkan addon domain, dan resource-nya terbatas.

## Keputusan
Satu instalasi **WordPress Multisite mode subdirectory** di `preview.prasetyawebworks.web.id`. Setiap template mendapat satu site di `/template-<kode>/`. Semua site dibuat `noindex` lewat mu-plugin. Live preview dibuat **bertahap** hanya untuk template terpilih, dan website menautkannya lewat `src/data/live-previews.json`.

Mode subdomain (`template-0001.preview…`) tidak dipakai, karena membutuhkan wildcard DNS dan wildcard SSL.

## Konsekuensi
- ✅ Satu instalasi untuk semua demo, dengan tema dan plugin dikelola terpusat. Tanpa wildcard DNS atau SSL.
- ✅ Demo tidak bersaing dengan website utama di Google (`noindex`).
- ⚠️ Membuat satu demo masih manual (sekitar 10–20 menit). 218 demo tidak realistis di paket Starter, jadi demo hanya untuk template unggulan.
- ⚠️ WordPress berada di akun cPanel yang sama dengan website utama. Plugin yang rentan berisiko ke semuanya, jadi wajib update rutin.

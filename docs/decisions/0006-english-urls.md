# 0006. Semua URL dan anchor berbahasa Inggris

- **Status:** Accepted
- **Tanggal:** 2026-10-17

## Konteks
Awalnya rute versi Indonesia memakai bahasa Indonesia (`/template/kuliner/`, `#kontak`), sedangkan versi Inggris memakai bahasa Inggris (`/en/templates/…`). Akibatnya struktur URL kedua bahasa berbeda, dan slug kategori ikut berbahasa Indonesia.

## Keputusan
Semua path dan anchor memakai **bahasa Inggris**, dengan bentuk jamak untuk koleksi:
- katalog: `/templates/`, `/templates/<category>/`, `/templates/<category>/page/<n>/`;
- versi Inggris sama persis dengan prefix `/en`;
- slug kategori berbahasa Inggris (`food-lifestyle`, `business-technology`, dan seterusnya);
- anchor home: `#why-us`, `#packages`, `#templates`, `#faq`, `#contact`, `#partners`.

Teks yang **tampil** di halaman tetap mengikuti bahasa halaman.

## Konsekuensi
- ✅ Struktur URL ID dan EN identik, jadi mudah dirawat dan tidak menimbulkan kebingungan.
- ⚠️ URL lama (`/template/…`, `#kontak`) sudah tidak berlaku (404). Ini diterima karena website baru tayang dan belum ada tautan lama yang tersebar.

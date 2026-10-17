# 0007. Komponen per section, gaya di-scope, dan type check di CI

- **Status:** Accepted
- **Tanggal:** 2026-10-17

## Konteks
Seluruh halaman home (header, 8 section, modal, dan semua script) berada di satu file `src/pages/index.astro` (375 baris), dengan CSS dalam baris sangat panjang (sampai 3.672 karakter). Beberapa selector ditulis dua kali, sehingga aturan yang belakangan diam-diam menimpa yang awal. Ada juga CSS untuk elemen yang sudah tidak ada. Halaman katalog punya header sendiri hasil salinan. Proyek juga belum menjalankan type check, sehingga error TypeScript baru ketahuan saat runtime.

## Keputusan
- Home dipecah menjadi **satu komponen per section** di `src/components/home/`, disusun oleh `HomePage.astro`. Rute `pages/index.astro` dan `pages/en/index.astro` hanya memanggilnya.
- **Header bersama** (`SiteHeader`) dipakai home dan katalog, dengan link yang menyesuaikan halaman. Komponen generik (`SectionIntro`, `FilterChips`, `Pagination`) ada di `components/ui/`.
- Setiap komponen memegang markup, `<style>` scoped, dan `<script>`-nya sendiri. Logika bersama dipindah ke `src/scripts/`. `global.css` hanya untuk token, gaya dasar, dan utilitas lintas komponen.
- Konstanta situs dipusatkan di `src/config/site.ts`.
- `@astrojs/check` dan `typescript` ditambahkan. `npm run check` dijalankan di CI sebelum build.
- Refactor diverifikasi dengan **perbandingan screenshot piksel per piksel**. Hasilnya, home ID identik 0 piksel di 1440, 768, dan 390 px.

## Konsekuensi
- ✅ Setiap bagian bisa ditemukan, dibaca, dan diubah tanpa menyentuh yang lain. Gaya tidak bocor antarkomponen.
- ✅ Halaman katalog kini punya navigasi lengkap yang sama dengan home.
- ✅ Error tipe menggagalkan deploy, bukan sampai ke pengunjung.
- ⚠️ Perubahan tampilan yang disengaja:
  - header katalog sekarang sama dengan header home (fixed, dengan menu);
  - pemilih bahasa desktop selalu berurutan "ID / EN".
- ⚠️ Komponen yang berkomunikasi lewat atribut data (misalnya `PricingSection` dan `PackageModal`) harus menjaga nama atributnya tetap sama.

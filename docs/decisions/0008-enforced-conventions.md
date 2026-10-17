# 0008. Konvensi kode ditegakkan oleh alat dan AGENTS.md

- **Status:** Accepted
- **Tanggal:** 2026-10-17

## Konteks
Setelah refactor ([0007](0007-component-structure.md)), konvensi kode tertulis di `docs/development.md`. Aturan yang hanya tertulis mudah terlupa saat menambah fitur, terutama karena sebagian besar kode project ini ditulis bersama AI asisten yang memulai setiap sesi tanpa ingatan sesi sebelumnya.

## Keputusan
- **Alat otomatis**, dijalankan lewat `npm run validate` dan diwajibkan di CI sebelum build:
  - Prettier dengan `prettier-plugin-astro` untuk format;
  - ESLint (`@eslint/js`, `typescript-eslint`, `eslint-plugin-astro`) untuk JS/TS;
  - Stylelint (`stylelint-config-recommended` + aturan project) untuk CSS, termasuk larangan selector dobel dan `filter: blur()`;
  - `astro check` untuk tipe.
- **Ringkasan konvensi untuk AI asisten** di `AGENTS.md` (dibaca otomatis tiap sesi, `CLAUDE.md` adalah symlink ke file itu), merujuk ke dokumentasi lengkap.
- `.editorconfig` untuk editor.

## Konsekuensi
- ✅ Pelanggaran format, lint, atau tipe menggagalkan deploy, bukan sampai ke produksi.
- ✅ AI asisten mengikuti struktur dan aturan yang sama tanpa perlu diingatkan.
- ⚠️ Stylelint saat ini membawa kerentanan *denial of service* lewat dependensi `braces`. Kerentanan ini hanya ada di alat pengembangan dan tidak ikut ke website (`npm audit --omit=dev` = 0). Perbarui Stylelint saat perbaikannya tersedia.
- ⚠️ Pemformatan pertama mengubah 28 file. Diverifikasi tanpa perubahan tampilan (screenshot identik di 12 kombinasi halaman dan lebar layar).
- ⚠️ Aturan yang belum bisa ditegakkan alat (misalnya "pakai token, bukan nilai mentah" dan "teks lewat `content.ts`") tetap bergantung pada review dan `AGENTS.md`.

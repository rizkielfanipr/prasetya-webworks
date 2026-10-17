# Pengembangan

## Prasyarat

- Node.js **≥ 22.12** (lihat `engines` di `package.json`). CI memakai Node 22.
- npm (lockfile: `package-lock.json`).
- Editor yang membaca `.editorconfig`: indentasi tab, UTF-8, LF. Untuk VS Code, pasang ekstensi Astro (direkomendasikan di `.vscode/extensions.json`), serta Prettier, ESLint, dan Stylelint, supaya masalah terlihat langsung di editor.

## Perintah

| Perintah | Fungsi |
|---|---|
| `npm install` | Pasang dependensi |
| `npx astro dev --background` | Dev server di background (`npx astro dev status` / `logs` / `stop`) |
| `npm run format` | Rapikan format semua file dengan Prettier |
| `npm run lint` | ESLint (JS/TS di `.ts` dan `.astro`) + Stylelint (CSS) |
| `npm run check` | Type check seluruh project (`.ts` dan `.astro`) |
| `npm run validate` | **Gabungan:** cek format + lint + type check. **Harus lolos.** CI menjalankannya sebelum build, dan kalau gagal, deploy berhenti |
| `npm run build` | Build produksi ke `dist/` |
| `npm run preview` | Menyajikan hasil build secara lokal |

> Di mode dev, toolbar audit Astro ikut memuat semua gambar. Untuk mengukur performa, misalnya berapa thumbnail yang terunduh, selalu uji dari hasil `npm run build`.

## Konvensi kode

### Struktur
- **Rute (`src/pages/`) tetap tipis.** Isinya hanya import komponen halaman lalu meneruskan `locale` dan parameter.
- **Letak komponen:**
  - `components/layout/`: bagian yang muncul di semua halaman (header, footer, tombol melayang).
  - `components/ui/`: komponen generik yang tidak tahu soal bisnis (judul section, filter, pagination). Teksnya diterima lewat props.
  - `components/home/`: section halaman home.
  - `components/templates/`: katalog template.
- **Logika JS yang dipakai di lebih dari satu komponen** ditaruh di `src/scripts/` sebagai fungsi yang di-`export`, lalu di-`import` dari `<script>` komponen.
- **Konstanta situs** (email, logo, URL) diambil dari `src/config/site.ts`. Jangan menulis ulang nilainya di komponen.

### Teks dan bahasa
- Teks UI tidak ditulis langsung di komponen. Tambahkan ke `src/i18n/content.ts` di objek `id` **dan** `en` dengan kunci yang sama.
- URL dan anchor berbahasa Inggris, huruf kecil, kata dipisah tanda hubung, dan jamak untuk koleksi (`/templates/`, `#packages`).

### CSS
- Gaya komponen ditulis di `<style>` komponen itu sendiri (otomatis di-scope). Hanya token, gaya dasar, dan utilitas lintas komponen yang masuk `src/styles/global.css`.
- **Selalu pakai token**, bukan nilai mentah: `var(--blue)`, `var(--font-serif)`, `var(--header-height)`, dan seterusnya.
- **Satu aturan per selector.** Jangan menulis selector yang sama dua kali di tempat berbeda dalam satu file. Ubah aturan yang sudah ada.
- Format multi-baris, satu properti per baris. Untuk aturan pendek di dalam `@media`, satu baris boleh.
- Urutan blok: aturan dasar → `@keyframes` → `@media` dari lebar ke sempit (1000 → 800 → 560 px) → `prefers-reduced-motion`.
- Hindari `filter: blur()` di dalam container `overflow:hidden` yang punya `border-radius`, karena Safari iOS memotongnya berbentuk persegi. Pakai `radial-gradient`.
- Hindari `:global()`. Kalau sebuah gaya harus berlaku lintas komponen, letakkan di `global.css`.

### JavaScript
- `<script>` komponen adalah module (TypeScript). Ambil elemen lewat `id` atau atribut `data-*` milik komponen itu sendiri.
- Hormati `prefers-reduced-motion` (`prefersReducedMotion()` dari `src/scripts/motion.ts`).
- Untuk efek saat scroll, pakai `onScrollFrame()` supaya tidak berjalan lebih dari sekali per frame.

### Alat yang menegakkan aturan ini

| Alat | Konfigurasi | Yang ditangkap |
|---|---|---|
| Prettier | `.prettierrc.json`, `.prettierignore` | Format kode: tab, kutip tunggal, lebar 140 kolom. `templates.json` dan file `.md` dikecualikan |
| ESLint | `eslint.config.mjs` | Variabel tidak terpakai, `any`, pola JS yang rawan bug, di `.ts` dan di `<script>`/frontmatter `.astro` |
| Stylelint | `stylelint.config.mjs` | Selector dan properti dobel, `filter: blur()`, properti CSS usang, sintaks tidak valid |
| `astro check` | `tsconfig.json` | Error TypeScript, termasuk props komponen yang salah |
| `.editorconfig` | `.editorconfig` | Indentasi dan akhir baris di editor |

Aturan untuk AI asisten (Claude Code dan sejenisnya) ada di `AGENTS.md` (`CLAUDE.md` adalah symlink ke file itu) dan dibaca otomatis setiap sesi. Kalau konvensi di dokumen ini berubah, ubah juga ringkasannya di sana.

### Lain-lain
- Komentar ditulis seperlunya, untuk menjelaskan **alasan**, bukan mengulang isi kode.
- **Commit** memakai format [Conventional Commits](https://www.conventionalcommits.org/): `feat:`, `fix:`, `refactor:`, `style:`, `ci:`, `docs:`, `chore:`.
- **Dokumentasi** diperbarui di commit yang sama dengan perubahan kodenya.

## Tugas yang sering dilakukan

### Mengubah teks
Edit `src/i18n/content.ts`. Cari teksnya, ubah versi `id` dan `en`.

### Menambah section baru di home
1. Buat `src/components/home/NamaSection.astro` dengan prop `locale`, dan pakai `SectionIntro` untuk judulnya.
2. Tambahkan teksnya di `content.ts`.
3. Pasang di `HomePage.astro` sesuai urutan.
4. Kalau ingin ikut animasi muncul, tambahkan selector-nya ke daftar `initScrollReveal([...])` di `HomePage.astro`.
5. Kalau perlu link di menu, tambahkan ke `links` di `SiteHeader.astro` dan `SiteFooter.astro`.

### Menandai template punya live preview
Tambahkan kode template ke `src/data/live-previews.json`:

```json
[
	"0001",
	"0002",
	"0103"
]
```

Template itu otomatis mendapat tombol **Live preview** (membuka `<previewBaseUrl>/template-<kode>/` di tab baru) dan tampil paling depan di kategorinya. Pastikan demo di WordPress sudah siap sebelum push. Lihat [wordpress-preview.md](wordpress-preview.md).

### Mengubah jumlah template per halaman
- Katalog: `CATALOG_PAGE_SIZE` di `src/data/templates.ts`.
- Home: `previewSize` di `src/components/home/TemplatesSection.astro`.

### Menampilkan section mitra
Di `src/components/home/HomePage.astro`, ubah `const showPartners = false;` menjadi `true`, lalu ganti logo placeholder di `PartnersSection.astro` dengan logo klien asli. Link menu "Mitra" di header dan footer ikut muncul.

### Mengganti email, logo, atau domain preview
Edit `src/config/site.ts`.

### Menambah atau mengganti gambar statis
Taruh di `public/images/` dan rujuk dengan path absolut (`/images/nama-file.webp`). Pakai WebP untuk foto, dan hapus file yang sudah tidak dirujuk.

## Pengujian sebelum push

Belum ada tes otomatis. Minimal lakukan:

1. `npm run format`, lalu `npm run validate` lolos, dan `npm run build` berhasil.
2. Buka hasil `npm run preview` dan cek:
   - home ID dan EN, katalog, satu halaman kategori, dan satu halaman pagination;
   - lebar HP (360 px dan 414 px), tablet (768 px), dan desktop, tanpa scroll horizontal;
   - tab filter, tombol "Lihat semua", "Pilih template" (pesan terisi di form kontak), modal paket, menu mobile, dan Live preview.
3. Kalau mengubah layout hero atau kartu, perhatikan perbedaan font antar platform. Android tidak punya font serif yang dipakai judul (lihat [troubleshooting.md](troubleshooting.md)).

**Untuk refactor**, yaitu perubahan yang seharusnya tidak mengubah tampilan: ambil screenshot satu halaman penuh **sebelum dan sesudah** di beberapa lebar layar, dengan `prefers-reduced-motion: reduce` supaya animasi tidak ikut, lalu bandingkan piksel per piksel. Cara ini dipakai saat merapikan `index.astro` menjadi komponen per section, dan hasilnya home identik 0 piksel.

## Hal yang tidak boleh di-commit

- File di luar kebutuhan website (aset brand, PDF, file ZIP kit) disimpan di luar repo, misalnya `~/Downloads/Prasetya Webworks - Brand Assets/`.
- Kunci SSH, password, atau API key. Simpan sebagai GitHub Secret (lihat [deployment.md](deployment.md)).

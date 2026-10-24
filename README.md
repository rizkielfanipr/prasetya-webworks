# Prasetya Webworks

Website company profile dan katalog template untuk **Prasetya Webworks**, jasa pembuatan website untuk UMKM dan bisnis.

- **Produksi:** https://prasetyawebworks.web.id (ID) · https://prasetyawebworks.web.id/en/ (EN)
- **Live preview template (WordPress):** https://preview.prasetyawebworks.web.id
- **Repo:** https://github.com/rizkielfanipr/prasetya-webworks

## Tech stack

| Bagian | Teknologi |
|---|---|
| Website | [Astro](https://astro.build) 7 (output statis), TypeScript, CSS per komponen |
| Ikon | Font Awesome Free (brands) |
| Hosting | cPanel shared hosting (GRIV CLOUD), Apache |
| CI/CD | GitHub Actions → build → rsync lewat SSH |
| Live preview template | WordPress Multisite + Elementor (subdomain `preview.`) |

## Mulai cepat

Butuh **Node.js ≥ 22.12**.

```sh
npm install
npx astro dev --background   # dev server di background (lihat AGENTS.md)
npm run format               # rapikan format (Prettier)
npm run validate             # format + lint + type check, harus lolos (dijalankan juga di CI)
npm run build                # build produksi ke dist/
npm run preview              # cek hasil build secara lokal
```

Kelola dev server background dengan `npx astro dev status`, `npx astro dev logs`, dan `npx astro dev stop`.

**Deploy otomatis:** setiap push ke `main` di-build dan diunggah ke hosting. Lihat [docs/deployment.md](docs/deployment.md).

## Struktur folder

```
.github/workflows/   CI/CD (deploy.yml)
docs/                Dokumentasi project
public/              Aset statis yang disalin apa adanya (favicon, gambar, thumbnail template)
src/
  components/
    layout/          Header, footer, tombol konsultasi melayang (semua halaman)
    ui/              Komponen generik: SectionIntro, FilterChips, Pagination
    home/            Halaman home, satu komponen per section
    templates/       Kartu dan halaman katalog template
  config/            Konstanta situs (email, logo, URL preview)
  data/              Data katalog template + helper
  i18n/              Semua teks UI dalam Bahasa Indonesia dan Inggris
  layouts/           Kerangka HTML
  pages/             Rute (file-based routing Astro), hanya meneruskan ke komponen halaman
  scripts/           Modul JS bersama (reveal, WhatsApp, motion)
  styles/            global.css: design token, gaya dasar, utilitas
```

Penjelasan lengkap ada di [docs/architecture.md](docs/architecture.md).

## Dokumentasi

Mulai dari [docs/README.md](docs/README.md).

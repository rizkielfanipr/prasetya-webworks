# Arsitektur

## Gambaran sistem

```
                 push ke main
Developer ─────────────────────────► GitHub ──► GitHub Actions
                                                  │ npm ci → validate (format, lint, types) → build
                                                  │ rsync via SSH
                                                  ▼
                         server.griv.co.id (cPanel, Apache, user "prasetya")
                         └─ public_html/
                            ├─ .htaccess                       ← pengarah domain utama (dipasang manual)
                            ├─ prasetyawebworks.web.id/        ← hasil build Astro (dist/)
                            └─ preview.prasetyawebworks.web.id/← WordPress Multisite (live preview)

Pengunjung ──► prasetyawebworks.web.id ─────────► website Astro (HTML statis)
           └─► preview.prasetyawebworks.web.id ─► demo template WordPress (noindex)
```

- **Website utama** sepenuhnya statis: tidak ada server Node atau database. Semua halaman dibuat saat build.
- **Live preview template** adalah instalasi WordPress terpisah di subdomain, tidak berbagi kode dengan website Astro. Website hanya menautkannya. Lihat [wordpress-preview.md](wordpress-preview.md).

## Struktur kode

```
src/
├── config/
│   └── site.ts                   Konstanta situs: nama, email, logo, URL WordPress preview
├── styles/
│   └── global.css                Design token, gaya dasar, utilitas bersama (.section-pad, .field-row, .scroll-reveal)
├── scripts/                      Modul TypeScript yang dipakai oleh <script> komponen
│   ├── motion.ts                 prefersReducedMotion(), onScrollFrame()
│   ├── scroll-reveal.ts          initScrollReveal(): animasi muncul saat di-scroll
│   ├── mailto.ts                 openMailto(): membuka aplikasi email dengan pesan siap kirim
│   └── contact.ts                prefillContactMessage(): mengisi form kontak di home
├── components/
│   ├── layout/                   Dipakai semua halaman
│   │   ├── SiteHeader.astro      Header + navigasi + menu mobile + pemilih bahasa
│   │   ├── SiteFooter.astro
│   │   └── WhatsAppFloat.astro   Tombol konsultasi melayang (dipasang di Layout)
│   ├── ui/                       Komponen generik tanpa pengetahuan domain
│   │   ├── SectionIntro.astro    Judul section "judul <em>penekanan</em>" + deskripsi
│   │   ├── FilterChips.astro     Deretan filter pill (mode link atau tombol)
│   │   └── Pagination.astro      Navigasi halaman bernomor
│   ├── home/                     Halaman home, satu file per section
│   │   ├── HomePage.astro        Menyusun semua section + animasi reveal
│   │   ├── HeroSection.astro
│   │   ├── PartnersSection.astro (disembunyikan, lihat flag showPartners)
│   │   ├── BenefitsSection.astro
│   │   ├── PricingSection.astro
│   │   ├── PackageModal.astro    Dialog pemesanan paket
│   │   ├── TemplatesSection.astro
│   │   ├── FaqSection.astro
│   │   ├── ContactSection.astro
│   │   └── TestimonialsPanel.astro
│   └── templates/                Domain katalog template
│       ├── TemplateCard.astro
│       └── TemplateCatalogPage.astro
├── data/
│   ├── templates.json            Data 218 template (lihat template-catalog.md)
│   ├── live-previews.json        Kode template yang sudah punya demo WordPress
│   └── templates.ts              Helper: urutan, kategori, path, pagination
├── i18n/
│   └── content.ts                Semua teks UI, objek `id` dan `en` dengan struktur sama
├── layouts/
│   └── Layout.astro              <head>, hreflang, global.css, WhatsAppFloat
└── pages/                        Rute: hanya meneruskan locale/parameter ke komponen halaman
```

### Prinsip pembagian

- **`pages/` tipis.** Setiap file rute hanya memanggil komponen halaman (`HomePage`, `TemplateCatalogPage`) dengan `locale` dan parameter. Versi ID dan EN memakai komponen yang sama.
- **Satu komponen, satu tanggung jawab.** Markup, gaya (`<style>` scoped), dan perilaku (`<script>`) sebuah bagian berada di file yang sama.
- **Logika yang dipakai lebih dari satu komponen** dipindah ke `src/scripts/`. Contohnya, `prefillContactMessage` dipakai oleh `TemplatesSection` (tombol "Pilih template") dan `ContactSection` (parameter URL dari katalog).
- **Komponen saling berkomunikasi lewat atribut data**, bukan lewat variabel global. Contoh: tombol `[data-package-select]` di `PricingSection` membawa data paket, lalu `PackageModal` membacanya.
- **Konstanta** (email, logo, URL preview) hanya ada di `src/config/site.ts`.

## Rute

| Rute | File | Komponen |
|---|---|---|
| `/`, `/en/` | `pages/index.astro`, `pages/en/index.astro` | `HomePage` |
| `/templates/` | `pages/templates/index.astro` | `TemplateCatalogPage` |
| `/templates/page/<n>/` | `pages/templates/page/[page].astro` | `TemplateCatalogPage` |
| `/templates/<category>/` | `pages/templates/[category].astro` | `TemplateCatalogPage` |
| `/templates/<category>/page/<n>/` | `pages/templates/[category]/page/[page].astro` | `TemplateCatalogPage` |
| `/en/templates/...` | `pages/en/templates/...` | Struktur sama untuk EN |

Daftar halaman katalog dibuat oleh `getStaticPaths()` dari data, jadi menambah template atau kategori otomatis menambah halaman.

**Konvensi URL:** semua path dan anchor berbahasa Inggris, dengan bentuk jamak untuk koleksi (`templates`). Anchor di home: `#why-us`, `#packages`, `#templates`, `#faq`, `#contact`, `#partners`, `#top`. Lihat [ADR 0006](decisions/0006-english-urls.md).

## Bahasa (i18n)

- Bahasa default **Indonesia** tanpa prefix (`/`), Inggris dengan prefix `/en/`. Diatur di `astro.config.mjs` (`prefixDefaultLocale: false`).
- Semua teks ada di `src/i18n/content.ts`. Objek `content.id` dan `content.en` **wajib** punya struktur yang sama, karena TypeScript memakai kunci `content.id` sebagai acuan tipe, misalnya untuk `TemplateCategory`.
- Komponen menerima prop `locale` lalu mengambil `content[locale]`.
- Teks dengan placeholder memakai `{nama}` lalu diganti dengan `.replace()`, contoh `'Halaman {page}'`.
- `Layout` dan `SiteHeader` menerima `alternates` (path halaman yang sama di tiap bahasa) untuk `hreflang` dan pemilih bahasa.

## Alur data katalog template

```
templates.json ──┐
                 ├─► templates.ts ──► urutan: template dengan live preview lebih dulu,
live-previews ───┘                    lalu (untuk "Semua") diselang-seling antarkategori
                                       │
                ┌──────────────────────┴──────────────────────┐
                ▼                                             ▼
   TemplatesSection (home)                     TemplateCatalogPage (/templates/...)
   6 template per tab, FilterChips mode tombol FilterChips mode link + Pagination
   tombol "Lihat semua" → katalog              24 per halaman (CATALOG_PAGE_SIZE)
```

## Alur pemesanan / konsultasi

1. **Dari home:** tombol "Pilih template" memanggil `prefillContactMessage()` untuk mengisi form `#contact`.
2. **Dari katalog:** tautan ke `/?template=<kode>&name=<nama>#contact`. Script `ContactSection` membaca parameter itu, mengisi pesan, lalu membersihkan URL.
3. **Paket:** tombol di `PricingSection` membuka `PackageModal` dengan detail paket.
4. Form kontak dan modal paket mengirim lewat `openMailto()` ke alamat email di `site.ts`, sehingga aplikasi email pengunjung yang terbuka. Teks label email diambil dari atribut `data-*` pada form. Tidak ada backend form.

## Gaya (CSS)

- **`src/styles/global.css`** hanya berisi:
  - **Design token** (CSS variables):
    - warna: `--ink`, `--ivory`, `--paper`, `--blue`, `--blue-hover`, `--blue-deep`, `--blue-soft`, `--muted`, `--line`;
    - font: `--font-sans`, `--font-serif`, `--font-display`;
    - tinggi header: `--header-height` (74 px, atau 66 px di ≤ 800 px).
  - Gaya dasar elemen (`body`, `a`, `button`, …).
  - Utilitas yang dipakai lintas komponen: `.section-pad`, `.field-row`, `.scroll-reveal`.
- **Semua gaya lainnya ada di `<style>` komponen** dan di-scope otomatis oleh Astro. Gaya sebuah komponen tidak bocor ke komponen lain.
- Urutan dalam setiap blok `<style>`: aturan dasar → `@keyframes` → `@media (max-width: 1000px)` → `800px` → `560px` → `prefers-reduced-motion`.
- Breakpoint: 1000px, 800px, 560px.
- Header situs `position: fixed`, jadi halaman selain home memberi jarak atas `calc(var(--header-height) + …)`.

## Fitur yang bisa dinyalakan atau dimatikan

| Flag | Lokasi | Fungsi |
|---|---|---|
| `showPartners` | `src/components/home/HomePage.astro` | Section "mitra" dan link menu "Mitra". Saat ini `false` karena belum ada logo klien asli |
| `previewSize` | `src/components/home/TemplatesSection.astro` | Jumlah template per tab di home (6) |
| `CATALOG_PAGE_SIZE` | `src/data/templates.ts` | Jumlah template per halaman katalog (24) |

## Utang teknis yang diketahui

- Form memakai `mailto:` dan sering tidak berfungsi baik di HP.
- Belum ada `sitemap.xml`, `robots.txt`, link canonical, Open Graph, dan `site` di `astro.config.mjs`.
- Script pembuat `templates.json` dan thumbnail belum ada di repo (lihat [template-catalog.md](template-catalog.md)).
- Belum ada tes otomatis. Regresi tampilan masih diperiksa manual dengan perbandingan screenshot (lihat [development.md](development.md)).

## Kebutuhan produk yang belum dikerjakan

Sisa dari dokumen kebutuhan awal (PRD landing page, ada di riwayat git):

- Tombol WhatsApp ke nomor bisnis asli, dengan pesan awal (termasuk nama paket atau template). Sekarang tombol mengarah ke form `#contact`.
- Form yang benar-benar mengirim data, dengan validasi, status berhasil/gagal, dan anti-spam (honeypot atau rate limit).
- Halaman 404 dan Kebijakan Privasi.
- Analytics untuk event konversi: klik WhatsApp, klik CTA paket, form mulai diisi, dan form terkirim/gagal.
- Structured data `ProfessionalService` (schema.org).
- Konten asli: testimoni klien (sekarang contoh) dan logo mitra (section disembunyikan, `showPartners`).
- Target kualitas: skor Lighthouse ≥ 90 (Performance, Accessibility, Best Practices, SEO), aksesibilitas WCAG 2.2 AA, dan target sentuh sekitar 44×44 px.

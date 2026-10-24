# ADR 0011 — Metadata SEO, sitemap dan data terstruktur

## Status

Accepted — 24 Oktober 2026

## Konteks

Situs harus muncul di Google dengan judul dan deskripsi yang jelas ("Prasetya Webworks - Jasa Bikin Website …") dan bisa dibagikan di WhatsApp/media sosial dengan pratinjau yang rapi. Sebelumnya belum ada `site` di config, sitemap, `robots.txt`, link canonical, Open Graph, maupun data schema.org.

## Keputusan

- `site: 'https://prasetyawebworks.web.id'` di `astro.config.mjs` menjadi sumber semua URL absolut.
- Sitemap dibuat oleh integrasi resmi `@astrojs/sitemap` (dengan anotasi hreflang ID/EN). `public/robots.txt` menunjuk ke `sitemap-index.xml`.
- `Layout.astro` merender `<title>`, meta description, canonical, hreflang absolut, Open Graph dan Twitter card. Teks judul dan deskripsi home ada di `meta` pada `src/i18n/content.ts`; katalog memakai `catalog.metaDescription*`.
- Gambar pratinjau 1200×630 di `public/images/og-image.png` (`site.ogImage`).
- Home menyertakan JSON-LD `WebSite` dan `ProfessionalService` (nama, URL, logo, email, wilayah, dan paket sebagai `Offer` dengan harga IDR), lewat prop `structuredData` di `Layout`.
- Nomor telepon dan profil sosial media belum dimasukkan ke JSON-LD selama masih placeholder.

## Konsekuensi

- ✅ Judul, deskripsi dan pratinjau link bisa diatur dari `content.ts`.
- ⚠️ Kalau domain produksi berubah, ganti `site` di `astro.config.mjs` dan baris `Sitemap:` di `public/robots.txt`.
- ⚠️ `og-image.png` dibuat manual; buat ulang kalau harga atau logo berubah.
- ⚠️ Peringkat untuk kata kunci umum tetap bergantung pada hal di luar kode: Google Search Console, Google Business Profile, konten, dan backlink.

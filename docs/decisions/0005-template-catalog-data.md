# 0005. Katalog dari kit tanpa Elementor Pro, dengan kode template tetap

- **Status:** Accepted
- **Tanggal:** 2026-10-17

## Konteks
Tersedia paket 568 kit Elementor (sumber: Envato Elements, dijual ulang). Hasil pemeriksaan isi ZIP:
- 565 kit berisi JSON dan gambar saja, aman dari sisi kode;
- 3 file adalah tema PHP lengkap yang membundel plugin premium, sehingga tidak dipakai;
- 347 kit membutuhkan Elementor Pro, yang tidak dibeli.

## Keputusan
- Katalog hanya berisi **218 kit yang bisa dipakai dengan Elementor gratis**.
- Setiap template diberi **kode 4 digit yang tetap** (`0001`–`0218`). Kode yang sama dipakai di kartu website, pesan konsultasi, alamat site preview, nama file kit (`<kode>-<nama>.zip`), dan nama thumbnail.
- 22 folder kategori asal digabung menjadi **7 kategori**, supaya tab filter tetap ringkas.
- Data disimpan sebagai JSON di repo (`src/data/templates.json`). Thumbnail berupa WebP 640×400.

## Konsekuensi
- ✅ Tidak butuh lisensi Elementor Pro dan tidak memakai plugin bajakan.
- ✅ Satu kode menghubungkan semua aset template, jadi mudah dilacak.
- ⚠️ Foto di dalam kit tidak berlisensi untuk website klien dan harus diganti.
- ⚠️ Kode tidak boleh diubah setelah dipakai. Template baru selalu mendapat nomor berikutnya.
- ⚠️ Script pembuat data dan thumbnail belum ada di repo (lihat [template-catalog.md](../template-catalog.md)).

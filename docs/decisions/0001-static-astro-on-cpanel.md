# 0001. Website statis Astro di shared hosting cPanel

- **Status:** Accepted
- **Tanggal:** 2026-10-16

## Konteks
Website berisi company profile dan katalog template. Kontennya jarang berubah, dan tidak ada akun pengguna atau transaksi. Hosting yang sudah dibeli adalah shared hosting cPanel (GRIV CLOUD, paket Starter) yang tidak menjalankan Node.js.

## Keputusan
Membangun website dengan **Astro dalam mode output statis**. Semua halaman, termasuk pagination dan kategori katalog, dibuat saat build menjadi HTML biasa, lalu diunggah ke cPanel.

## Konsekuensi
- ✅ Cepat, murah, aman (tidak ada server aplikasi atau database), dan cocok dengan shared hosting.
- ✅ Bisa dipindah ke hosting statis apa pun tanpa mengubah kode.
- ⚠️ Fitur dinamis (form, pengecek domain, dan sejenisnya) butuh layanan terpisah: script PHP kecil di hosting yang sama, layanan pihak ketiga, atau serverless. Saat ini form memakai `mailto:`.
- ⚠️ Setiap perubahan konten butuh build dan deploy, yang sudah otomatis lewat CI ([0002](0002-deploy-ssh-rsync.md)).

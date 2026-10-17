# Troubleshooting

Masalah yang pernah terjadi di project ini, berikut penyebab dan solusinya.

## Deploy

### `Secret SSH_PRIVATE_KEY is missing or empty`
Secret belum dibuat, atau dibuat di tempat yang salah (*Environment secrets* atau tab *Variables*). Buat di **Settings → Secrets and variables → Actions → Repository secrets** dengan nama persis `SSH_PRIVATE_KEY`.

### `SSH_PRIVATE_KEY is not a valid private key`
Isi secret tidak lengkap. Paste seluruh isi file private key, dari baris `-----BEGIN` sampai `-----END`.

### `connect ECONNREFUSED …:21`
Hosting tidak menyediakan FTP. Deploy harus lewat SSH (sudah dipakai sekarang). Lihat [ADR 0002](decisions/0002-deploy-ssh-rsync.md).

### `Host key verification failed`
Kunci SSH server berubah. Ambil yang baru dengan `ssh-keyscan -t ed25519 server.griv.co.id`, lalu perbarui baris `known_hosts` di `.github/workflows/deploy.yml`.

## Server dan domain

### AutoSSL gagal: *"… is unmanaged"*
Nameserver domain belum mengarah ke `ns1/ns2.griv.co.id`, atau DNS belum menyebar. Ganti nameserver di registrar, tunggu beberapa saat, lalu AutoSSL akan berhasil di jadwal berikutnya (tombol *Run AutoSSL* tidak tersedia di paket ini).

### Browser menampilkan "Not Secure" padahal "Certificate is valid"
Chrome masih mengingat pengecualian sertifikat lama (pernah klik *Proceed* waktu sertifikat masih self-signed). Tutup browser sepenuhnya, atau cek di tab incognito.

### Addon domain tidak bisa dibuat ("Share document root" terkunci)
Paket hosting tidak mengizinkan addon domain. Solusinya upgrade paket atau tanya penyedia hosting.

## Tampilan website

### Safari iOS: potongan persegi di sudut section (foto hero terlihat "bocor")
Bug WebKit: elemen dengan `filter: blur()` di dalam container `overflow:hidden` + `border-radius` dipotong berbentuk persegi. Hindari `filter: blur()` untuk dekorasi di dalam container yang melengkung. Pakai `radial-gradient`, dan beri container `isolation: isolate`.

### Android: konten hero terdorong ke kanan
Judul memakai font Iowan, Palatino, atau Georgia, yang tidak ada di Android, sehingga diganti font serif bawaan yang lebih lebar. Kalau teks diberi `white-space: nowrap`, judul memperlebar kolom grid. Selalu batasi kolom dengan `grid-template-columns: minmax(0,1fr)`, dan uji dengan font serif yang lebih lebar.

### Baris bawah footer tidak muncul di desktop
Elemen di dasar halaman tidak pernah memicu `IntersectionObserver` (karena `rootMargin` bawah negatif). Jangan memberi animasi `.scroll-reveal` pada footer.

### Favicon atau CSS lama masih muncul setelah deploy
Cache browser. Refresh paksa atau buka di tab incognito.

## WordPress preview

### Plugin "Template Kit – Import" tidak bisa di-install
Plugin ini butuh **PHP 8.3**. Ganti versi PHP domain preview di cPanel → MultiPHP Manager. Pastikan memilih plugin dari **envato**, bukan plugin lain yang namanya mirip.

### Upload kit gagal karena ukuran file
Naikkan batas PHP (cPanel → MultiPHP INI Editor) dan *Max upload file size* di Admin Jaringan → Pengaturan. Nilainya ada di [wordpress-preview.md](wordpress-preview.md).

### Menu "Template Kit" tidak ada
Menu itu ada di **Perkakas → Template Kit** di dasbor site, bukan di Admin Jaringan.

### Menu "Tampilan → Menu" tidak ada
Site masih memakai tema blok (Twenty Twenty-Five). Aktifkan **Hello Elementor**.

### Elementor: *"Situs Anda tidak memiliki kit standar"*
Kit global Elementor hilang, biasanya setelah import *Global Kit Styles*. Klik **Buat Ulang Kit**, lalu import ulang **Global Kit Styles** dari Perkakas → Template Kit.

### Link Home berakhiran `/home/`
Home belum dijadikan halaman depan. Buka **Pengaturan → Membaca → Laman statis → Beranda: Home**.

### Header masih menampilkan judul site bawaan tema
Header dari kit belum dipasang. Buat lewat **UAE → Header & Footer** dengan *Tampilkan Di: Seluruh Situs Web*.

### Gambar abu-abu bergambar gunung
Itu gambar placeholder bawaan kit Envato, bukan error. Ganti dengan foto sendiri.

# 0002. Deploy lewat SSH + rsync dari GitHub Actions

- **Status:** Accepted
- **Tanggal:** 2026-10-16

## Konteks
Deploy awalnya direncanakan lewat FTP/FTPS (FTP-Deploy-Action). Ternyata port 21 di server menolak semua koneksi, dan cPanel tidak menyediakan akun FTP. Port 22 (SSH) terbuka, dan cPanel menyediakan *SSH Access* untuk mendaftarkan key.

## Keputusan
GitHub Actions membangun website lalu menjalankan `rsync -rlz --delete` lewat SSH ke `public_html/prasetyawebworks.web.id/`. Autentikasinya memakai **deploy key ed25519 khusus** yang disimpan sebagai secret `SSH_PRIVATE_KEY`, dan host key server dipatok di workflow.

## Konsekuensi
- ✅ Password cPanel tidak disimpan di GitHub. Key bisa dicabut kapan saja dari cPanel.
- ✅ Hanya file yang berubah yang dikirim. `--delete` menjaga server tetap sama persis dengan `dist/`.
- ✅ Koneksi ke server palsu ditolak karena host key dipatok.
- ⚠️ Kalau hosting mengganti host key, baris `known_hosts` di workflow harus diperbarui.
- ⚠️ Key memberi akses shell ke akun cPanel. Lindungi akun GitHub dengan 2FA.

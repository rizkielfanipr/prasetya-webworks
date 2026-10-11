from __future__ import annotations

from pathlib import Path

from PIL import Image
from reportlab.lib.colors import Color, HexColor
from reportlab.lib.pagesizes import A4, landscape
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont
from reportlab.pdfgen import canvas


ROOT = Path('/Users/air/Projects/prasetya-webworks')
TMP = ROOT / 'tmp' / 'pdfs'
OUT = ROOT / 'output' / 'pdf'
LOGO_SOURCE = ROOT / 'public' / 'images' / 'prasetya-webworks-logo.png'
PDF_PATH = OUT / 'prasetya-webworks-brand-guidelines.pdf'
PAGE_W, PAGE_H = landscape(A4)

INK = HexColor('#11131A')
INK_2 = HexColor('#1B2030')
BLUE = HexColor('#173A9B')
BLUE_DEEP = HexColor('#0B2368')
BLUE_SOFT = HexColor('#D7E0FB')
IVORY = HexColor('#F4F1EA')
PAPER = HexColor('#FFFDF8')
MUTED = HexColor('#6F7180')
LINE = HexColor('#D9D5CC')
WHITE = HexColor('#FFFFFF')
RED = HexColor('#D75252')


def register_fonts() -> None:
    font_dir = Path('/System/Library/Fonts/Supplemental')
    pdfmetrics.registerFont(TTFont('PW-Sans', str(font_dir / 'Arial.ttf')))
    pdfmetrics.registerFont(TTFont('PW-Sans-Bold', str(font_dir / 'Arial Bold.ttf')))
    pdfmetrics.registerFont(TTFont('PW-Serif', str(font_dir / 'Georgia.ttf')))
    pdfmetrics.registerFont(TTFont('PW-Serif-Bold', str(font_dir / 'Georgia Bold.ttf')))
    pdfmetrics.registerFont(TTFont('PW-Serif-Italic', str(font_dir / 'Georgia Italic.ttf')))


def prepare_assets() -> dict[str, Path]:
    TMP.mkdir(parents=True, exist_ok=True)
    OUT.mkdir(parents=True, exist_ok=True)
    logo = Image.open(LOGO_SOURCE).convert('RGBA')
    alpha_box = logo.getchannel('A').getbbox()
    if alpha_box:
        logo = logo.crop(alpha_box)
    black_logo = TMP / 'logo-black.png'
    white_logo = TMP / 'logo-white.png'
    icon_black = TMP / 'icon-black.png'
    icon_white = TMP / 'icon-white.png'
    logo.save(black_logo)
    white_layer = Image.new('RGBA', logo.size, (255, 255, 255, 0))
    white_layer.putalpha(logo.getchannel('A'))
    white_layer.save(white_logo)
    icon = logo.crop((0, 0, max(1, int(logo.width * .255)), logo.height))
    icon = icon.crop(icon.getchannel('A').getbbox())
    icon.save(icon_black)
    icon_white_layer = Image.new('RGBA', icon.size, (255, 255, 255, 0))
    icon_white_layer.putalpha(icon.getchannel('A'))
    icon_white_layer.save(icon_white)
    return {'logo_black': black_logo, 'logo_white': white_logo, 'icon_black': icon_black, 'icon_white': icon_white}


def draw_text(c: canvas.Canvas, text: str, x: float, y: float, size: float = 10,
              font: str = 'PW-Sans', color: Color = INK) -> None:
    c.setFont(font, size)
    c.setFillColor(color)
    c.drawString(x, y, text)


def wrap_lines(text: str, font: str, size: float, max_width: float) -> list[str]:
    words = text.split()
    lines: list[str] = []
    current = ''
    for word in words:
        candidate = f'{current} {word}'.strip()
        if not current or pdfmetrics.stringWidth(candidate, font, size) <= max_width:
            current = candidate
        else:
            lines.append(current)
            current = word
    if current:
        lines.append(current)
    return lines


def draw_paragraph(c: canvas.Canvas, text: str, x: float, y: float, max_width: float,
                   size: float = 9, leading: float | None = None,
                   font: str = 'PW-Sans', color: Color = MUTED) -> float:
    leading = leading or size * 1.45
    cursor = y
    c.setFont(font, size)
    c.setFillColor(color)
    for line in wrap_lines(text, font, size, max_width):
        c.drawString(x, cursor, line)
        cursor -= leading
    return cursor


def draw_label(c: canvas.Canvas, text: str, x: float, y: float, color: Color = BLUE) -> None:
    c.setFont('PW-Sans-Bold', 7.2)
    c.setFillColor(color)
    c.drawString(x, y, text.upper())


def rounded_box(c: canvas.Canvas, x: float, y: float, w: float, h: float,
                fill: Color = PAPER, stroke: Color | None = LINE, radius: float = 14) -> None:
    c.setFillColor(fill)
    c.setStrokeColor(stroke or fill)
    c.setLineWidth(.8)
    c.roundRect(x, y, w, h, radius, fill=1, stroke=1 if stroke else 0)


def draw_image_cover(c: canvas.Canvas, image_path: Path, x: float, y: float, w: float, h: float,
                     radius: float = 0) -> None:
    im = Image.open(image_path)
    iw, ih = im.size
    scale = max(w / iw, h / ih)
    crop_w, crop_h = w / scale, h / scale
    left = max(0, (iw - crop_w) / 2)
    top = max(0, (ih - crop_h) / 2)
    cropped = im.crop((int(left), int(top), int(left + crop_w), int(top + crop_h)))
    temp = TMP / f'cover-{image_path.stem}-{int(x)}-{int(y)}-{int(w)}-{int(h)}.png'
    cropped.save(temp)
    if radius:
        c.saveState()
        path = c.beginPath()
        path.roundRect(x, y, w, h, radius)
        c.clipPath(path, stroke=0, fill=0)
        c.drawImage(str(temp), x, y, width=w, height=h, preserveAspectRatio=False, mask='auto')
        c.restoreState()
    else:
        c.drawImage(str(temp), x, y, width=w, height=h, preserveAspectRatio=False, mask='auto')


def draw_logo(c: canvas.Canvas, path: Path, x: float, y: float, w: float) -> float:
    im = Image.open(path)
    h = w * im.height / im.width
    c.drawImage(str(path), x, y, width=w, height=h, preserveAspectRatio=True, mask='auto')
    return h


def page_footer(c: canvas.Canvas, page: int, dark: bool = False) -> None:
    color = Color(1, 1, 1, alpha=.5) if dark else MUTED
    c.setStrokeColor(Color(1, 1, 1, alpha=.14) if dark else LINE)
    c.setLineWidth(.5)
    c.line(42, 25, PAGE_W - 42, 25)
    draw_text(c, 'prasetya webworks  /  brand guidelines v1.0  /  oktober 2026', 42, 12, 6.4, 'PW-Sans', color)
    c.setFont('PW-Sans-Bold', 6.4)
    c.setFillColor(color)
    c.drawRightString(PAGE_W - 42, 12, f'{page:02d}')


def page_title(c: canvas.Canvas, number: str, title: str, subtitle: str, dark: bool = False) -> None:
    fg = WHITE if dark else INK
    sub = Color(1, 1, 1, alpha=.67) if dark else MUTED
    draw_label(c, number, 44, PAGE_H - 50, BLUE_SOFT if dark else BLUE)
    draw_text(c, title, 44, PAGE_H - 94, 28, 'PW-Serif', fg)
    draw_paragraph(c, subtitle, 44, PAGE_H - 117, 480, 8.8, 13, 'PW-Sans', sub)


def draw_cover(c: canvas.Canvas, assets: dict[str, Path]) -> None:
    c.setFillColor(INK)
    c.rect(0, 0, PAGE_W, PAGE_H, fill=1, stroke=0)
    c.setFillColor(BLUE_DEEP)
    c.circle(PAGE_W - 60, PAGE_H - 10, 230, fill=1, stroke=0)
    c.setFillColor(BLUE)
    c.roundRect(PAGE_W - 330, -52, 390, 185, 90, fill=1, stroke=0)
    c.setFillColor(Color(1, 1, 1, alpha=.06))
    for i in range(6):
        c.roundRect(55 + i * 34, 66 + i * 18, 230, 12, 6, fill=1, stroke=0)
    c.setFillAlpha(1)
    c.setStrokeAlpha(1)
    draw_logo(c, assets['logo_white'], 58, PAGE_H - 150, 205)
    draw_label(c, 'Brand Guidelines', 58, 245, BLUE_SOFT)
    draw_text(c, 'Identitas yang jelas.', 58, 193, 32, 'PW-Serif', WHITE)
    draw_text(c, 'Bekerja lebih jauh.', 58, 154, 32, 'PW-Serif-Italic', BLUE_SOFT)
    draw_paragraph(c, 'Panduan penggunaan identitas visual Prasetya Webworks untuk menjaga setiap titik kontak tetap konsisten, modern, dan mudah dikenali.', 58, 116, 410, 9.4, 15, 'PW-Sans', Color(1, 1, 1, alpha=.72))
    draw_text(c, 'VERSION 1.0', PAGE_W - 155, 44, 7, 'PW-Sans-Bold', WHITE)
    c.showPage()


def draw_foundation(c: canvas.Canvas, assets: dict[str, Path], page: int) -> None:
    c.setFillColor(PAPER)
    c.rect(0, 0, PAGE_W, PAGE_H, fill=1, stroke=0)
    page_title(c, '01 / FOUNDATION', 'Fondasi merek', 'Prasetya Webworks hadir sebagai studio web yang menggabungkan ketajaman strategi, karakter visual, dan eksekusi yang tenang.')
    cards = [
        ('01', 'Jelas', 'Setiap keputusan desain harus punya alasan dan membantu pengguna memahami langkah berikutnya.'),
        ('02', 'Berkarakter', 'Tampilan terasa khas tanpa bergantung pada dekorasi berlebihan atau tren yang cepat usang.'),
        ('03', 'Terpercaya', 'Bahasa, tata letak, dan interaksi menyampaikan kompetensi dengan cara yang hangat dan manusiawi.'),
    ]
    x0, y0, gap = 44, 135, 16
    card_w = (PAGE_W - 88 - gap * 2) / 3
    for i, (num, title, body) in enumerate(cards):
        x = x0 + i * (card_w + gap)
        rounded_box(c, x, y0, card_w, 180, WHITE, LINE, 20)
        draw_text(c, num, x + 18, y0 + 145, 8, 'PW-Sans-Bold', BLUE)
        draw_text(c, title, x + 18, y0 + 103, 20, 'PW-Serif', INK)
        draw_paragraph(c, body, x + 18, y0 + 79, card_w - 36, 8.3, 13, 'PW-Sans', MUTED)
    draw_label(c, 'Brand promise', 44, 91)
    draw_text(c, 'Website berkualitas untuk bisnis yang siap ', 44, 58, 17, 'PW-Serif', INK)
    offset = pdfmetrics.stringWidth('Website berkualitas untuk bisnis yang siap ', 'PW-Serif', 17)
    draw_text(c, 'naik kelas.', 44 + offset, 58, 17, 'PW-Serif-Italic', BLUE)
    page_footer(c, page)
    c.showPage()


def draw_logo_system(c: canvas.Canvas, assets: dict[str, Path], page: int) -> None:
    c.setFillColor(IVORY)
    c.rect(0, 0, PAGE_W, PAGE_H, fill=1, stroke=0)
    page_title(c, '02 / LOGO', 'Sistem logo', 'Logo utama adalah kombinasi simbol abstrak dan wordmark huruf kecil. Pertahankan proporsi serta hubungan keduanya.')
    rounded_box(c, 44, 195, 465, 210, WHITE, LINE, 22)
    draw_label(c, 'Primary lockup', 65, 373)
    draw_logo(c, assets['logo_black'], 88, 250, 370)
    rounded_box(c, 526, 195, 267, 210, INK, None, 22)
    draw_label(c, 'Reversed lockup', 547, 373, BLUE_SOFT)
    draw_logo(c, assets['logo_white'], 566, 268, 188)
    rounded_box(c, 44, 64, 232, 112, WHITE, LINE, 18)
    draw_label(c, 'Symbol', 62, 145)
    draw_logo(c, assets['icon_black'], 117, 80, 84)
    rounded_box(c, 292, 64, 501, 112, BLUE, None, 18)
    draw_label(c, 'Prinsip penggunaan', 312, 145, WHITE)
    draw_paragraph(c, 'Gunakan lockup utama sebagai pilihan pertama. Simbol mandiri hanya digunakan ketika konteks sudah jelas, misalnya favicon, avatar, atau elemen dekoratif bermerek.', 312, 120, 445, 8.4, 13, 'PW-Sans', Color(1, 1, 1, alpha=.82))
    page_footer(c, page)
    c.showPage()


def draw_spacing(c: canvas.Canvas, assets: dict[str, Path], page: int) -> None:
    c.setFillColor(PAPER)
    c.rect(0, 0, PAGE_W, PAGE_H, fill=1, stroke=0)
    page_title(c, '03 / SPACING', 'Ruang aman & ukuran minimum', 'Berikan logo cukup ruang untuk bernapas. Ruang aman minimum ditentukan oleh tinggi simbol dan berlaku di semua sisi.')
    x, y, w = 80, 205, 410
    logo_h = draw_logo(c, assets['logo_black'], x + 48, y + 48, w - 96)
    c.setStrokeColor(BLUE)
    c.setDash(5, 4)
    c.setLineWidth(1)
    c.roundRect(x, y, w, logo_h + 96, 16, fill=0, stroke=1)
    c.setDash()
    draw_text(c, 'x', x + 17, y + 18, 10, 'PW-Serif-Italic', BLUE)
    draw_text(c, 'x', x + w - 26, y + 18, 10, 'PW-Serif-Italic', BLUE)
    draw_label(c, 'Clear space = 1x', 80, 176)
    draw_paragraph(c, 'Jangan tempatkan teks, foto, garis, atau tepi bidang di dalam area putus-putus.', 80, 156, 410, 8.5, 13)
    rounded_box(c, 532, 205, 261, 190, IVORY, LINE, 20)
    draw_label(c, 'Ukuran minimum', 552, 363)
    draw_logo(c, assets['logo_black'], 552, 292, 155)
    draw_text(c, 'Digital  120 px', 552, 270, 8.2, 'PW-Sans-Bold', INK)
    draw_logo(c, assets['logo_black'], 552, 226, 105)
    draw_text(c, 'Cetak  28 mm', 552, 209, 8.2, 'PW-Sans-Bold', INK)
    rounded_box(c, 532, 78, 261, 105, BLUE_DEEP, None, 18)
    draw_label(c, 'Catatan', 552, 150, BLUE_SOFT)
    draw_paragraph(c, 'Jika detail wordmark mulai sulit dibaca, gunakan simbol mandiri dan pastikan nama merek hadir di konteks terdekat.', 552, 128, 220, 8.2, 12.5, 'PW-Sans', WHITE)
    page_footer(c, page)
    c.showPage()


def draw_backgrounds(c: canvas.Canvas, assets: dict[str, Path], page: int) -> None:
    c.setFillColor(IVORY)
    c.rect(0, 0, PAGE_W, PAGE_H, fill=1, stroke=0)
    page_title(c, '04 / BACKGROUNDS', 'Penggunaan pada latar', 'Utamakan kontras tinggi. Gunakan versi hitam pada bidang terang dan versi putih pada bidang gelap atau biru.')
    samples = [
        (44, 202, 360, 175, WHITE, assets['logo_black'], 'TERANG / LOGO HITAM'),
        (433, 202, 360, 175, INK, assets['logo_white'], 'GELAP / LOGO PUTIH'),
        (44, 63, 360, 112, BLUE, assets['logo_white'], 'BIRU / LOGO PUTIH'),
        (433, 63, 360, 112, BLUE_SOFT, assets['logo_black'], 'BIRU MUDA / LOGO HITAM'),
    ]
    for x, y, w, h, bg, logo, label in samples:
        rounded_box(c, x, y, w, h, bg, None, 20)
        logo_w = min(225, w * .62)
        im = Image.open(logo)
        logo_h = logo_w * im.height / im.width
        draw_logo(c, logo, x + (w - logo_w) / 2, y + (h - logo_h) / 2 + 4, logo_w)
        label_color = WHITE if bg in (INK, BLUE) else BLUE_DEEP
        draw_text(c, label, x + 16, y + 14, 6.4, 'PW-Sans-Bold', label_color)
    page_footer(c, page)
    c.showPage()


def draw_misuse(c: canvas.Canvas, assets: dict[str, Path], page: int) -> None:
    c.setFillColor(PAPER)
    c.rect(0, 0, PAGE_W, PAGE_H, fill=1, stroke=0)
    page_title(c, '05 / MISUSE', 'Hal yang harus dihindari', 'Konsistensi dibangun dari disiplin kecil. Jangan mengubah bentuk, proporsi, warna, atau keterbacaan logo.')
    labels = ['Jangan diregangkan', 'Jangan diputar', 'Jangan beri bayangan', 'Jangan gunakan warna acak', 'Jangan ubah jarak lockup', 'Jangan di atas latar ramai']
    x0, y0, gap_x, gap_y = 44, 78, 14, 14
    w = (PAGE_W - 88 - gap_x * 2) / 3
    h = 134
    for i, label in enumerate(labels):
        row, col = divmod(i, 3)
        x = x0 + col * (w + gap_x)
        y = y0 + (1 - row) * (h + gap_y)
        bg = WHITE if i != 5 else HexColor('#B3B7C3')
        rounded_box(c, x, y, w, h, bg, LINE, 18)
        c.saveState()
        if i == 1:
            c.translate(x + w / 2, y + 78)
            c.rotate(8)
            draw_logo(c, assets['logo_black'], -70, -17, 140)
        elif i == 0:
            c.drawImage(str(assets['logo_black']), x + 40, y + 60, width=w - 70, height=32, preserveAspectRatio=False, mask='auto')
        elif i == 2:
            c.setFillColor(Color(0, 0, 0, alpha=.22))
            c.roundRect(x + 48, y + 57, w - 90, 36, 12, fill=1, stroke=0)
            draw_logo(c, assets['logo_black'], x + 42, y + 64, w - 84)
        elif i == 3:
            c.setFillColor(HexColor('#BE2E8A'))
            c.roundRect(x + 36, y + 55, w - 72, 46, 12, fill=1, stroke=0)
            draw_logo(c, assets['logo_white'], x + 50, y + 67, w - 100)
        elif i == 4:
            draw_logo(c, assets['icon_black'], x + 38, y + 62, 45)
            draw_text(c, 'prasetya', x + 120, y + 78, 17, 'PW-Sans-Bold', INK)
        else:
            for j in range(6):
                c.setStrokeColor(HexColor('#5C6280'))
                c.line(x + 20, y + 46 + j * 12, x + w - 20, y + 95 - j * 5)
            draw_logo(c, assets['logo_black'], x + 50, y + 66, w - 100)
        c.restoreState()
        c.setStrokeColor(RED)
        c.setLineWidth(1.4)
        c.line(x + w - 28, y + h - 27, x + w - 14, y + h - 13)
        c.line(x + w - 14, y + h - 27, x + w - 28, y + h - 13)
        draw_text(c, label, x + 14, y + 13, 7.2, 'PW-Sans-Bold', INK)
    page_footer(c, page)
    c.showPage()


def draw_palette(c: canvas.Canvas, page: int) -> None:
    c.setFillColor(INK)
    c.rect(0, 0, PAGE_W, PAGE_H, fill=1, stroke=0)
    page_title(c, '06 / COLOR', 'Palet warna', 'Warna biru memberi aksen percaya diri. Hitam, ivory, dan putih menjaga tampilan tetap matang dan memberi ruang untuk konten.', dark=True)
    colors = [
        ('SIGNATURE BLUE', '#173A9B', 'RGB 23 58 155', 'CMYK 85 63 0 39', BLUE, WHITE),
        ('DEEP BLUE', '#0B2368', 'RGB 11 35 104', 'CMYK 89 66 0 59', BLUE_DEEP, WHITE),
        ('INK', '#11131A', 'RGB 17 19 26', 'CMYK 35 27 0 90', INK_2, WHITE),
        ('SOFT BLUE', '#D7E0FB', 'RGB 215 224 251', 'CMYK 14 11 0 2', BLUE_SOFT, INK),
        ('IVORY', '#F4F1EA', 'RGB 244 241 234', 'CMYK 0 1 4 4', IVORY, INK),
        ('PAPER', '#FFFDF8', 'RGB 255 253 248', 'CMYK 0 1 3 0', PAPER, INK),
    ]
    x0, y0, gap = 44, 78, 10
    w = (PAGE_W - 88 - gap * 5) / 6
    for i, (name, hexv, rgb, cmyk, bg, fg) in enumerate(colors):
        x = x0 + i * (w + gap)
        c.setFillColor(bg)
        c.roundRect(x, y0, w, 270, 17, fill=1, stroke=0)
        draw_text(c, name, x + 13, y0 + 235, 6.4, 'PW-Sans-Bold', fg)
        draw_text(c, hexv, x + 13, y0 + 58, 12, 'PW-Sans-Bold', fg)
        draw_text(c, rgb, x + 13, y0 + 37, 6.3, 'PW-Sans', fg)
        draw_text(c, cmyk, x + 13, y0 + 21, 6.3, 'PW-Sans', fg)
    draw_text(c, 'Gunakan Signature Blue untuk CTA dan aksen utama. Hindari memenuhi seluruh halaman dengan biru.', 44, 50, 7.4, 'PW-Sans', Color(1, 1, 1, alpha=.68))
    page_footer(c, page, dark=True)
    c.showPage()


def draw_typography(c: canvas.Canvas, page: int) -> None:
    c.setFillColor(PAPER)
    c.rect(0, 0, PAGE_W, PAGE_H, fill=1, stroke=0)
    page_title(c, '07 / TYPE', 'Tipografi', 'Perpaduan sans-serif yang bersih dan serif yang ekspresif menciptakan ritme modern tanpa kehilangan kehangatan.')
    rounded_box(c, 44, 212, 360, 180, WHITE, LINE, 20)
    draw_label(c, 'Primary / Arial', 64, 360)
    draw_text(c, 'Aa', 64, 285, 64, 'PW-Sans-Bold', INK)
    draw_text(c, 'ABCDEFGH  abcdefgh  0123456789', 64, 248, 9, 'PW-Sans', MUTED)
    draw_text(c, 'Navigasi, body copy, label, tombol', 64, 227, 7.4, 'PW-Sans-Bold', BLUE)
    rounded_box(c, 433, 212, 360, 180, IVORY, LINE, 20)
    draw_label(c, 'Editorial / Georgia', 453, 360)
    draw_text(c, 'Aa', 453, 285, 64, 'PW-Serif-Italic', BLUE)
    draw_text(c, 'ABCDEFGH  abcdefgh  0123456789', 453, 248, 9, 'PW-Serif', MUTED)
    draw_text(c, 'Headline, emphasis, editorial accent', 453, 227, 7.4, 'PW-Sans-Bold', BLUE)
    draw_label(c, 'Hierarchy example', 44, 175)
    draw_text(c, 'website berkualitas', 44, 134, 27, 'PW-Serif-Bold', INK)
    draw_text(c, 'untuk bisnis yang siap ', 44, 102, 24, 'PW-Serif', INK)
    x_offset = pdfmetrics.stringWidth('untuk bisnis yang siap ', 'PW-Serif', 24)
    draw_text(c, 'naik kelas.', 44 + x_offset, 102, 24, 'PW-Serif-Italic', BLUE)
    draw_paragraph(c, 'Gunakan sentence case. Jaga headline ringkas dan sisakan ruang putih yang cukup.', 44, 76, 470, 8.5, 13)
    rounded_box(c, 610, 65, 183, 105, BLUE, None, 17)
    draw_text(c, 'MULAI KONSULTASI  ↗', 628, 121, 7, 'PW-Sans-Bold', WHITE)
    draw_text(c, 'Label tombol', 628, 93, 7, 'PW-Sans', BLUE_SOFT)
    page_footer(c, page)
    c.showPage()


def draw_graphic_system(c: canvas.Canvas, assets: dict[str, Path], page: int) -> None:
    c.setFillColor(IVORY)
    c.rect(0, 0, PAGE_W, PAGE_H, fill=1, stroke=0)
    page_title(c, '08 / GRAPHIC SYSTEM', 'Elemen visual', 'Gunakan bentuk membulat, garis tipis, aksen biru, dan transisi lembut untuk menyatukan pengalaman dari layar ke layar.')
    rounded_box(c, 44, 183, 350, 205, WHITE, LINE, 28)
    draw_label(c, 'Rounded surfaces', 66, 354)
    rounded_box(c, 66, 257, 306, 68, IVORY, LINE, 18)
    draw_text(c, 'Konten utama', 84, 294, 12, 'PW-Serif', INK)
    draw_text(c, 'Radius konsisten 16-28 px', 84, 273, 7.4, 'PW-Sans', MUTED)
    c.setStrokeColor(BLUE)
    c.setLineWidth(2)
    c.arc(88, 204, 325, 270, 12, 145)
    draw_text(c, 'garis gestural', 66, 210, 7.2, 'PW-Sans-Bold', BLUE)
    rounded_box(c, 412, 183, 381, 205, INK, None, 28)
    draw_label(c, 'Layer & contrast', 434, 354, BLUE_SOFT)
    c.setFillColor(Color(1, 1, 1, alpha=.07))
    c.roundRect(434, 229, 337, 88, 20, fill=1, stroke=0)
    c.setFillColor(BLUE)
    c.roundRect(450, 246, 158, 48, 24, fill=1, stroke=0)
    draw_text(c, 'AKSI UTAMA  ↗', 473, 266, 7, 'PW-Sans-Bold', WHITE)
    c.setFillColor(Color(1, 1, 1, alpha=.13))
    c.circle(716, 271, 28, fill=1, stroke=0)
    draw_logo(c, assets['icon_white'], 697, 252, 38)
    rounded_box(c, 44, 65, 749, 93, BLUE_SOFT, None, 24)
    draw_label(c, 'Aturan komposisi', 66, 129, BLUE_DEEP)
    rules = ['Banyak ruang kosong', 'Satu aksen dominan', 'Kontras jelas', 'Gerak yang tenang']
    for i, rule in enumerate(rules):
        x = 66 + i * 176
        c.setFillColor(BLUE)
        c.circle(x + 6, 95, 6, fill=1, stroke=0)
        draw_text(c, rule, x + 18, 91, 8.2, 'PW-Sans-Bold', INK)
    page_footer(c, page)
    c.showPage()


def draw_imagery(c: canvas.Canvas, page: int) -> None:
    c.setFillColor(PAPER)
    c.rect(0, 0, PAGE_W, PAGE_H, fill=1, stroke=0)
    page_title(c, '09 / IMAGERY', 'Arah fotografi', 'Pilih gambar yang terasa arsitektural, terang-terarah, dan tenang. Foto harus membantu pesan, bukan sekadar mengisi ruang.')
    images = [ROOT / 'public/images/hero-studio-dark-v2.webp', ROOT / 'public/images/benefit-strategy.webp', ROOT / 'public/images/benefit-character-design.webp']
    widths = [360, 201, 201]
    x = 44
    for image_path, w in zip(images, widths):
        draw_image_cover(c, image_path, x, 164, w, 220, 20)
        x += w + 15
    draw_label(c, 'DO', 44, 133)
    draw_paragraph(c, 'Gunakan pencahayaan natural, komposisi bersih, nuansa studio atau arsitektur, dan warna yang mudah menyatu dengan overlay biru-gelap.', 44, 111, 350, 8.4, 13)
    draw_label(c, "DON'T", 433, 133, RED)
    draw_paragraph(c, 'Hindari stok foto yang terlalu generik, pose berlebihan, saturasi ekstrem, latar berantakan, atau visual yang tidak memiliki hubungan dengan pesan.', 433, 111, 360, 8.4, 13)
    page_footer(c, page)
    c.showPage()


def draw_voice(c: canvas.Canvas, page: int) -> None:
    c.setFillColor(INK)
    c.rect(0, 0, PAGE_W, PAGE_H, fill=1, stroke=0)
    page_title(c, '10 / VOICE', 'Bahasa merek', 'Terdengar percaya diri, spesifik, dan manusiawi. Hindari frasa generik yang bisa digunakan oleh merek apa pun.', dark=True)
    traits = [('Jelas', 'Kalimat pendek dan keputusan langsung.'), ('Tenang', 'Tidak memaksa atau menjanjikan berlebihan.'), ('Tajam', 'Menjelaskan manfaat dengan bukti dan konteks.'), ('Hangat', 'Bahasa mudah dipahami, bukan jargon internal.')]
    for i, (title, body) in enumerate(traits):
        x = 44 + (i % 2) * 382
        y = 265 - (i // 2) * 105
        rounded_box(c, x, y, 365, 88, Color(1, 1, 1, alpha=.06), Color(1, 1, 1, alpha=.12), 17)
        draw_text(c, title, x + 18, y + 52, 14, 'PW-Serif', WHITE)
        draw_paragraph(c, body, x + 18, y + 30, 320, 7.8, 12, 'PW-Sans', Color(1, 1, 1, alpha=.66))
    draw_label(c, 'Gunakan', 44, 119, BLUE_SOFT)
    draw_text(c, '“Website yang bekerja untuk tujuan bisnis Anda.”', 44, 91, 12, 'PW-Serif-Italic', WHITE)
    draw_label(c, 'Hindari', 433, 119, RED)
    draw_text(c, '“Solusi digital inovatif untuk masa depan.”', 433, 91, 12, 'PW-Serif-Italic', Color(1, 1, 1, alpha=.55))
    page_footer(c, page, dark=True)
    c.showPage()


def draw_applications(c: canvas.Canvas, assets: dict[str, Path], page: int) -> None:
    c.setFillColor(IVORY)
    c.rect(0, 0, PAGE_W, PAGE_H, fill=1, stroke=0)
    page_title(c, '11 / APPLICATION', 'Contoh penerapan', 'Gunakan sistem yang sama pada website, proposal, media sosial, dan materi presentasi agar pengalaman merek terasa utuh.')
    rounded_box(c, 44, 135, 472, 255, WHITE, LINE, 18)
    c.setFillColor(INK)
    c.roundRect(55, 147, 450, 229, 13, fill=1, stroke=0)
    c.setFillColor(Color(1, 1, 1, alpha=.09))
    c.rect(55, 349, 450, 27, fill=1, stroke=0)
    for i, dot in enumerate([RED, HexColor('#E2B144'), HexColor('#4DAF72')]):
        c.setFillColor(dot)
        c.circle(69 + i * 12, 362, 3, fill=1, stroke=0)
    draw_logo(c, assets['logo_white'], 75, 315, 102)
    draw_text(c, 'website berkualitas untuk', 76, 258, 23, 'PW-Serif-Bold', WHITE)
    draw_text(c, 'bisnis yang siap naik kelas.', 76, 226, 23, 'PW-Serif-Italic', BLUE_SOFT)
    c.setFillColor(BLUE)
    c.roundRect(76, 178, 150, 32, 16, fill=1, stroke=0)
    draw_text(c, 'MULAI KONSULTASI  ↗', 94, 190, 6.6, 'PW-Sans-Bold', WHITE)
    rounded_box(c, 538, 214, 255, 176, BLUE, None, 20)
    draw_logo(c, assets['icon_white'], 560, 326, 45)
    draw_text(c, 'desain yang', 560, 286, 21, 'PW-Serif', WHITE)
    draw_text(c, 'bekerja.', 560, 258, 22, 'PW-Serif-Italic', BLUE_SOFT)
    draw_text(c, '@prasetyawebworks', 560, 232, 6.8, 'PW-Sans-Bold', WHITE)
    rounded_box(c, 538, 67, 255, 128, WHITE, LINE, 20)
    draw_logo(c, assets['logo_black'], 558, 151, 95)
    draw_label(c, 'Project proposal', 558, 124)
    draw_text(c, 'Website redesign', 558, 96, 17, 'PW-Serif', INK)
    draw_text(c, 'Prepared for Client Name', 558, 78, 6.8, 'PW-Sans', MUTED)
    page_footer(c, page)
    c.showPage()


def draw_checklist(c: canvas.Canvas, assets: dict[str, Path], page: int) -> None:
    c.setFillColor(PAPER)
    c.rect(0, 0, PAGE_W, PAGE_H, fill=1, stroke=0)
    page_title(c, '12 / CHECKLIST', 'Sebelum dipublikasikan', 'Gunakan daftar ini untuk memastikan setiap materi tetap selaras dengan identitas Prasetya Webworks.')
    checks = ['Versi logo sesuai dengan kontras latar.', 'Clear space dan ukuran minimum terpenuhi.', 'Warna berasal dari palet resmi.', 'Arial dan Georgia digunakan sesuai hierarki.', 'Headline spesifik dan bebas frasa generik.', 'Foto terasa tenang, bersih, dan relevan.', 'Radius, garis, dan tombol konsisten.', 'Tampilan diperiksa pada desktop dan mobile.']
    x0, y0 = 44, 330
    for i, item in enumerate(checks):
        col, row = i // 4, i % 4
        x = x0 + col * 380
        y = y0 - row * 56
        c.setStrokeColor(BLUE)
        c.setLineWidth(1.2)
        c.roundRect(x, y - 5, 18, 18, 5, fill=0, stroke=1)
        draw_text(c, item, x + 30, y, 8.6, 'PW-Sans', INK)
    rounded_box(c, 44, 68, 749, 82, INK, None, 22)
    draw_logo(c, assets['logo_white'], 66, 93, 145)
    draw_text(c, 'Pertanyaan mengenai penggunaan identitas merek?', 280, 113, 11, 'PW-Serif', WHITE)
    draw_text(c, 'hello@prasetyawebworks.com', 280, 90, 8, 'PW-Sans-Bold', BLUE_SOFT)
    page_footer(c, page)
    c.showPage()


def generate() -> None:
    register_fonts()
    assets = prepare_assets()
    c = canvas.Canvas(str(PDF_PATH), pagesize=(PAGE_W, PAGE_H))
    c.setTitle('Prasetya Webworks Brand Guidelines')
    c.setAuthor('Prasetya Webworks')
    c.setSubject('Brand identity and usage guidelines')
    c.setCreator('Prasetya Webworks')
    draw_cover(c, assets)
    draw_foundation(c, assets, 2)
    draw_logo_system(c, assets, 3)
    draw_spacing(c, assets, 4)
    draw_backgrounds(c, assets, 5)
    draw_misuse(c, assets, 6)
    draw_palette(c, 7)
    draw_typography(c, 8)
    draw_graphic_system(c, assets, 9)
    draw_imagery(c, 10)
    draw_voice(c, 11)
    draw_applications(c, assets, 12)
    draw_checklist(c, assets, 13)
    c.save()
    print(PDF_PATH)


if __name__ == '__main__':
    generate()

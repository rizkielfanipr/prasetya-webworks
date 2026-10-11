from pathlib import Path

from PIL import Image, ImageDraw


files = sorted(Path('tmp/pdfs/rendered').glob('page-*.png'))
thumbs = []

for index, path in enumerate(files, 1):
    image = Image.open(path).convert('RGB')
    image.thumbnail((500, 354))
    card = Image.new('RGB', (520, 390), '#d9d9d9')
    card.paste(image, ((520 - image.width) // 2, 18))
    ImageDraw.Draw(card).text((12, 366), f'Page {index:02d}', fill='black')
    thumbs.append(card)

columns = 3
rows = (len(thumbs) + columns - 1) // columns
sheet = Image.new('RGB', (columns * 520, rows * 390), '#bcbcbc')

for index, image in enumerate(thumbs):
    sheet.paste(image, ((index % columns) * 520, (index // columns) * 390))

sheet.save('tmp/pdfs/brand-guidelines-contact-sheet.jpg', quality=88)

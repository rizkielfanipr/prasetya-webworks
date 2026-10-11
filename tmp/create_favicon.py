from pathlib import Path

from PIL import Image, ImageDraw


root = Path('/Users/air/Projects/prasetya-webworks')
source = Image.open(root / 'public/images/prasetya-webworks-logo.png').convert('RGBA')
visible = source.getchannel('A').getbbox()

if visible:
    source = source.crop(visible)

symbol = source.crop((0, 0, max(1, int(source.width * 0.255)), source.height))
symbol_box = symbol.getchannel('A').getbbox()

if symbol_box:
    symbol = symbol.crop(symbol_box)

white_symbol = Image.new('RGBA', symbol.size, (255, 255, 255, 0))
white_symbol.putalpha(symbol.getchannel('A'))
white_symbol.thumbnail((332, 332), Image.Resampling.LANCZOS)

favicon = Image.new('RGBA', (512, 512), (0, 0, 0, 0))
background = Image.new('RGBA', favicon.size, (0, 0, 0, 0))
ImageDraw.Draw(background).rounded_rectangle((24, 24, 488, 488), radius=132, fill='#173A9B')
favicon.alpha_composite(background)
favicon.alpha_composite(white_symbol, ((512 - white_symbol.width) // 2, (512 - white_symbol.height) // 2))

favicon.save(root / 'public/favicon.png', optimize=True)
favicon.save(root / 'public/apple-touch-icon.png', optimize=True)
favicon.save(root / 'public/favicon.ico', sizes=[(16, 16), (32, 32), (48, 48)])

# Build the Workshop preview (thumbnail.jpeg) from the original art (thumbnail.original.jpeg, by hhoangg,
# CC BY 4.0): cover the original "Co-op Synergies" title with a dark band and draw this fork's name.
# Always reads the original, so re-running never stamps a title twice. Needs Pillow.
#   python tools/make_thumbnail.py ["Title"]
import os
import sys

from PIL import Image, ImageDraw, ImageFont

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
SRC = os.path.join(ROOT, "thumbnail.original.jpeg")
OUT = os.path.join(ROOT, "thumbnail.jpeg")
TITLE = sys.argv[1] if len(sys.argv) > 1 else "Fixed Coop Synergies"
SIZE = 1024
BAND_TOP, BAND_SOLID = 760, 830   # fade from transparent at BAND_TOP to solid at BAND_SOLID (old title starts ~850)
INK, OUTLINE, RULE = (244, 234, 208), (13, 13, 18), (210, 187, 67)


def font(px):
    for name in ("arialbd.ttf", "Arial Bold.ttf", "DejaVuSans-Bold.ttf", "LiberationSans-Bold.ttf"):
        try:
            return ImageFont.truetype(name, px)
        except OSError:
            pass
    sys.exit("make_thumbnail: no bold TrueType font found")


art = Image.open(SRC).convert("RGB").resize((SIZE, SIZE))
band = Image.new("L", (SIZE, SIZE), 0)
draw_band = ImageDraw.Draw(band)
for y in range(BAND_TOP, SIZE):
    alpha = 255 if y >= BAND_SOLID else int(255 * (y - BAND_TOP) / (BAND_SOLID - BAND_TOP))
    draw_band.line([(0, y), (SIZE, y)], fill=alpha)
art = Image.composite(Image.new("RGB", (SIZE, SIZE), OUTLINE), art, band)

draw = ImageDraw.Draw(art)
px = 96
while True:   # largest size that fits with a 60px margin each side
    f = font(px)
    left, top, right, bottom = draw.textbbox((0, 0), TITLE, font=f, stroke_width=6)
    if right - left <= SIZE - 120 or px <= 40:
        break
    px -= 4
x = (SIZE - (right - left)) // 2 - left
y = 925 - (bottom - top) // 2 - top
draw.text((x, y), TITLE, font=f, fill=INK, stroke_width=6, stroke_fill=OUTLINE)
draw.rounded_rectangle([SIZE // 2 - 156, 990, SIZE // 2 + 156, 994], radius=2, fill=RULE)

art.save(OUT, "JPEG", quality=90, optimize=True)
print("make_thumbnail: wrote %s (%d KB, title %r, %dpx; Steam's cap is 1024 KB)"
      % (OUT, os.path.getsize(OUT) // 1024, TITLE, px))

# -*- coding: utf-8 -*-
from pathlib import Path
from PIL import Image, ImageDraw, ImageFilter

ROOT = Path(__file__).resolve().parents[1]
OUT = ROOT / "docs" / "skills" / "book" / "assets"
SRC = OUT / "_src"


def make_frame(size, outer, ring_colors, inner, glow=None):
    img = Image.new("RGBA", (size, size), (0, 0, 0, 0))
    d = ImageDraw.Draw(img)
    if glow:
        g = Image.new("RGBA", (size, size), (0, 0, 0, 0))
        gd = ImageDraw.Draw(g)
        gd.ellipse((4, 4, size - 5, size - 5), fill=glow)
        g = g.filter(ImageFilter.GaussianBlur(8))
        img = Image.alpha_composite(img, g)
        d = ImageDraw.Draw(img)
    d.ellipse((6, 6, size - 7, size - 7), fill=outer[0], outline=outer[1], width=5)
    d.ellipse((16, 16, size - 17, size - 17), fill=ring_colors[0], outline=ring_colors[1], width=3)
    d.ellipse((28, 28, size - 29, size - 29), fill=inner)
    return img


def cut_white_bg(im: Image.Image) -> Image.Image:
    """Treat near-white JPEG background as transparent."""
    im = im.convert("RGBA")
    px = im.load()
    w, h = im.size
    for y in range(h):
        for x in range(w):
            r, g, b, a = px[x, y]
            if r > 245 and g > 245 and b > 245:
                px[x, y] = (r, g, b, 0)
            elif r > 230 and g > 230 and b > 230:
                # soft edge
                px[x, y] = (r, g, b, max(0, 255 - (r + g + b - 690) * 8))
    return im


def place_sword(frame, sword_path, scale=0.78):
    sword = cut_white_bg(Image.open(sword_path))
    w, h = sword.size
    nw = int(frame.size[0] * scale)
    nh = int(h * nw / w)
    sword = sword.resize((nw, nh), Image.Resampling.LANCZOS)
    x = (frame.size[0] - nw) // 2
    y = (frame.size[1] - nh) // 2 - 2
    out = frame.copy()
    out.alpha_composite(sword, (x, y))
    return out


def main():
    OUT.mkdir(parents=True, exist_ok=True)
    frame_u = make_frame(
        256,
        outer=((26, 18, 8, 255), (240, 210, 120, 255)),
        ring_colors=((212, 160, 23, 255), (255, 241, 176, 255)),
        inner=(36, 24, 12, 255),
    )
    unlocked = place_sword(frame_u, SRC / "sword-cartoon-copper.jpg")
    unlocked.save(OUT / "node-unlocked.png")

    frame_a = make_frame(
        256,
        outer=((7, 20, 16, 255), (157, 255, 208, 255)),
        ring_colors=((47, 155, 120, 255), (233, 255, 245, 255)),
        inner=(11, 34, 27, 255),
        glow=(125, 255, 178, 90),
    )
    active = place_sword(frame_a, SRC / "sword-cartoon-jade.jpg")
    active.save(OUT / "node-active.png")
    print("ok", OUT / "node-unlocked.png", OUT / "node-active.png")


if __name__ == "__main__":
    main()

#!/usr/bin/env python3
"""Generate an Easter-themed social post for EMETIX Focus."""

from __future__ import annotations

import math
import random
from pathlib import Path

from PIL import Image, ImageDraw, ImageFilter, ImageFont
import arabic_reshaper
from bidi.algorithm import get_display


WIDTH = 1080
HEIGHT = 1350
OUTPUT_PATH = Path("/workspace/social_media_designs/easter_emetix_focus_post.png")


def ar_text(text: str) -> str:
    """Return Arabic text with proper shaping and bidi order."""
    return get_display(arabic_reshaper.reshape(text))


def rounded_rect(draw: ImageDraw.ImageDraw, box, radius, fill, outline=None, width=1):
    draw.rounded_rectangle(box, radius=radius, fill=fill, outline=outline, width=width)


def draw_background(canvas: Image.Image) -> None:
    draw = ImageDraw.Draw(canvas)
    top = (255, 250, 238)
    bottom = (235, 244, 255)
    for y in range(HEIGHT):
        t = y / (HEIGHT - 1)
        color = tuple(int(top[i] * (1 - t) + bottom[i] * t) for i in range(3))
        draw.line([(0, y), (WIDTH, y)], fill=color)

    # Subtle decorative egg outlines.
    rng = random.Random(42)
    for _ in range(22):
        w = rng.randint(80, 170)
        h = int(w * 1.25)
        x = rng.randint(-40, WIDTH - 30)
        y = rng.randint(40, HEIGHT - 60)
        c = rng.choice([(216, 202, 246, 80), (198, 226, 244, 80), (245, 212, 220, 80)])
        overlay = Image.new("RGBA", (WIDTH, HEIGHT), (0, 0, 0, 0))
        od = ImageDraw.Draw(overlay)
        od.ellipse((x, y, x + w, y + h), outline=c, width=4)
        canvas.alpha_composite(overlay)


def draw_egg(canvas: Image.Image, center_x: int, center_y: int, w: int, color: tuple[int, int, int]) -> None:
    h = int(w * 1.25)
    egg = Image.new("RGBA", (w + 20, h + 20), (0, 0, 0, 0))
    d = ImageDraw.Draw(egg)
    d.ellipse((10, 10, 10 + w, 10 + h), fill=color, outline=(255, 255, 255, 230), width=4)

    # Stripe + dot pattern
    for i in range(4):
        yy = 22 + i * (h // 4)
        d.arc((16, yy, w + 4, yy + 24), 0, 180, fill=(255, 255, 255, 180), width=3)
    for i in range(7):
        x = 24 + (i % 4) * (w // 4)
        y = 45 + (i // 4) * (h // 3)
        d.ellipse((x, y, x + 10, y + 10), fill=(255, 255, 255, 190))

    canvas.alpha_composite(egg, (center_x - (w + 20) // 2, center_y - (h + 20) // 2))


def draw_ribbon(draw: ImageDraw.ImageDraw, font_ar_bold: ImageFont.FreeTypeFont) -> None:
    ribbon_h = 120
    rounded_rect(draw, (48, 38, WIDTH - 48, 38 + ribbon_h), 36, fill=(120, 96, 186, 245))
    txt = ar_text("تصميم خاص لعيد الفصح")
    bbox = draw.textbbox((0, 0), txt, font=font_ar_bold)
    tx = (WIDTH - (bbox[2] - bbox[0])) // 2
    ty = 38 + (ribbon_h - (bbox[3] - bbox[1])) // 2 - 3
    draw.text((tx, ty), txt, font=font_ar_bold, fill=(255, 255, 255))


def draw_product_pack(
    canvas: Image.Image,
    draw: ImageDraw.ImageDraw,
    font_en_bold: ImageFont.FreeTypeFont,
    font_en: ImageFont.FreeTypeFont,
) -> tuple[int, int, int, int]:
    # Drop shadow
    pack_box = (110, 535, 420, 1070)
    shadow = Image.new("RGBA", (WIDTH, HEIGHT), (0, 0, 0, 0))
    sd = ImageDraw.Draw(shadow)
    rounded_rect(sd, (pack_box[0] + 12, pack_box[1] + 16, pack_box[2] + 12, pack_box[3] + 16), 26, fill=(0, 0, 0, 105))
    shadow = shadow.filter(ImageFilter.GaussianBlur(10))
    canvas.alpha_composite(shadow)

    rounded_rect(draw, pack_box, 28, fill=(247, 211, 37), outline=(25, 37, 91), width=6)
    # top notch look
    draw.polygon(
        [
            (pack_box[0], pack_box[1] + 24),
            (pack_box[0] + 26, pack_box[1] + 6),
            (pack_box[2] - 26, pack_box[1] + 6),
            (pack_box[2], pack_box[1] + 24),
        ],
        fill=(240, 201, 25),
    )

    draw.text((145, 605), "EMETIX", font=font_en_bold, fill=(25, 37, 91))
    draw.text((145, 690), "Focus", font=font_en_bold, fill=(25, 37, 91))
    draw.line((145, 780, 385, 780), fill=(25, 37, 91), width=4)
    draw.text((145, 810), "For Better", font=font_en, fill=(40, 40, 40))
    draw.text((145, 848), "Attention & Focus", font=font_en, fill=(40, 40, 40))
    draw.text((360, 1010), "6g", font=font_en, fill=(25, 37, 91))

    # Tiny icon row
    for i, symbol in enumerate(["\u25ce", "\u2605", "\u2726"]):
        draw.text((160 + i * 62, 942), symbol, font=font_en_bold, fill=(25, 37, 91))

    return pack_box


def draw_content(
    draw: ImageDraw.ImageDraw,
    font_ar_bold: ImageFont.FreeTypeFont,
    font_ar: ImageFont.FreeTypeFont,
    font_en_bold: ImageFont.FreeTypeFont,
):
    l1 = ar_text("خليك مركز في عيد الفصح")
    l2 = ar_text("واستمتع بكل لحظة مع EMETIX Focus")
    l3 = ar_text("تركيز يدوم خلال الزيارات والاحتفالات")

    x_base = 980
    y = 245
    for line, font, color in [
        (l1, font_ar_bold, (21, 36, 88)),
        (l2, font_ar_bold, (21, 36, 88)),
        (l3, font_ar, (52, 70, 133)),
    ]:
        bbox = draw.textbbox((0, 0), line, font=font)
        w = bbox[2] - bbox[0]
        draw.text((x_base - w, y), line, font=font, fill=color)
        y += (bbox[3] - bbox[1]) + 20

    # English subtitle
    draw.text((508, 530), "EASTER SPECIAL", font=font_en_bold, fill=(120, 96, 186))


def draw_badge(
    draw: ImageDraw.ImageDraw, canvas: Image.Image, font_ar_bold: ImageFont.FreeTypeFont, cx: int, cy: int
) -> None:
    r = 96
    overlay = Image.new("RGBA", (WIDTH, HEIGHT), (0, 0, 0, 0))
    d = ImageDraw.Draw(overlay)
    d.ellipse((cx - r, cy - r, cx + r, cy + r), fill=(30, 52, 119, 245), outline=(252, 220, 90, 255), width=8)

    for i in range(18):
        a = 2 * math.pi * i / 18
        x1 = cx + int((r + 6) * math.cos(a))
        y1 = cy + int((r + 6) * math.sin(a))
        x2 = cx + int((r + 16) * math.cos(a))
        y2 = cy + int((r + 16) * math.sin(a))
        d.line((x1, y1, x2, y2), fill=(252, 220, 90, 220), width=3)

    canvas.alpha_composite(overlay)

    t1 = ar_text("مفعول خلال")
    t2 = ar_text("15 دقيقة")
    b1 = draw.textbbox((0, 0), t1, font=font_ar_bold)
    b2 = draw.textbbox((0, 0), t2, font=font_ar_bold)
    draw.text((cx - (b1[2] - b1[0]) // 2, cy - 30), t1, font=font_ar_bold, fill=(255, 255, 255))
    draw.text((cx - (b2[2] - b2[0]) // 2, cy + 10), t2, font=font_ar_bold, fill=(255, 240, 173))


def draw_cta(draw: ImageDraw.ImageDraw, font_ar_bold: ImageFont.FreeTypeFont) -> None:
    box = (120, 1180, WIDTH - 120, 1290)
    rounded_rect(draw, box, radius=52, fill=(214, 40, 40), outline=(255, 255, 255), width=6)
    txt = ar_text("اطلبه الآن واستعد لعيد الفصح")
    bbox = draw.textbbox((0, 0), txt, font=font_ar_bold)
    tx = (WIDTH - (bbox[2] - bbox[0])) // 2
    ty = (box[1] + box[3] - (bbox[3] - bbox[1])) // 2 - 4
    draw.text((tx, ty), txt, font=font_ar_bold, fill=(255, 255, 255))


def load_fonts():
    arabic_bold = "/usr/share/fonts/truetype/noto/NotoSansArabic-Bold.ttf"
    arabic_regular = "/usr/share/fonts/truetype/noto/NotoSansArabic-Regular.ttf"
    latin_bold = "/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf"
    latin_regular = "/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf"
    return {
        "ar_bold_54": ImageFont.truetype(arabic_bold, 54),
        "ar_bold_44": ImageFont.truetype(arabic_bold, 44),
        "ar_bold_36": ImageFont.truetype(arabic_bold, 36),
        "ar_regular_34": ImageFont.truetype(arabic_regular, 34),
        "en_bold_72": ImageFont.truetype(latin_bold, 72),
        "en_bold_44": ImageFont.truetype(latin_bold, 44),
        "en_bold_34": ImageFont.truetype(latin_bold, 34),
        "en_30": ImageFont.truetype(latin_regular, 30),
    }


def main() -> None:
    OUTPUT_PATH.parent.mkdir(parents=True, exist_ok=True)
    fonts = load_fonts()

    canvas = Image.new("RGBA", (WIDTH, HEIGHT), (255, 255, 255, 255))
    draw_background(canvas)
    draw = ImageDraw.Draw(canvas)

    draw_ribbon(draw, fonts["ar_bold_44"])

    draw_egg(canvas, 930, 890, 120, (255, 186, 198))
    draw_egg(canvas, 860, 990, 110, (191, 225, 255))
    draw_egg(canvas, 965, 1080, 95, (216, 201, 255))
    draw_egg(canvas, 780, 1100, 80, (255, 230, 170))

    pack_box = draw_product_pack(canvas, draw, fonts["en_bold_72"], fonts["en_30"])
    draw_content(draw, fonts["ar_bold_54"], fonts["ar_regular_34"], fonts["en_bold_34"])
    draw_badge(draw, canvas, fonts["ar_bold_36"], cx=445, cy=760)
    draw_cta(draw, fonts["ar_bold_44"])

    # Small sparkles near product.
    for p in [(500, 700), (545, 1000), (760, 820)]:
        draw.text((p[0], p[1]), "✦", font=fonts["en_bold_44"], fill=(252, 212, 77))
        draw.text((p[0] + 18, p[1] + 22), "✧", font=fonts["en_bold_34"], fill=(120, 96, 186))

    # Soft vignette for focus.
    vignette = Image.new("RGBA", (WIDTH, HEIGHT), (0, 0, 0, 0))
    vd = ImageDraw.Draw(vignette)
    vd.rectangle((0, 0, WIDTH, HEIGHT), fill=(255, 255, 255, 0))
    for i in range(12):
        alpha = int(6 + i * 4)
        vd.rounded_rectangle((i * 2, i * 2, WIDTH - i * 2, HEIGHT - i * 2), 44, outline=(255, 255, 255, alpha), width=3)
    canvas.alpha_composite(vignette)

    canvas.convert("RGB").save(OUTPUT_PATH, quality=95)
    print(f"Created: {OUTPUT_PATH}")
    print(f"Product pack area: {pack_box}")


if __name__ == "__main__":
    main()

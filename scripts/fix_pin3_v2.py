#!/usr/bin/env python3
"""Fix Pin 3 (celebration) v2 — better vertical fill and text contrast."""

from PIL import Image, ImageDraw, ImageFont
import os, random

TPA_PATH = "/sessions/exciting-charming-clarke/mnt/the-period-academy"
LOGO_PATH = f"{TPA_PATH}/public/brand/logo-with-url-white.png"
OUT_DIR = f"{TPA_PATH}/public/pinterest"
PREVIEW_DIR = "/sessions/exciting-charming-clarke/mnt/Claude"

PERIWINKLE    = (120, 139, 255)
HARD_PINK     = (232, 66, 93)
SOFT_PINK     = (247, 180, 193)
WHITE         = (255, 255, 255)
SLATE_BLUE    = (137, 141, 170)
SOFT_YELLOW   = (255, 251, 120)
ELECTRIC_BLUE = (120, 209, 255)
TANGERINE     = (255, 224, 120)

W, H = 1000, 1500

def get_font(size, bold=False):
    bold_paths = [
        "/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf",
        "/usr/share/fonts/truetype/liberation/LiberationSans-Bold.ttf",
    ]
    reg_paths = [
        "/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf",
        "/usr/share/fonts/truetype/liberation/LiberationSans-Regular.ttf",
    ]
    paths = bold_paths if bold else reg_paths
    for p in paths:
        if os.path.exists(p):
            return ImageFont.truetype(p, size)
    return ImageFont.load_default()

def paste_logo(img, bg_color, y_top=0, logo_w=320):
    logo = Image.open(LOGO_PATH).convert("RGBA")
    logo_h = int(logo.height * logo_w / logo.width)
    band_h = logo_h + 30
    draw = ImageDraw.Draw(img)
    draw.rectangle([0, y_top, W, y_top + band_h], fill=bg_color)
    logo = logo.resize((logo_w, logo_h), Image.LANCZOS)
    logo_x = (W - logo_w) // 2
    logo_y = y_top + 15
    img.paste(logo, (logo_x, logo_y), logo)
    return y_top + band_h

def tw(draw, text, font):
    bb = draw.textbbox((0, 0), text, font=font)
    return bb[2] - bb[0]

def th(draw, text, font):
    bb = draw.textbbox((0, 0), text, font=font)
    return bb[3] - bb[1]

def draw_wrapped_centered(draw, text, cx, y, max_w, font, fill, line_spacing=10):
    words = text.split()
    lines = []
    cur = []
    for word in words:
        test = " ".join(cur + [word])
        bb = draw.textbbox((0, 0), test, font=font)
        if bb[2] - bb[0] > max_w and cur:
            lines.append(" ".join(cur))
            cur = [word]
        else:
            cur.append(word)
    if cur:
        lines.append(" ".join(cur))
    y0 = y
    for line in lines:
        lw = tw(draw, line, font)
        draw.text((cx - lw // 2, y0), line, font=font, fill=fill)
        y0 += th(draw, line or "A", font) + line_spacing
    return y0


def make_pin3():
    img = Image.new("RGB", (W, H), TANGERINE)
    draw = ImageDraw.Draw(img)

    # Logo on Hard Pink band
    logo_bottom = paste_logo(img, HARD_PINK, y_top=0)

    # Confetti dots — spread across ENTIRE canvas (more toward bottom too)
    random.seed(77)
    confetti_colors = [PERIWINKLE, HARD_PINK, WHITE, SOFT_PINK, ELECTRIC_BLUE]
    for _ in range(80):
        cx3 = random.randint(0, W)
        cy3 = random.randint(logo_bottom, H - 70)
        r = random.randint(4, 16)
        color = random.choice(confetti_colors)
        draw.ellipse([cx3 - r, cy3 - r, cx3 + r, cy3 + r], fill=color)

    # Hard Pink inset border
    margin = 30
    draw.rounded_rectangle([margin, logo_bottom + 20, W - margin, H - margin],
                            radius=24, outline=HARD_PINK, width=9)

    # Soft Yellow stars as decoration (top area)
    star_font = get_font(80, bold=True)
    star_y = logo_bottom + 55
    star_text = "★"
    # Left star in Soft Yellow
    draw.text((160, star_y), star_text, font=star_font, fill=SOFT_YELLOW)
    # Right star in Periwinkle
    draw.text((W - 160 - tw(draw, star_text, star_font), star_y), star_text, font=star_font, fill=PERIWINKLE)

    # ── LARGE HARD PINK background box for main message
    box_y = logo_bottom + 185
    box_h = 280
    draw.rectangle([48, box_y, W - 48, box_y + box_h], fill=HARD_PINK)

    # Main message — WHITE on Hard Pink box
    main_font = get_font(80, bold=True)
    msg_lines = ["Period confidence", "starts at home."]
    msg_y = box_y + 24
    for line in msg_lines:
        lw2 = tw(draw, line, main_font)
        draw.text(((W - lw2) // 2, msg_y), line, font=main_font, fill=WHITE)
        msg_y += th(draw, line, main_font) + 12

    content_y = box_y + box_h + 50

    # "YOU'VE GOT THIS." — Periwinkle, big centered
    got_font = get_font(84, bold=True)
    got_text = "YOU\u2019VE GOT THIS."
    gw = tw(draw, got_text, got_font)
    draw.text(((W - gw) // 2, content_y), got_text, font=got_font, fill=PERIWINKLE)
    content_y += th(draw, got_text, got_font) + 35

    # Soft Yellow thick rule
    draw.rectangle([120, content_y, W - 120, content_y + 8], fill=SOFT_YELLOW)
    content_y += 40

    # Secondary message — Hard Pink text (visible on Tangerine)
    sec_font = get_font(38, bold=True)
    sec_text = "Every parent who has this conversation is making the world a little less awkward for the next generation."
    draw_wrapped_centered(draw, sec_text, W // 2, content_y, W - 140, sec_font, HARD_PINK, line_spacing=12)

    # Large Periwinkle ellipse arc in bottom-right as decorative element
    draw.ellipse([680, H - 320, 1020, H - (-10)], fill=PERIWINKLE)
    draw.ellipse([700, H - 300, 1000, H + 10], fill=TANGERINE)

    # URL bar — Periwinkle with Hard Pink text
    draw.rectangle([0, H - 60, W, H], fill=PERIWINKLE)
    url_font = get_font(34, bold=True)
    url_text = "theperiodacademy.com"
    uw = tw(draw, url_text, url_font)
    draw.text(((W - uw) // 2, H - 50), url_text, font=url_font, fill=HARD_PINK)

    fname = "pin-celebration-period-confidence-20260312.png"
    img.save(f"{OUT_DIR}/{fname}")
    img.save(f"{PREVIEW_DIR}/{fname}")
    print(f"✅ Pin 3 v2 saved: {fname}")
    return fname

if __name__ == "__main__":
    make_pin3()

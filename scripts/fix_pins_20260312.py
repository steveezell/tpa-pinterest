#!/usr/bin/env python3
"""Fix Pin 2 (quote-pull) and Pin 3 (celebration) for 2026-03-12."""

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

def draw_wrapped(draw, text, x, y, max_w, font, fill, line_spacing=10):
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
        draw.text((x, y0), line, font=font, fill=fill)
        y0 += th(draw, line or "A", font) + line_spacing
    return y0


# ─────────────────────────────────────────────
# PIN 2 FIXED: quote-pull — schools don't teach enough
# Redesign: full-canvas, fill lower half with additional context cards
# ─────────────────────────────────────────────
def make_pin2():
    img = Image.new("RGB", (W, H), PERIWINKLE)
    draw = ImageDraw.Draw(img)

    # Logo band
    logo_bottom = paste_logo(img, PERIWINKLE, y_top=0)

    # ── Slate Blue diagonal header zone behind quote
    diag_poly = [(0, logo_bottom), (W, logo_bottom), (W, logo_bottom + 350), (0, logo_bottom + 520)]
    draw.polygon(diag_poly, fill=SLATE_BLUE)

    # Label
    label_font = get_font(26, bold=True)
    label_text = "FROM THE PERIOD ACADEMY"
    lw = tw(draw, label_text, label_font)
    draw.text(((W - lw) // 2, logo_bottom + 22), label_text, font=label_font, fill=SOFT_YELLOW)

    # Big open quote mark
    qmark_font = get_font(110, bold=True)
    draw.text((44, logo_bottom + 50), "\u201C", font=qmark_font, fill=HARD_PINK)

    # Main quote text
    quote = "The most prepared kids are the ones whose parents took an active role — and it doesn't have to be hard or awkward. It just has to happen."
    q_font = get_font(46, bold=True)
    quote_y = logo_bottom + 175
    quote_end_y = draw_wrapped(draw, quote, 68, quote_y, W - 130, q_font, WHITE, line_spacing=12)

    # Close quote
    close_font = get_font(80, bold=True)
    draw.text((W - 90, quote_end_y - 30), "\u201D", font=close_font, fill=HARD_PINK)

    # Attribution
    attr_y = quote_end_y + 30
    draw.rectangle([80, attr_y, W - 80, attr_y + 4], fill=HARD_PINK)
    attr_y += 18
    attr_font = get_font(32, bold=True)
    attr_text = "— theperiodacademy.com"
    aw = tw(draw, attr_text, attr_font)
    draw.text(((W - aw) // 2, attr_y), attr_text, font=attr_font, fill=SOFT_PINK)
    attr_y += th(draw, attr_text, attr_font) + 55

    # ── 3 stat-style cards to fill the lower canvas
    stat_font = get_font(32, bold=True)
    stat_body_font = get_font(28)

    stats = [
        ("1 session.", "Most schools cover periods in a single 30-minute class. That's not enough."),
        ("No federal standard.", "Period education requirements vary by state — many have none at all."),
        ("You can fill the gap.", "Parents who take an active role raise more confident, prepared kids."),
    ]

    for stat_title, stat_body in stats:
        # Card background
        card_h = 130
        draw.rectangle([48, attr_y, W - 48, attr_y + card_h], fill=HARD_PINK)
        draw.rectangle([48, attr_y, 120, attr_y + card_h], fill=ELECTRIC_BLUE)
        # Stat title
        draw.text((130, attr_y + 16), stat_title, font=stat_font, fill=SOFT_YELLOW)
        title_h = th(draw, stat_title, stat_font)
        # Stat body
        draw_wrapped(draw, stat_body, 130, attr_y + 18 + title_h + 8, W - 190, stat_body_font, WHITE, line_spacing=6)
        attr_y += card_h + 18

    # Decorative Soft Pink circle bottom-right
    draw.ellipse([760, H - 340, 1040, H - 60], fill=SOFT_PINK)
    draw.ellipse([780, H - 320, 1020, H - 80], fill=PERIWINKLE)

    # Credential band
    cred_y = H - 130
    draw.rectangle([0, cred_y, W, cred_y + 70], fill=TANGERINE)
    cred_font = get_font(28, bold=True)
    cred_text = "Period Education by a Certified Nurse-Midwife"
    cw = tw(draw, cred_text, cred_font)
    draw.text(((W - cw) // 2, cred_y + 18), cred_text, font=cred_font, fill=HARD_PINK)

    # URL bar
    draw.rectangle([0, H - 60, W, H], fill=HARD_PINK)
    url_font = get_font(34, bold=True)
    url_text = "theperiodacademy.com"
    uw = tw(draw, url_text, url_font)
    draw.text(((W - uw) // 2, H - 50), url_text, font=url_font, fill=WHITE)

    fname = "pin-schools-period-education-quote-pull-20260312.png"
    img.save(f"{OUT_DIR}/{fname}")
    img.save(f"{PREVIEW_DIR}/{fname}")
    print(f"✅ Pin 2 fixed: {fname}")
    return fname


# ─────────────────────────────────────────────
# PIN 3 FIXED: celebration (standalone)
# Template D: Tangerine BG, wavy Hard Pink inset border, warm joyful layout
# No overlapping circle — use confetti + clean text composition
# ─────────────────────────────────────────────
def make_pin3():
    img = Image.new("RGB", (W, H), TANGERINE)
    draw = ImageDraw.Draw(img)

    # Logo on Hard Pink band
    logo_bottom = paste_logo(img, HARD_PINK, y_top=0)

    # Wavy-ish inset border using a series of rounded rectangles (scalloped effect)
    # Use layered rects slightly inset with HARD_PINK then TANGERINE to create border
    margin = 28
    border_w = 10
    # Outer border rect
    draw.rounded_rectangle([margin, logo_bottom + margin, W - margin, H - margin], radius=28, outline=HARD_PINK, width=border_w)
    # Inner dotted feel: add small HARD_PINK circles along the border edge
    # (simplified — just the corner arcs reinforce by adding dots at corners)
    for cx2, cy2 in [
        (margin + 28, logo_bottom + margin + 28),
        (W - margin - 28, logo_bottom + margin + 28),
        (margin + 28, H - margin - 28),
        (W - margin - 28, H - margin - 28),
    ]:
        draw.ellipse([cx2 - 14, cy2 - 14, cx2 + 14, cy2 + 14], fill=HARD_PINK)

    # Confetti dots (smaller, more varied) — keep within content area
    random.seed(99)
    confetti_colors = [PERIWINKLE, HARD_PINK, WHITE, SOFT_PINK, ELECTRIC_BLUE, SOFT_YELLOW]
    for _ in range(90):
        cx3 = random.randint(60, W - 60)
        cy3 = random.randint(logo_bottom + 60, H - 90)
        r = random.randint(5, 14)
        color = random.choice(confetti_colors)
        draw.ellipse([cx3 - r, cy3 - r, cx3 + r, cy3 + r], fill=color)

    # Large emoji-style celebration graphic — "🎉" rendered as text
    emoji_font = get_font(140, bold=True)
    emoji_y = logo_bottom + 80
    # Place a big party emoji or substitute with ★ + exclamation
    # Use text "★" as the celebration graphic in Soft Yellow
    star_text = "★"
    sw = tw(draw, star_text, emoji_font)
    draw.text(((W - sw) // 2 - 80, emoji_y), star_text, font=emoji_font, fill=SOFT_YELLOW)
    draw.text(((W - sw) // 2 + 80, emoji_y), star_text, font=emoji_font, fill=PERIWINKLE)

    # Main message — Periwinkle large bold centered
    main_font = get_font(82, bold=True)
    msg_lines = ["Period confidence", "starts at home."]
    msg_y = emoji_y + th(draw, star_text, emoji_font) + 40

    for line in msg_lines:
        lw2 = tw(draw, line, main_font)
        draw.text(((W - lw2) // 2, msg_y), line, font=main_font, fill=PERIWINKLE)
        msg_y += th(draw, line, main_font) + 16

    msg_y += 20

    # Hard Pink thick divider
    draw.rectangle([100, msg_y, W - 100, msg_y + 8], fill=HARD_PINK)
    msg_y += 38

    # "YOU'VE GOT THIS." — Hard Pink, smaller so it doesn't clip
    got_font = get_font(72, bold=True)
    got_text = "YOU\u2019VE GOT THIS."
    gw = tw(draw, got_text, got_font)
    draw.text(((W - gw) // 2, msg_y), got_text, font=got_font, fill=HARD_PINK)
    msg_y += th(draw, got_text, got_font) + 46

    # Secondary warm message in WHITE
    sec_font = get_font(34)
    sec_text = "Every parent who has this conversation is making the world a little less awkward for the next generation."
    draw_wrapped(draw, sec_text, 80, msg_y, W - 160, sec_font, WHITE, line_spacing=10)

    # URL bar — Periwinkle with Hard Pink text
    draw.rectangle([0, H - 60, W, H], fill=PERIWINKLE)
    url_font = get_font(34, bold=True)
    url_text = "theperiodacademy.com"
    uw = tw(draw, url_text, url_font)
    draw.text(((W - uw) // 2, H - 50), url_text, font=url_font, fill=HARD_PINK)

    fname = "pin-celebration-period-confidence-20260312.png"
    img.save(f"{OUT_DIR}/{fname}")
    img.save(f"{PREVIEW_DIR}/{fname}")
    print(f"✅ Pin 3 fixed: {fname}")
    return fname


if __name__ == "__main__":
    f2 = make_pin2()
    f3 = make_pin3()
    print("\nFixed pins saved.")

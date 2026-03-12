#!/usr/bin/env python3
"""Generate 3 TPA Pinterest pins for 2026-03-12."""

from PIL import Image, ImageDraw, ImageFont
import os, textwrap, random, math

# Paths
TPA_PATH = "/sessions/exciting-charming-clarke/mnt/the-period-academy"
LOGO_PATH = f"{TPA_PATH}/public/brand/logo-with-url-white.png"
OUT_DIR = f"{TPA_PATH}/public/pinterest"
PREVIEW_DIR = "/sessions/exciting-charming-clarke/mnt/Claude"
os.makedirs(OUT_DIR, exist_ok=True)
os.makedirs(PREVIEW_DIR, exist_ok=True)

# Brand colors
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
    """Try to get a reasonable system font."""
    bold_paths = [
        "/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf",
        "/usr/share/fonts/truetype/liberation/LiberationSans-Bold.ttf",
        "/usr/share/fonts/truetype/freefont/FreeSansBold.ttf",
    ]
    reg_paths = [
        "/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf",
        "/usr/share/fonts/truetype/liberation/LiberationSans-Regular.ttf",
        "/usr/share/fonts/truetype/freefont/FreeSans.ttf",
    ]
    paths = bold_paths if bold else reg_paths
    for p in paths:
        if os.path.exists(p):
            return ImageFont.truetype(p, size)
    return ImageFont.load_default()

def get_italic_font(size):
    italic_paths = [
        "/usr/share/fonts/truetype/dejavu/DejaVuSans-Oblique.ttf",
        "/usr/share/fonts/truetype/liberation/LiberationSans-Italic.ttf",
        "/usr/share/fonts/truetype/freefont/FreeSansOblique.ttf",
    ]
    for p in italic_paths:
        if os.path.exists(p):
            return ImageFont.truetype(p, size)
    return get_font(size)

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

def draw_text_wrapped(draw, text, x, y, max_width, font, fill, align="left", stroke_fill=None, stroke_width=0):
    """Draw wrapped text, return bottom y."""
    # Wrap manually
    words = text.split()
    lines = []
    current = []
    for word in words:
        test = " ".join(current + [word])
        bbox = draw.textbbox((0, 0), test, font=font)
        if bbox[2] - bbox[0] > max_width and current:
            lines.append(" ".join(current))
            current = [word]
        else:
            current.append(word)
    if current:
        lines.append(" ".join(current))

    for line in lines:
        if stroke_fill and stroke_width:
            draw.text((x, y), line, font=font, fill=fill, stroke_fill=stroke_fill, stroke_width=stroke_width, align=align)
        else:
            draw.text((x, y), line, font=font, fill=fill)
        bbox = draw.textbbox((0, 0), line, font=font)
        y += (bbox[3] - bbox[1]) + 8
    return y

def text_width(draw, text, font):
    bb = draw.textbbox((0, 0), text, font=font)
    return bb[2] - bb[0]

def text_height(draw, text, font):
    bb = draw.textbbox((0, 0), text, font=font)
    return bb[3] - bb[1]

# ─────────────────────────────────────────────
# PIN 1: tip-list — first-period-kit-what-to-include
# Template A with a Hard Pink left sidebar + large numbered layout
# ─────────────────────────────────────────────
def make_pin1():
    img = Image.new("RGB", (W, H), PERIWINKLE)
    draw = ImageDraw.Draw(img)

    # Logo band
    logo_bottom = paste_logo(img, PERIWINKLE, y_top=0)

    # Hard Pink left sidebar strip (full height, 18px wide)
    draw.rectangle([0, logo_bottom, 18, H], fill=HARD_PINK)

    # Decorative large Electric Blue circle (partially off right edge, behind content)
    cx, cy, cr = 880, logo_bottom + 280, 230
    draw.ellipse([cx - cr, cy - cr, cx + cr, cy + cr], fill=(120, 209, 255, 0))
    # Use a slightly muted version
    draw.ellipse([cx - cr, cy - cr, cx + cr, cy + cr], fill=(140, 220, 255))
    # Soft Pink smaller circle top-left area
    draw.ellipse([35, logo_bottom + 30, 35 + 110, logo_bottom + 30 + 110], fill=SOFT_PINK)

    # Headline zone — color block behind headline text
    headline_y = logo_bottom + 50
    headline_text = "5 Things Every Parent Should Know About First Period Kits"
    h_font = get_font(54, bold=True)

    # Wrap the headline to get its height
    words = headline_text.split()
    h_lines = []
    current = []
    for word in words:
        test = " ".join(current + [word])
        bb = draw.textbbox((0, 0), test, font=h_font)
        if bb[2] - bb[0] > 860 and current:
            h_lines.append(" ".join(current))
            current = [word]
        else:
            current.append(word)
    if current:
        h_lines.append(" ".join(current))

    line_h = text_height(draw, "Ay", h_font) + 10
    total_h_h = len(h_lines) * line_h + 24
    # Draw backdrop box
    draw.rectangle([28, headline_y - 10, W - 28, headline_y + total_h_h], fill=HARD_PINK)
    # Draw headline text in SOFT_PINK with outline
    cy2 = headline_y + 4
    for line in h_lines:
        draw.text((52, cy2), line, font=h_font, fill=SOFT_PINK, stroke_fill=HARD_PINK, stroke_width=0)
        cy2 += line_h

    content_y = headline_y + total_h_h + 35

    # 5 Tips with large Electric Blue numbers + white text
    tips = [
        ("Pads first, always.", "Start with regular and light pads — no pressure for tampons. Keep a few in her backpack."),
        ("A discreet pouch.", "A small cosmetics bag she can carry without feeling self-conscious. Simple and practical."),
        ("A spare pair of underwear.", "Accidents happen. One backup pair in her locker = instant confidence."),
        ("Skip the novelty items.", "Crystals and confetti don't help. The goal is normalcy, not a survival kit."),
        ("Education beats products.", "A prepared mind handles this better than any product. The conversation IS the kit."),
    ]

    num_font = get_font(72, bold=True)
    tip_title_font = get_font(36, bold=True)
    tip_body_font = get_font(30)

    for i, (title, body) in enumerate(tips):
        num_str = str(i + 1)
        num_w = text_width(draw, num_str, num_font)
        # Large number in Electric Blue
        draw.text((42, content_y - 8), num_str, font=num_font, fill=ELECTRIC_BLUE)
        # Tip title in SOFT_PINK
        draw.text((42 + num_w + 20, content_y + 4), title, font=tip_title_font, fill=SOFT_PINK)
        # Tip body in WHITE
        body_y = content_y + text_height(draw, title, tip_title_font) + 12
        draw_text_wrapped(draw, body, 42 + num_w + 20, body_y, W - 42 - num_w - 40, tip_body_font, WHITE)
        content_y = body_y + text_height(draw, body[:30], tip_body_font) * 2 + 30

    # Credential band (Tangerine)
    cred_y = H - 130
    draw.rectangle([0, cred_y, W, cred_y + 70], fill=TANGERINE)
    cred_font = get_font(28, bold=True)
    cred_text = "Period Education by a Certified Nurse-Midwife"
    cw = text_width(draw, cred_text, cred_font)
    draw.text(((W - cw) // 2, cred_y + 18), cred_text, font=cred_font, fill=HARD_PINK)

    # URL bar (Hard Pink)
    draw.rectangle([0, H - 60, W, H], fill=HARD_PINK)
    url_font = get_font(34, bold=True)
    url_text = "theperiodacademy.com"
    uw = text_width(draw, url_text, url_font)
    draw.text(((W - uw) // 2, H - 50), url_text, font=url_font, fill=WHITE)

    fname = "pin-first-period-kit-tip-list-20260312.png"
    img.save(f"{OUT_DIR}/{fname}")
    img.save(f"{PREVIEW_DIR}/{fname}")
    print(f"✅ Pin 1 saved: {fname}")
    return fname


# ─────────────────────────────────────────────
# PIN 2: quote-pull — why-schools-dont-teach-enough-about-periods
# Template A with diagonal color zone — bold asymmetric design
# ─────────────────────────────────────────────
def make_pin2():
    img = Image.new("RGB", (W, H), PERIWINKLE)
    draw = ImageDraw.Draw(img)

    # Logo band
    logo_bottom = paste_logo(img, PERIWINKLE, y_top=0)

    # Diagonal slash: dark Slate Blue zone in top-left quadrant going diagonally
    # Draw a polygon for the diagonal background area
    diag_poly = [(0, logo_bottom), (W, logo_bottom), (W, logo_bottom + 320), (0, logo_bottom + 480)]
    draw.polygon(diag_poly, fill=SLATE_BLUE)

    # "QUOTE" label over the slate zone
    label_font = get_font(26, bold=True)
    label_text = "FROM THE PERIOD ACADEMY"
    lw = text_width(draw, label_text, label_font)
    draw.text(((W - lw) // 2, logo_bottom + 28), label_text, font=label_font, fill=SOFT_YELLOW)

    # Large open-quote marks in Hard Pink
    quote_mark_font = get_font(130, bold=True)
    draw.text((48, logo_bottom + 55), "\u201C", font=quote_mark_font, fill=HARD_PINK)

    # The quote — large, centered, white text
    quote = "The most prepared kids are the ones whose parents took an active role — and it doesn't have to be hard or awkward. It just has to happen."
    q_font = get_font(44, bold=True)

    quote_y = logo_bottom + 200
    draw_text_wrapped(draw, quote, 70, quote_y, W - 140, q_font, WHITE)

    # Calculate where quote ends for placement of next elements
    words = quote.split()
    q_lines = []
    current = []
    for word in words:
        test = " ".join(current + [word])
        bb = draw.textbbox((0, 0), test, font=q_font)
        if bb[2] - bb[0] > W - 140 and current:
            q_lines.append(" ".join(current))
            current = [word]
        else:
            current.append(word)
    if current:
        q_lines.append(" ".join(current))
    q_end_y = quote_y + len(q_lines) * (text_height(draw, "A", q_font) + 8)

    # Close quote + attribution
    close_font = get_font(80, bold=True)
    draw.text((W - 100, q_end_y - 20), "\u201D", font=close_font, fill=HARD_PINK)

    attr_y = q_end_y + 50
    # Hard Pink horizontal rule
    draw.rectangle([80, attr_y, W - 80, attr_y + 4], fill=HARD_PINK)
    attr_y += 20
    attr_font = get_font(32, bold=True)
    attr_text = "— theperiodacademy.com"
    aw = text_width(draw, attr_text, attr_font)
    draw.text(((W - aw) // 2, attr_y), attr_text, font=attr_font, fill=SOFT_PINK)
    attr_y += text_height(draw, attr_text, attr_font) + 50

    # Subtext — from the article
    sub_font = get_font(33)
    sub_text = "Most schools cover periods in ONE 30-minute session. Your child deserves more than that."
    draw_text_wrapped(draw, sub_text, 70, attr_y, W - 140, sub_font, WHITE)

    # Decorative Electric Blue circle bottom-right
    draw.ellipse([700, H - 500, 1040, H - 160], fill=ELECTRIC_BLUE)
    # Overlay with Periwinkle to "knock it back"
    draw.ellipse([710, H - 490, 1030, H - 170], fill=PERIWINKLE)

    # Soft Pink small decorative circle bottom-left
    draw.ellipse([-30, H - 280, 130, H - 120], fill=SOFT_PINK)

    # Credential band (Tangerine)
    cred_y = H - 130
    draw.rectangle([0, cred_y, W, cred_y + 70], fill=TANGERINE)
    cred_font = get_font(28, bold=True)
    cred_text = "Period Education by a Certified Nurse-Midwife"
    cw = text_width(draw, cred_text, cred_font)
    draw.text(((W - cw) // 2, cred_y + 18), cred_text, font=cred_font, fill=HARD_PINK)

    # URL bar
    draw.rectangle([0, H - 60, W, H], fill=HARD_PINK)
    url_font = get_font(34, bold=True)
    url_text = "theperiodacademy.com"
    uw = text_width(draw, url_text, url_font)
    draw.text(((W - uw) // 2, H - 50), url_text, font=url_font, fill=WHITE)

    fname = "pin-schools-period-education-quote-pull-20260312.png"
    img.save(f"{OUT_DIR}/{fname}")
    img.save(f"{PREVIEW_DIR}/{fname}")
    print(f"✅ Pin 2 saved: {fname}")
    return fname


# ─────────────────────────────────────────────
# PIN 3: celebration (standalone)
# Template D: Tangerine BG, confetti-style dots, warm direct message
# ─────────────────────────────────────────────
def make_pin3():
    img = Image.new("RGB", (W, H), TANGERINE)
    draw = ImageDraw.Draw(img)

    # Logo on Hard Pink band
    logo_bottom = paste_logo(img, HARD_PINK, y_top=0)

    # Confetti-style small dots scattered across canvas
    random.seed(42)
    confetti_colors = [PERIWINKLE, HARD_PINK, WHITE, SOFT_PINK, ELECTRIC_BLUE]
    for _ in range(120):
        cx = random.randint(0, W)
        cy = random.randint(logo_bottom + 10, H - 70)
        r = random.randint(4, 18)
        color = random.choice(confetti_colors)
        draw.ellipse([cx - r, cy - r, cx + r, cy + r], fill=color)

    # Large background circle in Hard Pink (semi-translucent effect via layering)
    # Just a big faded ring
    big_cx, big_cy, big_r = 500, logo_bottom + 560, 340
    # Outer ring
    draw.ellipse([big_cx - big_r, big_cy - big_r, big_cx + big_r, big_cy + big_r], fill=HARD_PINK)
    draw.ellipse([big_cx - big_r + 22, big_cy - big_r + 22, big_cx + big_r - 22, big_cy + big_r - 22], fill=TANGERINE)

    # Main celebration message — in Periwinkle, bold, centered
    msg_font = get_font(80, bold=True)
    msg_lines = ["Period confidence", "starts at home."]

    msg_y = logo_bottom + 280
    for line in msg_lines:
        lw = text_width(draw, line, msg_font)
        draw.text(((W - lw) // 2, msg_y), line, font=msg_font, fill=PERIWINKLE)
        msg_y += text_height(draw, line, msg_font) + 14

    # Bold "YOU'VE GOT THIS." in Hard Pink, below circle zone
    got_font = get_font(90, bold=True)
    got_text = "YOU'VE GOT THIS."
    gw = text_width(draw, got_text, got_font)
    got_y = logo_bottom + 820
    draw.text(((W - gw) // 2, got_y), got_text, font=got_font, fill=HARD_PINK)

    # Secondary message in WHITE
    sec_font = get_font(36)
    sec_text = "Every parent who has this conversation is making the world a little less awkward for the next generation."
    sec_y = got_y + text_height(draw, got_text, got_font) + 40
    draw_text_wrapped(draw, sec_text, 70, sec_y, W - 140, sec_font, WHITE)

    # Soft Yellow accent dots as "sparkles" near the YOU'VE GOT THIS text
    for sx, sy in [(90, got_y + 20), (W - 90, got_y + 30), (70, got_y + 80), (W - 70, got_y + 70)]:
        draw.ellipse([sx - 10, sy - 10, sx + 10, sy + 10], fill=SOFT_YELLOW)

    # URL bar — Periwinkle with Hard Pink text
    draw.rectangle([0, H - 60, W, H], fill=PERIWINKLE)
    url_font = get_font(34, bold=True)
    url_text = "theperiodacademy.com"
    uw = text_width(draw, url_text, url_font)
    draw.text(((W - uw) // 2, H - 50), url_text, font=url_font, fill=HARD_PINK)

    fname = "pin-celebration-period-confidence-20260312.png"
    img.save(f"{OUT_DIR}/{fname}")
    img.save(f"{PREVIEW_DIR}/{fname}")
    print(f"✅ Pin 3 saved: {fname}")
    return fname


if __name__ == "__main__":
    f1 = make_pin1()
    f2 = make_pin2()
    f3 = make_pin3()
    print("\nAll 3 pins generated:")
    print(f"  1. {f1}  → tip-list (first period kit)")
    print(f"  2. {f2}  → quote-pull (schools/period ed)")
    print(f"  3. {f3}  → celebration (standalone)")

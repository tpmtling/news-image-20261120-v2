"""Newspaper front page for Friday 20 November 2026.

One 1024x1024 image that sums up the day's world news, styled as a
classic broadsheet front page. Deterministic: fixed layout and fonts,
no timestamps, no randomness.
"""
from PIL import Image, ImageDraw, ImageFont

W = 1024
H = 1024

PAPER = (247, 242, 231)
INK = (26, 23, 16)
SOFT = (84, 78, 64)
FAINT = (150, 142, 122)
RED = (179, 32, 42)
RULE = (26, 23, 16)

SANS = "/usr/share/fonts/truetype/noto/NotoSans-Regular.ttf"
SANS_B = "/usr/share/fonts/truetype/noto/NotoSans-Bold.ttf"
SERIF = "/usr/share/fonts/truetype/noto/NotoSerif-Regular.ttf"
SERIF_B = "/usr/share/fonts/truetype/noto/NotoSerif-Bold.ttf"
SERIF_K = "/usr/share/fonts/truetype/noto/NotoSerif-Black.ttf"


def font(path, size):
    return ImageFont.truetype(path, size)


def wrap(draw, text, fnt, max_w):
    words = text.split()
    lines = []
    cur = ""
    for w in words:
        trial = (cur + " " + w).strip()
        if draw.textlength(trial, font=fnt) <= max_w:
            cur = trial
        else:
            if cur:
                lines.append(cur)
            cur = w
    if cur:
        lines.append(cur)
    return lines


def draw_wrapped(draw, xy, text, fnt, fill, max_w, leading):
    x, y = xy
    for line in wrap(draw, text, fnt, max_w):
        draw.text((x, y), line, font=fnt, fill=fill)
        y += leading
    return y


def centered(draw, y, text, fnt, fill):
    w = draw.textlength(text, font=fnt)
    draw.text(((W - w) / 2, y), text, font=fnt, fill=fill)
    return y + fnt.size + 8


LEAD_HEAD = "World Court: Myanmar committed genocide against the Rohingya"
LEAD_BODY = (
    "THE HAGUE - The International Court of Justice ruled on Thursday "
    "that Myanmar committed genocide against the Rohingya during its "
    "2017 military operations, a historic judgment in the case brought "
    "by The Gambia. The court found the state responsible for killings, "
    "expulsions and destruction that drove hundreds of thousands to flee."
)

LEFT = [
    {
        "kicker": "CYCLONE AKVAN",
        "title": "Cyclone Akvan bears down on India's east coast",
        "body": (
            "More than 120,000 people were evacuated and dozens of "
            "trains cancelled as severe Cyclone Akvan neared landfall "
            "between Puri and Gopalpur on Friday afternoon."
        ),
    },
    {
        "kicker": "MIDDLE EAST",
        "title": "Riyadh skyscraper hit as Gulf war widens",
        "body": (
            "A Riyadh skyscraper was damaged and a tanker struck near "
            "Oman as Houthi missiles were intercepted; Qatar warned a "
            "Hormuz closure is now a global crisis."
        ),
    },
]

RIGHT = [
    {
        "kicker": "SHENZHEN SUMMIT",
        "title": "Trump, Xi and Putin issue 'Declaration Towards Peace'",
        "body": (
            "The three leaders called for UN reforms and talks to cut "
            "nuclear risks after their first trilateral summit, but "
            "delivered no breakthroughs on Ukraine or trade."
        ),
    },
    {
        "kicker": "BUSINESS",
        "title": "Anthropic prices IPO at $83, eyes $1.5 trillion value",
        "body": (
            "Anthropic set its IPO price at $83 a share, targeting a "
            "valuation above $1.5 trillion in one of the biggest "
            "listings of the AI era."
        ),
    },
]

BRIEFS = [
    "Trump unveils $17 billion of Southeast Asia deals for US firms",
    "Merz: Europe expects a seat at new Ukraine peace talks soon",
    "Kushner says Russia is open to NATO-style guarantees for Ukraine",
    "NASA's Voyager 1 phones home from a light-day away",
    "National Book Award for fiction goes to 'Paradiso 17'",
]


def story(draw, x, y, col_w, item):
    draw.text((x, y), item["kicker"], font=font(SANS_B, 15), fill=RED)
    y += 20
    y = draw_wrapped(draw, (x, y), item["title"], font(SERIF_B, 24), INK, col_w, 28)
    y += 3
    y = draw_wrapped(draw, (x, y), item["body"], font(SERIF, 17), SOFT, col_w, 22)
    return y


def main():
    img = Image.new("RGB", (W, H), PAPER)
    d = ImageDraw.Draw(img)
    margin = 54

    # masthead
    centered(d, 28, "THE WORLD TODAY", font(SERIF_K, 64), INK)
    d.line([(margin, 110), (W - margin, 110)], fill=RULE, width=5)
    d.line([(margin, 119), (W - margin, 119)], fill=RULE, width=1)
    dateline = "Friday, November 20, 2026  -  World Edition  -  One image, the whole day"
    centered(d, 128, dateline, font(SANS, 17), SOFT)
    d.line([(margin, 162), (W - margin, 162)], fill=RULE, width=1)

    # lead story
    y = 176
    d.text((margin, y), "THE HAGUE  -  WORLD COURT", font=font(SANS_B, 17), fill=RED)
    y += 27
    y = draw_wrapped(d, (margin, y), LEAD_HEAD, font(SERIF_K, 46), INK, W - 2 * margin, 52)
    y += 6
    y = draw_wrapped(d, (margin, y), LEAD_BODY, font(SERIF, 19), SOFT, W - 2 * margin, 27)
    y += 14
    d.line([(margin, y), (W - margin, y)], fill=RED, width=3)
    y += 14

    # two columns
    gap = 36
    col_w = (W - 2 * margin - gap) // 2
    left_x = margin
    right_x = margin + col_w + gap
    top = y
    ly = top
    for i, item in enumerate(LEFT):
        ly = story(d, left_x, ly, col_w, item)
        ly += 12
        if i == 0:
            d.line([(left_x, ly), (left_x + col_w, ly)], fill=FAINT, width=1)
            ly += 14
    ry = top
    for i, item in enumerate(RIGHT):
        ry = story(d, right_x, ry, col_w, item)
        ry += 12
        if i == 0:
            d.line([(right_x, ry), (right_x + col_w, ry)], fill=FAINT, width=1)
            ry += 14
    # vertical divider between the columns
    div_x = margin + col_w + gap // 2
    d.line([(div_x, top), (div_x, max(ly, ry))], fill=FAINT, width=1)
    y = max(ly, ry) + 2

    # briefs strip
    d.line([(margin, y), (W - margin, y)], fill=RULE, width=3)
    y += 10
    d.text((margin, y), "IN BRIEF", font=font(SANS_B, 17), fill=RED)
    y += 20
    for brief in BRIEFS:
        d.rectangle([margin + 4, y + 7, margin + 12, y + 15], fill=RED)
        y = draw_wrapped(d, (margin + 30, y), brief, font(SERIF, 18), INK, W - 2 * margin - 30, 22)
        y += 2

    # footer
    d.line([(margin, H - 46), (W - margin, H - 46)], fill=RULE, width=1)
    centered(d, H - 36, "THE WORLD TODAY  -  Friday, November 20, 2026", font(SANS, 15), SOFT)

    img.save("news_image.png", format="PNG", optimize=False)
    print("saved news_image.png", img.size)


if __name__ == "__main__":
    main()

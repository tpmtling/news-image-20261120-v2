"""Friday 20 November 2026, set as a classic newspaper front page.

This script draws THE WORLD TODAY for 20 November 2026: one
1024x1024 PNG, fully deterministic - the same fixed text, fonts and
geometry on every run, with no clock and no random numbers. main.py
copies the finished picture to /output/entry.png.
"""

from PIL import Image
from PIL import ImageDraw
from PIL import ImageFont

PAGE = (1024, 1024)
EDGE = 56
GAP = 34

PALETTE = {
    "paper": (247, 242, 231),
    "ink": (26, 23, 16),
    "grey": (84, 78, 64),
    "pale": (150, 142, 122),
    "red": (179, 32, 42),
}

FONT_FILES = {
    "sans": "/usr/share/fonts/truetype/noto/NotoSans-Regular.ttf",
    "sans-bold": "/usr/share/fonts/truetype/noto/NotoSans-Bold.ttf",
    "serif": "/usr/share/fonts/truetype/noto/NotoSerif-Regular.ttf",
    "serif-bold": "/usr/share/fonts/truetype/noto/NotoSerif-Bold.ttf",
    "serif-black": "/usr/share/fonts/truetype/noto/NotoSerif-Black.ttf",
}


def load(name, size):
    return ImageFont.truetype(FONT_FILES[name], size)


def split_lines(draw, text, font, width):
    words = text.split(" ")
    lines = []
    current = ""
    for word in words:
        candidate = word if not current else current + " " + word
        if draw.textlength(candidate, font=font) <= width:
            current = candidate
        else:
            lines.append(current)
            current = word
    if current:
        lines.append(current)
    return lines


def paragraph(draw, x, y, text, font, colour, width, leading):
    for line in split_lines(draw, text, font, width):
        draw.text((x, y), line, font=font, fill=colour)
        y += leading
    return y


def centred(draw, y, text, font, colour):
    width = draw.textlength(text, font=font)
    draw.text(((PAGE[0] - width) / 2, y), text, font=font, fill=colour)
    return y + font.size + 8


LEAD = {
    "flag": "THE HAGUE  -  WORLD COURT",
    "head": "World Court: Myanmar committed genocide against the Rohingya",
    "text": (
        "THE HAGUE - The International Court of Justice ruled on Thursday "
        "that Myanmar committed genocide against the Rohingya during its "
        "2017 military operations, a historic judgment in the case brought "
        "by The Gambia. The court found the state responsible for killings, "
        "expulsions and destruction that drove hundreds of thousands to flee."
    ),
}

COLUMNS = [
    [
        {
            "tag": "CYCLONE AKVAN",
            "head": "Cyclone Akvan bears down on India's east coast",
            "text": (
                "More than 120,000 people were evacuated and dozens of "
                "trains cancelled as severe Cyclone Akvan neared landfall "
                "between Puri and Gopalpur on Friday afternoon."
            ),
        },
        {
            "tag": "MIDDLE EAST",
            "head": "Riyadh skyscraper hit as Gulf war widens",
            "text": (
                "A Riyadh skyscraper was damaged and a tanker struck near "
                "Oman as Houthi missiles were intercepted; Qatar warned a "
                "Hormuz closure is now a global crisis."
            ),
        },
    ],
    [
        {
            "tag": "SHENZHEN SUMMIT",
            "head": "Trump, Xi and Putin issue 'Declaration Towards Peace'",
            "text": (
                "The three leaders called for UN reforms and talks to cut "
                "nuclear risks after their first trilateral summit, but "
                "delivered no breakthroughs on Ukraine or trade."
            ),
        },
        {
            "tag": "BUSINESS",
            "head": "Anthropic prices IPO at $83, eyes $1.5 trillion value",
            "text": (
                "Anthropic set its IPO price at $83 a share, targeting a "
                "valuation above $1.5 trillion in one of the biggest "
                "listings of the AI era."
            ),
        },
    ],
]

BRIEFS = [
    "Trump unveils $17 billion of Southeast Asia deals for US firms",
    "Merz: Europe expects a seat at new Ukraine peace talks soon",
    "Kushner says Russia is open to NATO-style guarantees for Ukraine",
    "NASA's Voyager 1 phones home from a light-day away",
    "National Book Award for fiction goes to 'Paradiso 17'",
]


def masthead(draw):
    centred(draw, 28, "THE WORLD TODAY", load("serif-black", 64), PALETTE["ink"])
    draw.line([(EDGE, 110), (PAGE[0] - EDGE, 110)], fill=PALETTE["ink"], width=5)
    draw.line([(EDGE, 119), (PAGE[0] - EDGE, 119)], fill=PALETTE["ink"], width=1)
    dateline = "Friday, November 20, 2026  -  World Edition  -  One image, the whole day"
    centred(draw, 128, dateline, load("sans", 17), PALETTE["grey"])
    draw.line([(EDGE, 162), (PAGE[0] - EDGE, 162)], fill=PALETTE["ink"], width=1)
    return 176


def lead_story(draw, y):
    draw.text((EDGE, y), LEAD["flag"], font=load("sans-bold", 17), fill=PALETTE["red"])
    y += 27
    y = paragraph(draw, EDGE, y, LEAD["head"], load("serif-black", 46),
                  PALETTE["ink"], PAGE[0] - 2 * EDGE, 52)
    y += 6
    y = paragraph(draw, EDGE, y, LEAD["text"], load("serif", 19),
                  PALETTE["grey"], PAGE[0] - 2 * EDGE, 27)
    y += 14
    draw.line([(EDGE, y), (PAGE[0] - EDGE, y)], fill=PALETTE["red"], width=3)
    return y + 18


def column_story(draw, x, y, width, item):
    draw.text((x, y), item["tag"], font=load("sans-bold", 15), fill=PALETTE["red"])
    y += 20
    y = paragraph(draw, x, y, item["head"], load("serif-bold", 24),
                  PALETTE["ink"], width, 28)
    y += 3
    y = paragraph(draw, x, y, item["text"], load("serif", 17),
                  PALETTE["grey"], width, 22)
    return y


def two_columns(draw, y):
    width = (PAGE[0] - 2 * EDGE - GAP) // 2
    left = EDGE
    right = EDGE + width + GAP
    top = y
    ends = []
    for x, stories in ((left, COLUMNS[0]), (right, COLUMNS[1])):
        cursor = top
        for position, item in enumerate(stories):
            cursor = column_story(draw, x, cursor, width, item)
            cursor += 12
            if position == 0:
                draw.line([(x, cursor), (x + width, cursor)],
                          fill=PALETTE["pale"], width=1)
                cursor += 14
        ends.append(cursor)
    divider = EDGE + width + GAP // 2
    draw.line([(divider, top), (divider, max(ends))], fill=PALETTE["pale"], width=1)
    return max(ends) + 2


def briefs_block(draw, y):
    draw.line([(EDGE, y), (PAGE[0] - EDGE, y)], fill=PALETTE["ink"], width=3)
    y += 10
    draw.text((EDGE, y), "IN BRIEF", font=load("sans-bold", 17), fill=PALETTE["red"])
    y += 20
    for brief in BRIEFS:
        draw.rectangle([EDGE + 4, y + 7, EDGE + 12, y + 15], fill=PALETTE["red"])
        y = paragraph(draw, EDGE + 30, y, brief, load("serif", 18),
                      PALETTE["ink"], PAGE[0] - 2 * EDGE - 30, 22)
        y += 2
    return y


def footer(draw):
    draw.line([(EDGE, PAGE[1] - 46), (PAGE[0] - EDGE, PAGE[1] - 46)],
              fill=PALETTE["ink"], width=1)
    centred(draw, PAGE[1] - 36, "THE WORLD TODAY  -  Friday, November 20, 2026",
            load("sans", 15), PALETTE["grey"])


def build():
    canvas = Image.new("RGB", PAGE, PALETTE["paper"])
    draw = ImageDraw.Draw(canvas)
    y = masthead(draw)
    y = lead_story(draw, y)
    y = two_columns(draw, y)
    briefs_block(draw, y)
    footer(draw)
    canvas.save("news_image.png")
    print("saved news_image.png", canvas.size)


if __name__ == "__main__":
    build()

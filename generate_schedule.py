from reportlab.lib.pagesizes import A4
from reportlab.lib import colors
from reportlab.lib.units import mm
from reportlab.pdfgen import canvas
from reportlab.lib.colors import HexColor, white, black
from reportlab.platypus import Paragraph, Frame
from reportlab.lib.styles import ParagraphStyle
from reportlab.lib.enums import TA_CENTER, TA_LEFT

OUTPUT_PATH = "/sessions/jolly-kind-sagan/mnt/routine_maker/daily_schedule.pdf"

# A4 dimensions
PAGE_W, PAGE_H = A4  # 595.27 x 841.89 pts

MARGIN_H = 8 * mm
MARGIN_V = 8 * mm

# Colors
MAGENTA     = HexColor("#3B6D11")   # olive green border/accent
LIGHT_ROSE  = HexColor("#EAF3DE")   # light olive fill for key cards
LIGHT_GRAY  = HexColor("#F5F5F5")   # fill for normal cards
CARD_BORDER = HexColor("#BDBDBD")   # normal border
TEXT_DARK   = HexColor("#212121")
TEXT_TIME   = HexColor("#27500A")   # dark olive for time
TITLE_COLOR = HexColor("#27500A")

# Key tasks (partial match)
KEY_KEYWORDS = ["wake up", "gym session", "deep-dive", "jogging", "dinner time"]

def is_key(task_desc):
    low = task_desc.lower()
    return any(k in low for k in KEY_KEYWORDS)

# Schedule data: (time_24, label, emoji)
schedule = [
    ("05:00",           "Wake Up Time",                                         "☀️"),
    ("05:05 – 05:45",   "Personal Hygiene\nBrush teeth · wash face · toilet · shave", "🪥"),
    ("05:45 – 06:00",   "Dress up for Gym\nWalk / cycle to gym",               "🎽"),
    ("06:00 – 07:00",   "Gym Session\nIntensive workout (see gym plan)",        "🏋️"),
    ("07:00 – 07:15",   "Walk back to Dorm",                                    "🚶"),
    ("07:15 – 07:30",   "Shower & Change\nFresh clothes on!",                   "🚿"),
    ("07:30 – 08:00",   "Prepare & Eat Breakfast\nEggs · milk · protein · fruits · salad", "🍳"),
    ("08:00 – 08:15",   "Pack Lunch Box\nSandwich / wrap / salad",              "🥪"),
    ("08:15 – 08:30",   "Pack Backpack\niPad · keyboard · mouse · headset · chargers", "🎒"),
    ("08:30 – 08:50",   "Walk / Cycle to Library\nJohn C. Hitt Library",       "🚴"),
    ("08:50 – 09:00",   "Arrive at Library\nFind quiet spot · settle in",      "📚"),
    ("09:00 – 12:00",   "Deep-Dive Time  (Morning)\nIntensive study · read · work on subjects", "🧠"),
    ("12:00 – 12:30",   "Lunch Break\nEat · relax · walk around",              "🥗"),
    ("12:30 – 15:00",   "Deep-Dive Time  (Afternoon)\nSubject 2 focus",        "🧠"),
    ("15:00 – 16:30",   "In-Classroom Lecture (Thursdays)\nor Extended Study Time", "🎓"),
    ("16:30 – 17:00",   "Walk Back to Dorm\nChange into casual clothes",       "👟"),
    ("17:00 – 17:30",   "Dinner Preparation\nCheck fridge · follow meal plan · note grocery needs", "🥘"),
    ("17:30 – 18:30",   "Jogging / Running Time\nTrack your route · stay consistent", "🏃"),
    ("18:30 – 19:00",   "Campus Exploration\nCycle / walk · discover cafes & new spots", "🌆"),
    ("19:00 – 20:00",   "Dinner Time\nEat the meal you prepared",              "🍽️"),
    ("20:00 – 20:15",   "Evening Stroll\nWalk around dorm · Neptune 157",      "🌙"),
    ("20:15 – 21:00",   "Free Time\nChess · checkers · scrabble · cards · Carrom", "🎲"),
    ("21:00",           "Lights Out — Sleep Well\n8 hours · consistent schedule every night", "😴"),
]

QUOTE = (
    '"Lost time is never found again."\n— Benjamin Franklin\n\n'
    'Every minute of your day is a brick in the foundation of your future. '
    'A disciplined routine is not a cage — it is the scaffold on which champions are built. '
    'Show up on time, every time. The world rewards those who respect the clock.'
)


def draw_page(c):
    c.setFillColor(white)
    c.rect(0, 0, PAGE_W, PAGE_H, fill=1, stroke=0)

    # ── Title ──────────────────────────────────────────────────────────────
    c.setFillColor(TITLE_COLOR)
    c.setFont("Helvetica-Bold", 15)
    c.drawCentredString(PAGE_W / 2, PAGE_H - MARGIN_V - 5*mm, "🎓  MY DAILY ROUTINE — UNIVERSITY LIFE")
    c.setFont("Helvetica", 8)
    c.setFillColor(HexColor("#757575"))
    c.drawCentredString(PAGE_W / 2, PAGE_H - MARGIN_V - 9*mm, "Stay disciplined · Stay consistent · Own your day")

    title_bottom = PAGE_H - MARGIN_V - 13 * mm

    # ── Quote block height estimate ─────────────────────────────────────
    QUOTE_BLOCK_H = 22 * mm

    # ── Available height for cards ──────────────────────────────────────
    avail_h = title_bottom - MARGIN_V - QUOTE_BLOCK_H - 4 * mm
    n = len(schedule)
    GAP = 1.2 * mm
    card_h = (avail_h - (n - 1) * GAP) / n

    usable_w = PAGE_W - 2 * MARGIN_H
    TIME_COL  = 30 * mm
    EMOJI_COL = 7  * mm
    LABEL_COL = usable_w - TIME_COL - EMOJI_COL - 4 * mm

    y = title_bottom

    for (time_str, label, emoji) in schedule:
        y -= card_h
        key = is_key(label)

        # Card fill
        fill_col = LIGHT_ROSE if key else LIGHT_GRAY
        border_col = MAGENTA if key else CARD_BORDER
        border_w = 1.5 if key else 0.6

        # Draw card rect
        c.setFillColor(fill_col)
        c.setStrokeColor(border_col)
        c.setLineWidth(border_w)
        c.roundRect(MARGIN_H, y, usable_w, card_h - 0.5*mm, 2*mm, fill=1, stroke=1)

        # Left accent bar for key tasks
        if key:
            c.setFillColor(MAGENTA)
            c.roundRect(MARGIN_H, y, 3*mm, card_h - 0.5*mm, 1*mm, fill=1, stroke=0)

        # Time
        c.setFillColor(TEXT_TIME if not key else MAGENTA)
        font_size_time = min(8.5, card_h * 0.38)
        c.setFont("Helvetica-Bold", font_size_time)
        time_x = MARGIN_H + (5 if key else 2) * mm
        c.drawString(time_x, y + (card_h - 0.5*mm) * 0.62, time_str)

        # Emoji
        c.setFont("Helvetica", min(9, card_h * 0.40))
        c.setFillColor(TEXT_DARK)
        emoji_x = MARGIN_H + TIME_COL
        c.drawString(emoji_x, y + (card_h - 0.5*mm) * 0.55, emoji)

        # Label (supports newline → two lines)
        lines = label.split("\n")
        label_x = MARGIN_H + TIME_COL + EMOJI_COL + 1.5 * mm
        if len(lines) == 1:
            fs = min(8.5, card_h * 0.38)
            c.setFont("Helvetica-Bold" if key else "Helvetica", fs)
            c.setFillColor(TEXT_DARK)
            c.drawString(label_x, y + (card_h - 0.5*mm) * 0.55, lines[0])
        else:
            fs1 = min(8.0, card_h * 0.36)
            fs2 = min(6.8, card_h * 0.30)
            c.setFont("Helvetica-Bold" if key else "Helvetica-Bold", fs1)
            c.setFillColor(TEXT_DARK)
            c.drawString(label_x, y + (card_h - 0.5*mm) * 0.70, lines[0])
            c.setFont("Helvetica-Oblique", fs2)
            c.setFillColor(HexColor("#555555"))
            c.drawString(label_x, y + (card_h - 0.5*mm) * 0.28, lines[1])

        y -= GAP

    # ── Quote block ─────────────────────────────────────────────────────
    quote_y = MARGIN_V
    c.setStrokeColor(MAGENTA)
    c.setLineWidth(0.8)
    c.setFillColor(HexColor("#FFF8E1"))
    c.roundRect(MARGIN_H, quote_y, usable_w, QUOTE_BLOCK_H - 1*mm, 2*mm, fill=1, stroke=1)

    # Use Paragraph + Frame for proper word-wrap inside the box
    pad = 4 * mm
    top_pad = 0.5          # px → pts (1px ≈ 0.75pt, but keep it literal as requested)
    frame_x = MARGIN_H + pad
    frame_y = quote_y + pad * 0.5
    frame_w = usable_w - 2 * pad
    frame_h = QUOTE_BLOCK_H - 2 * mm - top_pad

    quote_style = ParagraphStyle(
        "quote",
        fontName="Helvetica-BoldOblique",
        fontSize=7.5,
        leading=10,
        textColor=TITLE_COLOR,
        alignment=TA_CENTER,
        spaceAfter=2,
    )
    attr_style = ParagraphStyle(
        "attr",
        fontName="Helvetica-Oblique",
        fontSize=6.8,
        leading=9,
        textColor=HexColor("#3B6D11"),
        alignment=TA_CENTER,
        spaceAfter=3,
    )
    body_style = ParagraphStyle(
        "body",
        fontName="Helvetica",
        fontSize=6.5,
        leading=9,
        textColor=TEXT_DARK,
        alignment=TA_CENTER,
    )

    story = [
        Paragraph('"Lost time is never found again."', quote_style),
        Paragraph('— Benjamin Franklin', attr_style),
        Paragraph(
            'Every minute of your day is a brick in the foundation of your future. '
            'A disciplined routine is not a cage — it is the scaffold on which champions are built. '
            'Show up on time, every time. The world rewards those who respect the clock.',
            body_style,
        ),
    ]

    f = Frame(frame_x, frame_y, frame_w, frame_h, leftPadding=0, rightPadding=0,
              topPadding=0, bottomPadding=0, showBoundary=0)
    f.addFromList(story, c)


c_obj = canvas.Canvas(OUTPUT_PATH, pagesize=A4)
draw_page(c_obj)
c_obj.save()
print("PDF saved to", OUTPUT_PATH)

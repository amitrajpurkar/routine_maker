from reportlab.lib.pagesizes import A4, landscape
from reportlab.lib.units import mm
from reportlab.pdfgen import canvas
from reportlab.lib.colors import HexColor, white, black
from reportlab.platypus import Paragraph, Frame, Table, TableStyle
from reportlab.lib.styles import ParagraphStyle
from reportlab.lib.enums import TA_CENTER, TA_LEFT

OUTPUT = "/sessions/jolly-kind-sagan/mnt/routine_maker/OUTPUTS/weekly_meal_plan.pdf"

# Landscape A4
PAGE_W, PAGE_H = landscape(A4)   # 841.89 x 595.28 pts

ML = MR = 8 * mm
MT = 8 * mm
MB = 8 * mm
USABLE_W = PAGE_W - ML - MR

# B&W palette
C_BLACK  = HexColor("#000000")
C_DARK   = HexColor("#1A1A1A")
C_MID    = HexColor("#555555")
C_LIGHT  = HexColor("#AAAAAA")
C_VLIGHT = HexColor("#E8E8E8")
C_STRIPE = HexColor("#F5F5F5")
C_WHITE  = white

# ── Styles ─────────────────────────────────────────────────────────────────
def sty(name, font="Helvetica", size=7, leading=None, color=C_DARK,
        align=TA_LEFT, spaceAfter=0):
    return ParagraphStyle(name, fontName=font, fontSize=size,
                          leading=leading or size * 1.3,
                          textColor=color, alignment=align,
                          spaceAfter=spaceAfter)

S_TH    = sty("th",  "Helvetica-Bold",  7.5, color=C_BLACK, align=TA_CENTER)
S_DAY   = sty("day", "Helvetica-Bold",  8,   color=C_BLACK, align=TA_CENTER)
S_MEAL  = sty("ml",  "Helvetica-Bold",  7,   color=C_BLACK, align=TA_LEFT)
S_ITEM  = sty("it",  "Helvetica",       6.5, color=C_DARK,  align=TA_LEFT)
S_NOTE  = sty("nt",  "Helvetica-Oblique", 6, color=C_MID,   align=TA_CENTER)
S_LABEL = sty("lb",  "Helvetica-Bold",  7,   color=C_MID,   align=TA_LEFT)

# ── Meal data ───────────────────────────────────────────────────────────────
DAYS = ["Monday", "Tuesday", "Wednesday", "Thursday", "Friday", "Saturday", "Sunday"]

MEALS = {
    "Breakfast": [
        "Microwave scrambled eggs (2)\n+ whole wheat toast\n+ almond milk",
        "Wheatbix + almond milk\n+ fresh berries",
        "Smoked salmon + cream cheese\non whole wheat toast\n+ almond milk",
        "Turkey/ham deli roll-ups\n+ 2 hard-boiled eggs\n+ almond milk",
        "Multigrain cereal\n+ almond milk\n+ sliced banana",
        "Egg & turkey sausage\nEnglish muffin\n+ almond milk",
        "Microwave scrambled eggs (3)\n+ 2 turkey sausages\n+ toast + almond milk",
    ],
    "Packed Lunch": [
        "Turkey & cheese wrap\n+ banana",
        "Ham & Swiss sandwich\n+ apple + baby carrots",
        "Chicken salad wrap\n(rotisserie + mayo + lettuce)\n+ grapes",
        "Tuna salad sandwich ×2\n(canned tuna + mayo)\n+ orange",
        "Frank/sausage wrap\n+ mustard + cheese\n+ pre-packed salad box",
        "Egg salad sandwich\n+ fruit cup",
        "Smoked salmon bagel\n+ cream cheese\n+ cucumber slices",
    ],
    "Snack": [
        "Greek yogurt + granola",
        "Protein bar + orange",
        "String cheese + apple",
        "Almonds + banana",
        "Greek yogurt + honey",
        "Protein bar + almond milk",
        "Mixed nuts + dried fruit",
    ],
    "Dinner": [
        "Chicken rice bowl\n(Ready Rice + chicken strips\n+ steamed broccoli)",
        "Egg scramble w/ turkey sausage\n+ canned black beans\n+ whole wheat toast",
        "Canned chicken noodle soup\n+ dinner roll\n+ mixed fruit",
        "Frozen chicken breast\n+ Ready Rice packet\n+ microwave green beans",
        "Chicken quesadilla\n(rotisserie + cheese + salsa\nin whole wheat tortilla)\n+ side salad",
        "Chicken veggie soup\n(broth + chicken + Ready Rice\n+ frozen mixed veggies)",
        "Canned tomato soup\n+ cheese toast\n+ garden salad",
    ],
}

MEAL_KEYS = ["Breakfast", "Packed Lunch", "Snack", "Dinner"]

ROW_COLORS = {
    "Breakfast":    HexColor("#F0F0F0"),
    "Packed Lunch": HexColor("#FAFAFA"),
    "Snack":        HexColor("#F0F0F0"),
    "Dinner":       HexColor("#FAFAFA"),
}

GROCERY = [
    ("PROTEINS",
     "Rotisserie chicken (whole) · Eggs (1 doz) · Turkey deli slices · Ham deli slices · "
     "Smoked salmon · Canned tuna ×4 · Turkey sausage links (frozen) · "
     "Frozen pre-cooked chicken strips · Franks/hot dogs"),
    ("DAIRY & ALT.",
     "Almond milk (½ gal) · Greek yogurt ×6 · String cheese · Shredded cheese · "
     "Cream cheese · Swiss/American cheese slices"),
    ("GRAINS",
     "Whole wheat bread · Tortillas (burrito size) · English muffins · Bagels · "
     "Ready Rice packets ×5 · Multigrain cereal · Wheatbix / instant oats"),
    ("PRODUCE",
     "Bananas · Apples ×5 · Oranges ×4 · Grapes · Mixed berries · Baby carrots · "
     "Cucumber · Pre-washed lettuce · Frozen broccoli bag · Frozen green beans bag · "
     "Frozen mixed veggies bag"),
    ("PANTRY",
     "Chicken noodle soup ×3 · Tomato soup ×2 · Black beans ×2 · Chicken broth · "
     "Salsa · Mayo · Mustard · BBQ sauce · Honey · Granola · Protein bars ×8 · "
     "Almonds/mixed nuts · Dried fruit"),
]


# ── Page drawing ─────────────────────────────────────────────────────────────
def build_main_table():
    """Build the 7-day × 4-meal grid table."""
    col_w_day   = 12 * mm
    col_w_meal  = 2 * mm        # row label column
    n_days      = 7
    avail       = USABLE_W - col_w_day
    day_col_w   = avail / n_days

    # Header row: empty corner + day names
    header = [Paragraph("", S_TH)] + [Paragraph(d, S_DAY) for d in DAYS]

    rows = [header]
    for meal_key in MEAL_KEYS:
        row = [Paragraph(meal_key, S_MEAL)]
        for i, day in enumerate(DAYS):
            text = MEALS[meal_key][i]
            row.append(Paragraph(text, S_ITEM))
        rows.append(row)

    col_widths = [col_w_day] + [day_col_w] * n_days

    ts = TableStyle([
        # header row
        ("BACKGROUND",   (0, 0), (-1, 0),  C_DARK),
        ("TEXTCOLOR",    (0, 0), (-1, 0),  C_WHITE),
        ("LINEBELOW",    (0, 0), (-1, 0),  0.8, C_BLACK),
        # row label column
        ("BACKGROUND",   (0, 1), (0, -1),  C_VLIGHT),
        ("LINEAFTER",    (0, 0), (0, -1),  0.6, C_LIGHT),
        # alternating row fills for meal rows
        ("BACKGROUND",   (1, 1), (-1, 1),  ROW_COLORS["Breakfast"]),
        ("BACKGROUND",   (1, 2), (-1, 2),  ROW_COLORS["Packed Lunch"]),
        ("BACKGROUND",   (1, 3), (-1, 3),  ROW_COLORS["Snack"]),
        ("BACKGROUND",   (1, 4), (-1, 4),  ROW_COLORS["Dinner"]),
        # grid lines
        ("GRID",         (0, 0), (-1, -1), 0.3, C_LIGHT),
        ("BOX",          (0, 0), (-1, -1), 0.8, C_BLACK),
        # cell padding
        ("LEFTPADDING",  (0, 0), (-1, -1), 3),
        ("RIGHTPADDING", (0, 0), (-1, -1), 3),
        ("TOPPADDING",   (0, 0), (-1, -1), 3),
        ("BOTTOMPADDING",(0, 0), (-1, -1), 3),
        # vertical alignment
        ("VALIGN",       (0, 0), (-1, -1), "TOP"),
        # row label: centre vertically
        ("VALIGN",       (0, 1), (0, -1),  "MIDDLE"),
        # day header centre
        ("ALIGN",        (0, 0), (-1, 0),  "CENTER"),
    ])

    t = Table(rows, colWidths=col_widths, repeatRows=1)
    t.setStyle(ts)
    return t


def build_grocery_table():
    rows = []
    for cat, items in GROCERY:
        rows.append([Paragraph(cat, S_LABEL), Paragraph(items, S_ITEM)])
    ts = TableStyle([
        ("BACKGROUND",   (0, 0), (0, -1), C_VLIGHT),
        ("LINEAFTER",    (0, 0), (0, -1), 0.5, C_LIGHT),
        ("GRID",         (0, 0), (-1, -1), 0.3, C_LIGHT),
        ("BOX",          (0, 0), (-1, -1), 0.6, C_BLACK),
        ("LEFTPADDING",  (0, 0), (-1, -1), 3),
        ("RIGHTPADDING", (0, 0), (-1, -1), 3),
        ("TOPPADDING",   (0, 0), (-1, -1), 2),
        ("BOTTOMPADDING",(0, 0), (-1, -1), 2),
        ("VALIGN",       (0, 0), (-1, -1), "TOP"),
        ("ROWBACKGROUNDS", (0, 0), (-1, -1), [C_WHITE, C_STRIPE]),
    ])
    t = Table(rows, colWidths=[USABLE_W * 0.13, USABLE_W * 0.87])
    t.setStyle(ts)
    return t


def draw_page(cv):
    y = PAGE_H - MT

    # ── Title ─────────────────────────────────────────────────────────────
    cv.setFillColor(C_BLACK)
    cv.setFont("Helvetica-Bold", 14)
    cv.drawCentredString(PAGE_W / 2, y - 5.5*mm, "WEEKLY MEAL PLAN")
    cv.setFont("Helvetica", 7.5)
    cv.setFillColor(C_MID)
    cv.drawCentredString(PAGE_W / 2, y - 9.5*mm,
        "UCF Dorm  ·  Microwave meals  ·  3 meals + 1 snack per day  ·  "
        "Grocery run: Tuesday or Wednesday at Publix")
    y -= 13 * mm

    cv.setStrokeColor(C_LIGHT); cv.setLineWidth(0.5)
    cv.line(ML, y, PAGE_W - MR, y)
    y -= 3 * mm

    # ── Meal grid ────────────────────────────────────────────────────────
    t = build_main_table()
    tw, th = t.wrapOn(cv, USABLE_W, 999)
    t.drawOn(cv, ML, y - th)
    y -= th + 4 * mm

    # ── Section: Grocery ─────────────────────────────────────────────────
    cv.setFont("Helvetica-Bold", 8); cv.setFillColor(C_BLACK)
    cv.drawString(ML, y, "WEEKLY GROCERY LIST (Publix)  —  covers full 7 days")
    cv.setStrokeColor(C_LIGHT); cv.setLineWidth(0.4)
    cv.line(ML, y - 1.5*mm, PAGE_W - MR, y - 1.5*mm)
    y -= 5 * mm

    gt = build_grocery_table()
    gw, gh = gt.wrapOn(cv, USABLE_W, 999)
    gt.drawOn(cv, ML, y - gh)
    y -= gh + 4 * mm

    # ── Tips row ─────────────────────────────────────────────────────────
    tips = [
        "Use freezer items (Thu–Sun): frozen chicken strips, steam bags.",
        "Prep dinner at 17:00 → reheat after jogging at 19:00.",
        "Pack lunch the night before if mornings are rushed.",
        "Update weekly_meal_input.md before each Publix run.",
    ]
    tip_w = USABLE_W / len(tips)
    cv.setFont("Helvetica-Oblique", 6); cv.setFillColor(C_MID)
    for i, tip in enumerate(tips):
        cv.drawString(ML + i * tip_w, y, f"• {tip}")
    y -= 4 * mm

    # ── Footer ───────────────────────────────────────────────────────────
    cv.setFont("Helvetica-Oblique", 5.5); cv.setFillColor(C_LIGHT)
    cv.drawCentredString(PAGE_W / 2, MB,
        "Update INPUTS/weekly_meal_input.md each week and ask Claude to regenerate this plan.  "
        "·  Neptune 157  ·  June 2026")


# ── Run ───────────────────────────────────────────────────────────────────
cv = canvas.Canvas(OUTPUT, pagesize=landscape(A4))
cv.setFillColor(white)
cv.rect(0, 0, PAGE_W, PAGE_H, fill=1, stroke=0)
draw_page(cv)
cv.save()
print("PDF saved:", OUTPUT)

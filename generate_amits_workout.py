import os
from reportlab.lib.pagesizes import A4
from reportlab.lib.units import mm
from reportlab.pdfgen import canvas
from reportlab.lib.colors import HexColor, white
from reportlab.platypus import Paragraph, Table, TableStyle
from reportlab.lib.styles import ParagraphStyle
from reportlab.lib.enums import TA_CENTER, TA_LEFT

# Portable path: works no matter where the repo is cloned or which machine runs it,
# as long as this script stays in the project root next to the OUTPUTS/ folder.
SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
OUTPUT = os.path.join(SCRIPT_DIR, "OUTPUTS", "amits_weekly_workout.pdf")

PAGE_W, PAGE_H = A4
ML = MR = 10 * mm
MT = 8 * mm
MB = 8 * mm

C_BLACK  = HexColor("#000000")
C_DARK   = HexColor("#1A1A1A")
C_MID    = HexColor("#444444")
C_LIGHT  = HexColor("#AAAAAA")
C_VLIGHT = HexColor("#E8E8E8")
C_WHITE  = white

USABLE_W = PAGE_W - ML - MR


def sty(name, font="Helvetica", size=8, leading=None, color=C_DARK,
        align=TA_LEFT, spaceBefore=0, spaceAfter=0):
    return ParagraphStyle(name, fontName=font, fontSize=size,
                           leading=leading or size * 1.25, textColor=color,
                           alignment=align, spaceBefore=spaceBefore,
                           spaceAfter=spaceAfter)


S_TH  = sty("th",  "Helvetica-Bold", 6.5, color=C_BLACK, align=TA_CENTER)
S_TD  = sty("td",  "Helvetica",      6.5, color=C_DARK,  align=TA_LEFT)
S_TDC = sty("tdc", "Helvetica",      6.5, color=C_DARK,  align=TA_CENTER)
S_BODY = sty("body", "Helvetica",    7,   color=C_DARK)


def make_table(headers, rows, col_widths, center_cols=None):
    center_cols = center_cols or []
    data = [[Paragraph(h, S_TH) for h in headers]]
    for row in rows:
        cells = []
        for i, c in enumerate(row):
            style = S_TDC if i in center_cols else S_TD
            cells.append(Paragraph(str(c), style))
        data.append(cells)
    ts = TableStyle([
        ("BACKGROUND", (0, 0), (-1, 0), C_VLIGHT),
        ("LINEBELOW", (0, 0), (-1, 0), 0.5, C_LIGHT),
        ("LINEBELOW", (0, 1), (-1, -1), 0.3, C_VLIGHT),
        ("ROWBACKGROUNDS", (0, 1), (-1, -1), [C_WHITE, HexColor("#F5F5F5")]),
        ("LEFTPADDING", (0, 0), (-1, -1), 3),
        ("RIGHTPADDING", (0, 0), (-1, -1), 3),
        ("TOPPADDING", (0, 0), (-1, -1), 2),
        ("BOTTOMPADDING", (0, 0), (-1, -1), 2),
        ("BOX", (0, 0), (-1, -1), 0.5, C_LIGHT),
    ])
    t = Table(data, colWidths=col_widths)
    t.setStyle(ts)
    return t


def draw_table(c, t, y):
    tw, th = t.wrapOn(c, USABLE_W, 999)
    t.drawOn(c, ML, y - th)
    return y - th


def section_header(c, y, text, big=False):
    c.setFillColor(C_BLACK)
    c.setFont("Helvetica-Bold", 9 if big else 8)
    c.drawString(ML, y, text)
    c.setStrokeColor(C_LIGHT if not big else C_BLACK)
    c.setLineWidth(0.4 if not big else 0.8)
    c.line(ML, y - 1.5 * mm, ML + USABLE_W, y - 1.5 * mm)
    return y - (6 * mm if big else 5 * mm)


def bar(c, y, text, tag=None, height=6 * mm, fill=C_DARK, textcolor=C_WHITE):
    c.setFillColor(fill)
    c.rect(ML, y - height, USABLE_W, height, fill=1, stroke=0)
    c.setFillColor(textcolor)
    c.setFont("Helvetica-Bold", 8)
    c.drawString(ML + 2 * mm, y - height + 1.8 * mm, text)
    if tag:
        c.setFont("Helvetica-Oblique", 6.5)
        tw = c.stringWidth(tag, "Helvetica-Oblique", 6.5)
        c.drawString(ML + USABLE_W - tw - 2 * mm, y - height + 1.8 * mm, tag)
    return y - height - 1.5 * mm


def bullets(c, y, items, gap=4 * mm):
    c.setFont("Helvetica", 7)
    c.setFillColor(C_DARK)
    for it in items:
        c.drawString(ML, y, "•  " + it)
        y -= gap
    return y


def new_page(c):
    c.showPage()
    c.setFillColor(white)
    c.rect(0, 0, PAGE_W, PAGE_H, fill=1, stroke=0)


# ── DATA ─────────────────────────────────────────────────────────────────
OVERVIEW_ROWS = [
    ("Monday", "3-4 mi jog (4:30 AM)", "Circuit A - Lower Body & Core (20-25 min)", "~55-65 min"),
    ("Tuesday", "Rest from jogging", "Mobility & Stretch (15 min)", "~15 min"),
    ("Wednesday", "3-4 mi jog (4:30 AM)", "Circuit B - Upper Body & Core (20-25 min)", "~55-65 min"),
    ("Thursday", "Rest from jogging", "Optional easy walk (20-30 min) or rest", "Optional"),
    ("Friday", "3-4 mi jog (4:30 AM)", "Circuit C - Full Body & Core (20-25 min)", "~55-65 min"),
    ("Saturday", "Long jog, ~4 mi", "None - pure cardio day", "~40 min"),
    ("Sunday", "REST DAY", "Full recovery", "-"),
]

CIRCUIT_A = [
    ("Goblet Squat (dumbbell)", "3", "12", "Chest tall, knees track over toes"),
    ("Dumbbell Romanian Deadlift", "3", "12", "Hinge at hips, soft knees"),
    ("Dumbbell Walking Lunge", "3", "10/leg", "Long stride, controlled descent"),
    ("Glute Bridge (bodyweight/DB)", "3", "15", "Drive through heels, squeeze at top"),
    ("Plank", "3", "30-45 sec", "Hips level, brace core"),
    ("Standing Calf Raise (DBs)", "3", "15", "2 sec up, 2 sec down"),
]

CIRCUIT_B = [
    ("Dumbbell Floor Press", "3", "12", "Control descent, elbows ~45 deg"),
    ("Dumbbell Bent-Over Row", "3", "12", "Flat back, squeeze shoulder blade"),
    ("Dumbbell Shoulder Press", "3", "12", "Don't arch lower back"),
    ("Band Pull-Apart", "3", "15", "Slow, squeeze shoulder blades"),
    ("Dumbbell Bicep Curl", "3", "12", "Full range, no swinging"),
    ("Dead Bug", "3", "12/side", "Slow, lower back flat on floor"),
]

CIRCUIT_C = [
    ("Dumbbell Thruster (squat-press)", "3", "12", "Lighter DBs, full range"),
    ("Renegade Row (DBs, plank)", "3", "10/side", "Minimize hip rotation"),
    ("Reverse Lunge to Curl", "3", "10/leg", "Combines legs + arms"),
    ("Bird Dog", "3", "12/side", "Pause at top, opposite arm/leg"),
    ("Side Plank", "3", "20-30 sec/side", "Stack hips, straight line"),
    ("Mountain Climbers", "3", "30 sec", "Moderate pace, brace core"),
]

HYDRATION_ROWS = [
    ("On waking (before 4:30 AM jog)", "300-400 ml water immediately"),
    ("Right after jog", "200-300 ml water (more if hot/humid)"),
    ("Breakfast", "1 full glass with the meal"),
    ("Mid-morning", "Refill & finish a 500 ml bottle"),
    ("Lunch", "1 full glass with the meal"),
    ("Afternoon", "Refill & finish a second 500 ml bottle"),
    ("Dinner", "1 full glass with the meal"),
    ("After ~7:30 PM", "Taper fluids - sip only, protect sleep"),
]

SLEEP_ROWS = [
    ("8:15 PM", "Stop screens/work email - dim the lights"),
    ("8:15-8:35 PM", "Light stretch/short walk - lay out jog clothes & fill bottle"),
    ("8:35-8:50 PM", "Shower/hygiene - brief non-stimulating reading"),
    ("8:50-9:00 PM", "Lights out"),
]

EATING_BULLETS = [
    "Daily calorie target: ~1,900-2,050 kcal (est. maintenance ~2,550-2,650 kcal/day)",
    "Protein target: ~130-150 g/day (~30-40 g per meal) to protect muscle in a deficit",
    "Half the plate = vegetables/fruit at lunch and dinner",
    "Cut liquid calories - water, black coffee, unsweetened tea only",
    "Keep starchy carbs concentrated around the morning jog",
    "Dinner cutoff by 7:30-8:00 PM - aligns with sleep wind-down",
    "Batch-prep meals once a week (e.g. Sunday) to avoid impulsive choices",
    "One flexible meal per week is fine - supports long-term adherence",
]

PROGRESSION_ROWS = [
    ("Phase 1 - Foundation", "Wks 1-4", "Learn form, light-mod DB loads", "Keep pace/distance as-is", "-4 to -6 lb - waist -0.5 to -1 in"),
    ("Phase 2 - Build", "Wks 5-8", "Increase DB weight 2.5-5 lb", "Swap 1 Sat long jog/2wks for tempo", "-10 to -13 lb - waist -1.5 to -2 in"),
    ("Phase 3 - Sharpen", "Wks 9-12", "Highest resistance within limits", "Maintain volume, focus on pace", "-18 to -20 lb - waist <=32 in"),
]

REMINDERS = [
    "Get a quick medical check-up/clearance before ramping up training load at 52.",
    "Warm-up and cool-down are not optional - joint health matters more now.",
    "Progressive overload only when form is solid for 2 consecutive sessions.",
    "Track mileage/pace on your Nike dashboard monthly - confirm ~60 mi/month holds.",
    "A missed strength session is not a failure - get back on schedule next time.",
    "Sleep and hydration are load-bearing parts of this plan, not afterthoughts.",
]


def draw_circuit_page(c, y, day_title, tag, rows, finish_note):
    y = bar(c, y, day_title, tag)
    headers = ["Exercise", "Sets", "Reps", "Notes"]
    cws = [USABLE_W * f for f in [0.34, 0.08, 0.13, 0.45]]
    t = make_table(headers, rows, cws, center_cols=[1, 2])
    y = draw_table(c, t, y)
    c.setFont("Helvetica-Oblique", 6.5)
    c.setFillColor(C_MID)
    c.drawString(ML, y - 3 * mm, "Finish: " + finish_note)
    return y - 8 * mm


# ── PAGE 1 ───────────────────────────────────────────────────────────────
cv = canvas.Canvas(OUTPUT, pagesize=A4)
cv.setFillColor(white)
cv.rect(0, 0, PAGE_W, PAGE_H, fill=1, stroke=0)

y = PAGE_H - MT
cv.setFillColor(C_BLACK)
cv.setFont("Helvetica-Bold", 16)
cv.drawCentredString(PAGE_W / 2, y - 6 * mm, "AMIT'S WEEKLY WORKOUT PLAN")
cv.setFont("Helvetica", 8)
cv.setFillColor(C_MID)
cv.drawCentredString(PAGE_W / 2, y - 10.5 * mm,
                     "12-Week Weight Loss & Strength Program  -  Home Equipment Edition")
y -= 14 * mm

# profile box
box_h = 22 * mm
cv.setFillColor(C_VLIGHT)
cv.rect(ML, y - box_h, USABLE_W, box_h, fill=1, stroke=0)
cv.setStrokeColor(C_LIGHT); cv.setLineWidth(0.4)
cv.rect(ML, y - box_h, USABLE_W, box_h, fill=0, stroke=1)
lines = [
    "Profile: Male, 52 yrs - 5'7\" (170 cm) - 185 lb - Waist 35 in",
    "Goal (12 weeks): 165 lb  -  Waist <= 32 in  -  Increased strength & stamina",
    "Baseline: 4:30 AM jog, 3-4 mi, 4x/week (~60 mi/month) - the only current workout",
    "Equipment: Home only - dumbbells, resistance bands. Added time: 20-30 min, 3x/week.",
]
cv.setFont("Helvetica", 7)
cv.setFillColor(C_DARK)
ly = y - 4 * mm
for line in lines:
    cv.drawString(ML + 3 * mm, ly, line)
    ly -= 4.3 * mm
y -= box_h + 4 * mm

y = section_header(cv, y, "WHY THIS PLAN IS BUILT THIS WAY", big=True)
why_text = ("Your jogging base is solid - the plan keeps it unchanged and layers on 3 short home strength "
            "sessions, tighter hydration/sleep, and calorie/protein guardrails. Losing 20 lb in 12 weeks "
            "averages ~1.6-1.7 lb/week - achievable with consistent execution, but get medical clearance "
            "first given age and pace of this goal. Not personalized medical or dietetic advice.")
cv.setFont("Helvetica", 7)
cv.setFillColor(C_DARK)
words_y = y
import textwrap
for line in textwrap.wrap(why_text, width=112):
    cv.drawString(ML, words_y, line)
    words_y -= 3.6 * mm
y = words_y - 3 * mm

y = section_header(cv, y, "WEEKLY OVERVIEW")
headers = ["Day", "Morning Jog (unchanged)", "Added Strength / Recovery", "Total Time"]
cws = [USABLE_W * f for f in [0.13, 0.28, 0.42, 0.17]]
t = make_table(headers, OVERVIEW_ROWS, cws, center_cols=[3])
y = draw_table(cv, t, y)

cv.setFont("Helvetica-Oblique", 6)
cv.setFillColor(C_LIGHT)
cv.drawCentredString(PAGE_W / 2, MB, "Reference: Nike Running Dashboard - amitrajpurkar.github.io/static/nike-dashboard.html")

# ── PAGE 2: Circuit A + B ─────────────────────────────────────────────────
new_page(cv)
y = PAGE_H - MT
y = draw_circuit_page(cv, y, "MONDAY - CIRCUIT A: LOWER BODY & CORE", "Post-jog, 20-25 min",
                       CIRCUIT_A, "quad stretch - hamstring stretch - calf stretch on wall (3-5 min)")
y = draw_circuit_page(cv, y, "WEDNESDAY - CIRCUIT B: UPPER BODY & CORE", "Post-jog, 20-25 min",
                       CIRCUIT_B, "chest doorway stretch - shoulder cross-body - triceps overhead (3-5 min)")

y = section_header(cv, y, "STRENGTH FORMAT (ALL 3 CIRCUITS)")
bullets(cv, y, [
    "3 sets per exercise - 12-15 reps (or time noted) - 60-75 sec rest between sets",
    "Stop 2-3 reps before failure - form over weight, always",
    "Increase dumbbell weight 2.5-5 lb only after 2 clean sessions in a row",
], gap=4 * mm)

# ── PAGE 3: Circuit C + mobility + Sat/Sun + Hydration ────────────────────
new_page(cv)
y = PAGE_H - MT
y = draw_circuit_page(cv, y, "FRIDAY - CIRCUIT C: FULL BODY & CORE", "Post-jog, 20-25 min",
                       CIRCUIT_C, "full-body static stretch, hold each 20-30 sec")

y = bar(cv, y, "TUESDAY & THURSDAY - MOBILITY & RECOVERY (15 MIN)", "Not a rest-from-movement day", fill=C_LIGHT, textcolor=C_BLACK)
y = bullets(cv, y, [
    "Dynamic hip circles + leg swings - 10 each direction/side",
    "World's Greatest Stretch - 5/side  -  Hip flexor kneeling stretch - 30 sec/side",
    "Foam roll or hand-massage calves, hamstrings, IT band - 3-4 min",
    "Optional: 20-30 min easy walk on Thursday if you want extra movement without load",
], gap=4 * mm)
y -= 2 * mm

y = bar(cv, y, "SATURDAY (LONG JOG) & SUNDAY (FULL REST)", fill=C_LIGHT, textcolor=C_BLACK)
y = bullets(cv, y, [
    "Saturday: pure cardio, no added strength. Full stretch cool-down after (quads, hams, calves, hip flexors, lower back).",
    "Sunday: no training. Sleep in if you can, hydrate, meal-prep for the week, light walk only if restless.",
], gap=4 * mm)
y -= 2 * mm

y = section_header(cv, y, "HYDRATION PLAN  (Target: ~3.0-3.3 L / 100-110 oz per day)")
t = make_table(["Time", "Action"], HYDRATION_ROWS, [USABLE_W * 0.32, USABLE_W * 0.68])
y = draw_table(cv, t, y)
cv.setFont("Helvetica-Oblique", 6.5)
cv.setFillColor(C_MID)
cv.drawString(ML, y - 3 * mm, "Rule of thumb: if nothing but coffee before lunch, you're already behind for the day.")

# ── PAGE 4: Sleep + Eating ────────────────────────────────────────────────
new_page(cv)
y = PAGE_H - MT
y = section_header(cv, y, "SLEEP PLAN  (Target: Lights-out by 9:00-9:15 PM)", big=True)
cv.setFont("Helvetica", 7)
cv.setFillColor(C_DARK)
note = ("Waking at 4:30 AM makes a full 8-hour night hard. A consistent 9:00-9:15 PM lights-out gets you "
        "~7-7.25 hours - a real upgrade over an irregular schedule.")
ny = y
for line in textwrap.wrap(note, width=112):
    cv.drawString(ML, ny, line)
    ny -= 3.6 * mm
y = ny - 3 * mm

t = make_table(["Time", "Wind-down step"], SLEEP_ROWS, [USABLE_W * 0.25, USABLE_W * 0.75])
y = draw_table(cv, t, y)
y -= 3 * mm
y = bullets(cv, y, [
    "Caffeine cutoff: none after 2:00 PM",
    "Consistency: same lights-out time on weekends too (+/- 30 min max)",
], gap=4 * mm)
y -= 3 * mm

y = section_header(cv, y, "EATING GUARDRAILS  (Not a full meal plan - just the rules that matter)", big=True)
y = bullets(cv, y, EATING_BULLETS, gap=4.2 * mm)

# ── PAGE 5: Progression + Tracker + Reminders ─────────────────────────────
new_page(cv)
y = PAGE_H - MT
y = section_header(cv, y, "12-WEEK PHASED PROGRESSION", big=True)
headers = ["Phase", "Weeks", "Strength Focus", "Jog Adjustment", "Target Cumulative Change"]
cws = [USABLE_W * f for f in [0.16, 0.08, 0.24, 0.26, 0.26]]
t = make_table(headers, PROGRESSION_ROWS, cws)
y = draw_table(cv, t, y)
y -= 5 * mm

y = section_header(cv, y, "WEEKLY TRACKER  (Weigh in once a week, same day/time)", big=True)
tracker_headers = ["Week", "Weight (lb)", "Waist (in)", "Avg Sleep (hrs)", "Strength (/3)", "Notes"]
tracker_rows = [[str(i + 1), "", "", "", "", ""] for i in range(12)]
cws2 = [USABLE_W * f for f in [0.08, 0.14, 0.12, 0.14, 0.12, 0.40]]
t2 = make_table(tracker_headers, tracker_rows, cws2, center_cols=[0, 1, 2, 3, 4])
y = draw_table(cv, t2, y)
y -= 6 * mm

y = section_header(cv, y, "KEY REMINDERS", big=True)
bullets(cv, y, REMINDERS, gap=4.2 * mm)

cv.setFont("Helvetica-Oblique", 6)
cv.setFillColor(C_LIGHT)
cv.drawCentredString(PAGE_W / 2, MB, "Built for Amit - Home Equipment Edition - July 2026")

cv.save()
print("PDF saved:", OUTPUT)

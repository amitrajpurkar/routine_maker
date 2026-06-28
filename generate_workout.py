from reportlab.lib.pagesizes import A4
from reportlab.lib.units import mm
from reportlab.pdfgen import canvas
from reportlab.lib.colors import HexColor, white, black
from reportlab.platypus import Paragraph, Frame, Table, TableStyle
from reportlab.lib.styles import ParagraphStyle
from reportlab.lib.enums import TA_CENTER, TA_LEFT

OUTPUT = "/sessions/jolly-kind-sagan/mnt/routine_maker/weekly_workout_plan.pdf"

PAGE_W, PAGE_H = A4
ML = MR = 10 * mm   # left/right margins
MT = 8 * mm          # top margin
MB = 8 * mm          # bottom margin

# B&W palette
C_BLACK  = HexColor("#000000")
C_DARK   = HexColor("#1A1A1A")
C_MID    = HexColor("#444444")
C_LIGHT  = HexColor("#AAAAAA")
C_VLIGHT = HexColor("#E8E8E8")
C_WHITE  = white

USABLE_W = PAGE_W - ML - MR

# ── Styles ─────────────────────────────────────────────────────────────────
def sty(name, font="Helvetica", size=8, leading=None, color=C_DARK,
        align=TA_LEFT, spaceBefore=0, spaceAfter=0):
    return ParagraphStyle(name, fontName=font, fontSize=size,
                          leading=leading or size * 1.25, textColor=color,
                          alignment=align, spaceBefore=spaceBefore,
                          spaceAfter=spaceAfter)

S_TITLE   = sty("title",  "Helvetica-Bold",    16, color=C_BLACK, align=TA_CENTER)
S_SUB     = sty("sub",    "Helvetica-Oblique",  8, color=C_MID,   align=TA_CENTER)
S_DAY     = sty("day",    "Helvetica-Bold",     9, color=C_BLACK)
S_PHASE   = sty("phase",  "Helvetica-Bold",     7.5, color=C_MID)
S_BULLET  = sty("bullet", "Helvetica",          7, color=C_DARK)
S_NOTE    = sty("note",   "Helvetica-Oblique",  6.5, color=C_MID, align=TA_CENTER)
S_TH      = sty("th",     "Helvetica-Bold",     6.5, color=C_BLACK, align=TA_CENTER)
S_TD      = sty("td",     "Helvetica",          6.5, color=C_DARK,  align=TA_LEFT)
S_TDC     = sty("tdc",    "Helvetica",          6.5, color=C_DARK,  align=TA_CENTER)
S_SEC     = sty("sec",    "Helvetica-Bold",     8,   color=C_BLACK)
S_BODY    = sty("body",   "Helvetica",          7,   color=C_DARK)

# ── Table helper ───────────────────────────────────────────────────────────
def workout_table(headers, rows, col_widths):
    data = [[Paragraph(h, S_TH) for h in headers]]
    for row in rows:
        data.append([Paragraph(str(c), S_TDC if i > 0 else S_TD)
                     for i, c in enumerate(row)])
    ts = TableStyle([
        ("BACKGROUND",  (0, 0), (-1, 0),  C_VLIGHT),
        ("LINEBELOW",   (0, 0), (-1, 0),  0.5, C_LIGHT),
        ("LINEBELOW",   (0, 1), (-1, -1), 0.3, C_VLIGHT),
        ("ROWBACKGROUNDS", (0, 1), (-1, -1), [C_WHITE, HexColor("#F5F5F5")]),
        ("LEFTPADDING",  (0, 0), (-1, -1), 3),
        ("RIGHTPADDING", (0, 0), (-1, -1), 3),
        ("TOPPADDING",   (0, 0), (-1, -1), 2),
        ("BOTTOMPADDING",(0, 0), (-1, -1), 2),
        ("BOX",          (0, 0), (-1, -1), 0.5, C_LIGHT),
    ])
    t = Table(data, colWidths=col_widths)
    t.setStyle(ts)
    return t

# ── Data ───────────────────────────────────────────────────────────────────
DAYS = [
    {
        "title": "MONDAY — Core & Functional Strength",
        "tag": "Moderate Intensity",
        "warmup": "5 min treadmill walk  ·  Leg swings × 10  ·  Hip circles × 10  ·  Arm circles × 10",
        "cooldown": "Child's pose  ·  Cat-cow × 10  ·  Lying spinal twist  ·  Hip flexor stretch",
        "exercises": [
            ("Plank",                               "3", "45 sec",  "Elbows under shoulders, hips level"),
            ("Dead Bug",                            "3", "12/side", "Slow & controlled, lower back flat"),
            ("Cable Crunch / Crunch Machine",       "3", "15",      "Squeeze abs, don't pull with neck"),
            ("Pallof Press (anti-rotation)",        "3", "12/side", "Stand tall, resist rotation"),
            ("DB Romanian Deadlift (light)",        "3", "12",      "Hinge at hips, soft knees"),
            ("Bird Dog",                            "3", "12/side", "Pause at top of each rep"),
            ("Farmer's Carry (dumbbells)",          "3", "30 m",    "Stand tall, shoulders back"),
        ],
    },
    {
        "title": "TUESDAY — Upper Body Push  (Chest · Shoulders · Triceps)",
        "tag": "Moderate Intensity",
        "warmup": "Arm circles × 15  ·  Band pull-aparts × 15  ·  5 min light rowing machine",
        "cooldown": "Chest doorway stretch  ·  Shoulder cross-body stretch  ·  Tricep overhead stretch",
        "exercises": [
            ("Dumbbell Bench Press",                "3", "12",  "Control the descent"),
            ("Incline Dumbbell Press",              "3", "12",  "30–45° incline, upper chest"),
            ("Cable Chest Fly",                     "3", "15",  "Wide arc, squeeze at midline"),
            ("Dumbbell Shoulder Press",             "3", "12",  "Don't arch lower back"),
            ("Dumbbell Lateral Raise",              "3", "15",  "Light weight, slight elbow bend"),
            ("Tricep Rope Pushdown (cable)",        "3", "15",  "Elbows pinned, full extension"),
            ("Overhead DB Tricep Extension",        "3", "12",  "Both hands on one DB, elbows in"),
        ],
    },
    {
        "title": "WEDNESDAY — Lower Body  (Quads · Hamstrings · Glutes · Calves)",
        "tag": "Moderate Intensity",
        "warmup": "5 min easy bike  ·  Leg swings × 10  ·  Bodyweight squats × 10 (slow)",
        "cooldown": "Quad stretch  ·  Hamstring stretch  ·  Pigeon pose 45 sec/side  ·  Calf stretch",
        "exercises": [
            ("Goblet Squat (dumbbell)",             "3", "15",  "Chest tall, knees track toes"),
            ("Leg Press Machine",                   "3", "12",  "Don't lock knees at top"),
            ("Dumbbell Walking Lunge",              "3", "10/leg","Long stride, back knee near floor"),
            ("Seated Leg Curl Machine",             "3", "12",  "Full range, no jerking"),
            ("Glute Bridge (bodyweight)",           "3", "15",  "Drive through heels, squeeze top"),
            ("Standing Calf Raise",                 "3", "20",  "2 sec up · 2 hold · 2 down"),
            ("Step-Ups (box + dumbbells)",          "3", "10/leg","Full hip extension at top"),
        ],
    },
    {
        "title": "THURSDAY — Back Strength  (Lats · Traps · Rear Delts)",
        "tag": "Moderate Intensity",
        "warmup": "5 min rowing machine (light)  ·  Cat-cow × 10  ·  Shoulder rotations × 15",
        "cooldown": "Lat stretch  ·  Child's pose  ·  Thoracic rotation  ·  Upper trap stretch",
        "exercises": [
            ("Lat Pulldown (cable)",                "3", "12",  "Pull to upper chest, lean back slightly"),
            ("Seated Cable Row",                    "3", "12",  "Elbows drive back, squeeze blades"),
            ("DB Single-Arm Row",                   "3", "12/arm","Flat back, elbow drives to hip"),
            ("Face Pull (cable rope)",              "3", "15",  "External rotation, elbows high"),
            ("Bent-Over Rear Delt Fly (DB)",        "3", "15",  "Arms arc out wide"),
            ("Dumbbell Shrugs",                     "3", "15",  "Straight up, 1 sec hold, no rolling"),
            ("TRX Row / Assisted Pull-Up Machine",  "3", "10",  "Full stretch down, full contraction up"),
        ],
    },
    {
        "title": "FRIDAY — Arms & Biceps  (Biceps · Forearms · Light Triceps)",
        "tag": "Light–Moderate Intensity",
        "warmup": "5 min light elliptical  ·  Wrist circles × 10  ·  Arm swings across body × 15",
        "cooldown": "Bicep wall stretch  ·  Wrist flexor stretch  ·  Wrist extensor stretch  ·  Forearm massage",
        "exercises": [
            ("Dumbbell Bicep Curl",                 "3", "15",  "Full range, don't swing elbows"),
            ("Hammer Curl",                         "3", "15",  "Neutral grip, targets brachialis"),
            ("Cable Bicep Curl",                    "3", "15",  "Constant tension, slow negatives"),
            ("Incline Dumbbell Curl",               "3", "12",  "Full stretch at bottom"),
            ("EZ-Bar / Barbell Curl",               "3", "12",  "Elbows tucked at sides"),
            ("Wrist Curls (DB, seated)",            "3", "20",  "Forearm on thigh, full range"),
            ("Overhead Rope Extension (light)",     "3", "15",  "Keeps arms balanced"),
        ],
    },
    {
        "title": "SATURDAY — Full Body Light Circuit  (Active Recovery)",
        "tag": "Light Intensity — 3 Rounds · 45 sec work / 15 sec rest",
        "warmup": "5 min treadmill walk/jog  ·  Full body dynamic stretch head to toe",
        "cooldown": "Full body static stretch routine — hold each stretch 30 seconds",
        "exercises": [
            ("Bodyweight Squat",            "3 rds", "45 sec", "Slow and controlled"),
            ("Push-Up (or knee push-up)",   "3 rds", "45 sec", "Quality over quantity"),
            ("TRX Row",                     "3 rds", "45 sec", "Body at 45°, row to chest"),
            ("Reverse Lunge (bodyweight)",  "3 rds", "45 sec", "Alternate legs"),
            ("Plank Hold",                  "3 rds", "45 sec", "Breathe steadily"),
            ("DB Shoulder Press (light)",   "3 rds", "45 sec", "3–5 kg dumbbells"),
            ("Step Touches / Jumping Jacks","3 rds", "45 sec", "Gentle heart rate"),
        ],
    },
]

RWCSESSIONS = [
    ("Fitness Assessment",   "Free — book at ucf.qualtrics.com/jfe/form/SV_2uFJIOmriZfGWhw",
     "Start here. 1-on-1 with Certified Trainer: body composition + baseline measurements + personalised recommendations."),
    ("Personal Training",    "By appt at RWC Main · Walk-ins at RWC Downtown · fitness@ucf.edu · 407-823-2408",
     "Nationally certified trainers (ACE/ACSM/NASM/ISSA/NSCA). Custom program for your goals. Initial Consultation required."),
    ("Group Exercise",       "Free · 60+ classes/week · Reserve 24h before at ucfrwc.org · Arrive 15 min early",
     "Best beginner classes: KnightFit (full body), Cycle+Strength (legs+cardio), Pilates (core), Yoga (recovery), HIIT (stamina — start after 4–6 weeks)."),
]

REMINDERS = [
    "Eat a light protein snack 30–45 min before training (banana + peanut butter, or boiled egg).",
    "Bring a full water bottle — drink between every set.",
    "Warm-up and cool-down protect you from injury — never skip them.",
    "Never train to failure as a beginner — stop 2–3 reps before you can't continue.",
    "Log your weights in a notebook or phone — progressive overload is how you get stronger.",
    "Pain (not muscle burn) → stop and visit RWC Athletic Training Room (Tue–Thu 13:30–17:00).",
]


# ── Page renderer ──────────────────────────────────────────────────────────
def draw_page1(c):
    """Page 1: Title + Mon–Wed"""
    y = PAGE_H - MT
    # title
    c.setFillColor(C_BLACK)
    c.setFont("Helvetica-Bold", 16)
    c.drawCentredString(PAGE_W / 2, y - 6*mm, "WEEKLY GYM WORKOUT PLAN")
    c.setFont("Helvetica", 8)
    c.setFillColor(C_MID)
    c.drawCentredString(PAGE_W / 2, y - 10.5*mm,
                        "UCF Recreation & Wellness Center  ·  Beginner Strength & Stamina Program  ·  06:00–07:00 Morning Sessions")
    y -= 14 * mm
    # separator
    c.setStrokeColor(C_LIGHT); c.setLineWidth(0.5)
    c.line(ML, y, PAGE_W - MR, y)
    y -= 2 * mm

    for day in DAYS[:3]:
        y = draw_day(c, day, y)
        if y < MB + 5*mm:
            break

def draw_page2(c):
    """Page 2: Thu–Sat + Sunday note + Evening Cardio"""
    y = PAGE_H - MT
    for day in DAYS[3:]:
        y = draw_day(c, day, y)
    y = draw_sunday(c, y)
    y = draw_evening(c, y)

def draw_page3(c):
    """Page 3: RWC Instructor Sessions + Reminders + Progress tracker"""
    y = PAGE_H - MT
    y = draw_rwc(c, y)
    y = draw_reminders(c, y)
    y = draw_tracker(c, y)
    # footer
    c.setFont("Helvetica-Oblique", 6)
    c.setFillColor(C_LIGHT)
    c.drawCentredString(PAGE_W / 2, MB,
                        "UCF RWC  ·  rwc.sswb.ucf.edu  ·  407-823-2408  ·  ucfrec@ucf.edu  ·  June 2026")


def draw_day(c, day, y):
    PAD = 2 * mm
    # day header bar
    bar_h = 6 * mm
    c.setFillColor(C_DARK)
    c.rect(ML, y - bar_h, USABLE_W, bar_h, fill=1, stroke=0)
    c.setFillColor(C_WHITE)
    c.setFont("Helvetica-Bold", 8)
    c.drawString(ML + PAD, y - bar_h + 1.8*mm, day["title"])
    c.setFont("Helvetica-Oblique", 6.5)
    tag_w = c.stringWidth(day["tag"], "Helvetica-Oblique", 6.5)
    c.drawString(ML + USABLE_W - tag_w - PAD, y - bar_h + 1.8*mm, day["tag"])
    y -= bar_h + 1*mm

    # warm-up line
    c.setFont("Helvetica-Bold", 6.5); c.setFillColor(C_MID)
    c.drawString(ML, y, "WARM-UP (8 min):")
    c.setFont("Helvetica", 6.5); c.setFillColor(C_DARK)
    c.drawString(ML + 28*mm, y, day["warmup"])
    y -= 4 * mm

    # exercise table
    headers = ["Exercise", "Sets", "Reps", "Coaching Note"]
    cws = [USABLE_W * f for f in [0.37, 0.08, 0.10, 0.45]]
    t = workout_table(headers, day["exercises"], cws)
    tw, th = t.wrapOn(c, USABLE_W, 999)
    t.drawOn(c, ML, y - th)
    y -= th + 1*mm

    # cool-down line
    c.setFont("Helvetica-Bold", 6.5); c.setFillColor(C_MID)
    c.drawString(ML, y, "COOL-DOWN (10 min):")
    c.setFont("Helvetica", 6.5); c.setFillColor(C_DARK)
    c.drawString(ML + 30*mm, y, day["cooldown"])
    y -= 5 * mm

    return y


def draw_sunday(c, y):
    bar_h = 6 * mm
    c.setFillColor(C_LIGHT)
    c.rect(ML, y - bar_h, USABLE_W, bar_h, fill=1, stroke=0)
    c.setFillColor(C_BLACK)
    c.setFont("Helvetica-Bold", 8)
    c.drawString(ML + 2*mm, y - bar_h + 1.8*mm, "SUNDAY — REST DAY  ★")
    c.setFont("Helvetica", 7)
    c.setFillColor(C_MID)
    msg = ("No gym. The body builds muscle during recovery, not the workout. Sleep, hydrate, eat well, "
           "light walk, meal prep, call home, enjoy the day.")
    c.drawString(ML + 2*mm, y - bar_h - 4*mm, msg)
    return y - bar_h - 8*mm


def draw_evening(c, y):
    # section heading
    c.setFillColor(C_DARK); c.setFont("Helvetica-Bold", 8)
    c.drawString(ML, y, "EVENING CARDIO SESSION  (17:30–18:30 — Separate from Morning Gym)")
    c.setStrokeColor(C_LIGHT); c.setLineWidth(0.4)
    c.line(ML, y - 1.5*mm, ML + USABLE_W, y - 1.5*mm)
    y -= 5*mm

    rows = [
        ("Jogging / Running",    "Mon · Wed · Fri", "Campus paths, RWC Park"),
        ("Cycling",              "Tue · Thu",        "Campus cycle routes"),
        ("Swimming",             "Saturday",         "RWC Lap Pool — Mon–Fri 06:00–19:00, Sat 11:00–17:00"),
        ("Walk & Explore",       "Any day",          "Campus cafes, new spots — lower intensity option"),
    ]
    headers = ["Activity", "Suggested Days", "Where at UCF"]
    cws = [USABLE_W * f for f in [0.22, 0.18, 0.60]]
    t = workout_table(headers, rows, cws)
    tw, th = t.wrapOn(c, USABLE_W, 999)
    t.drawOn(c, ML, y - th)
    y -= th + 3*mm

    c.setFont("Helvetica-Oblique", 6.5); c.setFillColor(C_MID)
    c.drawString(ML, y,
                 "Tip: On heavy gym days, dial back evening intensity — a brisk walk counts. Consistency beats perfection.")
    return y - 5*mm


def draw_rwc(c, y):
    c.setFont("Helvetica-Bold", 9); c.setFillColor(C_BLACK)
    c.drawString(ML, y, "RWC INSTRUCTOR-LED SESSIONS FOR BEGINNERS")
    c.setStrokeColor(C_BLACK); c.setLineWidth(0.8)
    c.line(ML, y - 1.5*mm, ML + USABLE_W, y - 1.5*mm)
    y -= 6*mm

    labels = ["Step 1 — Fitness Assessment (Start Here)",
              "Step 2 — Personal Training",
              "Step 3 — Group Exercise Classes (Free)"]
    for i, (label, info, detail) in enumerate(RWCSESSIONS):
        # step box
        c.setFillColor(C_VLIGHT)
        box_h = 14 * mm
        c.rect(ML, y - box_h, USABLE_W, box_h, fill=1, stroke=0)
        c.setStrokeColor(C_LIGHT); c.setLineWidth(0.3)
        c.rect(ML, y - box_h, USABLE_W, box_h, fill=0, stroke=1)
        # left accent
        c.setFillColor(C_DARK)
        c.rect(ML, y - box_h, 2*mm, box_h, fill=1, stroke=0)
        # label
        c.setFont("Helvetica-Bold", 7.5); c.setFillColor(C_BLACK)
        c.drawString(ML + 4*mm, y - 4*mm, labels[i])
        # info
        c.setFont("Helvetica-Oblique", 6.5); c.setFillColor(C_MID)
        c.drawString(ML + 4*mm, y - 7.5*mm, info)
        # detail
        c.setFont("Helvetica", 6.5); c.setFillColor(C_DARK)
        # wrap detail text
        fr = Frame(ML + 4*mm, y - box_h + 1*mm,
                   USABLE_W - 6*mm, 5*mm,
                   leftPadding=0, rightPadding=0, topPadding=0, bottomPadding=0)
        story = [Paragraph(detail, S_BODY)]
        fr.addFromList(story, c)
        y -= box_h + 2*mm

    return y - 2*mm


def draw_reminders(c, y):
    c.setFont("Helvetica-Bold", 8); c.setFillColor(C_BLACK)
    c.drawString(ML, y, "KEY REMINDERS")
    c.setStrokeColor(C_LIGHT); c.setLineWidth(0.4)
    c.line(ML, y - 1.5*mm, ML + USABLE_W, y - 1.5*mm)
    y -= 5*mm
    c.setFont("Helvetica", 7); c.setFillColor(C_DARK)
    for r in REMINDERS:
        c.drawString(ML, y, f"•  {r}")
        y -= 4*mm
    return y - 3*mm


def draw_tracker(c, y):
    c.setFont("Helvetica-Bold", 8); c.setFillColor(C_BLACK)
    c.drawString(ML, y, "4-WEEK PROGRESS TRACKER")
    c.setStrokeColor(C_LIGHT); c.setLineWidth(0.4)
    c.line(ML, y - 1.5*mm, ML + USABLE_W, y - 1.5*mm)
    y -= 5*mm

    headers = ["Week", "Mon Core", "Tue Upper", "Wed Legs", "Thu Back", "Fri Arms", "Sat Circuit", "Sun Rest"]
    rows = [
        [f"Week {i+1}", "[ ]", "[ ]", "[ ]", "[ ]", "[ ]", "[ ]", "[ ]"]
        for i in range(4)
    ]
    cws_raw = [0.10, 0.13, 0.13, 0.12, 0.12, 0.12, 0.14, 0.14]
    cws = [USABLE_W * f for f in cws_raw]
    t = workout_table(headers, rows, cws)
    tw, th = t.wrapOn(c, USABLE_W, 999)
    t.drawOn(c, ML, y - th)
    y -= th + 3*mm

    c.setFont("Helvetica-Oblique", 6.5); c.setFillColor(C_MID)
    c.drawString(ML, y,
                 "Review at end of Week 4: note weight increases and discuss progression with your Personal Trainer.")
    return y - 5*mm


# ── Build PDF ──────────────────────────────────────────────────────────────
cv = canvas.Canvas(OUTPUT, pagesize=A4)

# Page 1
cv.setFillColor(white)
cv.rect(0, 0, PAGE_W, PAGE_H, fill=1, stroke=0)
draw_page1(cv)
cv.showPage()

# Page 2
cv.setFillColor(white)
cv.rect(0, 0, PAGE_W, PAGE_H, fill=1, stroke=0)
draw_page2(cv)
cv.showPage()

# Page 3
cv.setFillColor(white)
cv.rect(0, 0, PAGE_W, PAGE_H, fill=1, stroke=0)
draw_page3(cv)

cv.save()
print("PDF saved:", OUTPUT)

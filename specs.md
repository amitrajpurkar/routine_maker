# Daily Schedule Card — Project Specifications

## 1. Project Intent

This project produces a single-page, print-ready, colour PDF schedule card designed for a first-year Engineering undergraduate student living in a university dorm (UCF) for the first time. The card is intended to be printed in colour, laminated, and affixed to the inside of the student's dorm room door as a daily reference. The objective is to instil discipline, timeliness, and self-sufficiency in a student who is managing his own routine away from home for the first time.

---

## 2. Input Files

| File | Purpose |
|---|---|
| `timeslot_breakdown.md` | Source of truth for every timeslot, its start/end time, and task description |
| `format.md` | Visual and layout requirements for the output PDF |

---

## 3. Schedule Content

The schedule covers a full 24-hour day in 23 slots, running from 05:00 to 21:00 (sleep). All times are expressed in 24-hour (HH:MM) format. Each slot carries a primary task label and, where helpful, a short sub-description with specifics.

| # | Time | Task | Sub-description |
|---|---|---|---|
| 1 | 05:00 | Wake Up Time | — |
| 2 | 05:05 – 05:45 | Personal Hygiene | Brush teeth · wash face · toilet · shave |
| 3 | 05:45 – 06:00 | Dress up for Gym | Walk / cycle to gym |
| 4 | 06:00 – 07:00 | Gym Session | Intensive workout (see gym plan) |
| 5 | 07:00 – 07:15 | Walk back to Dorm | — |
| 6 | 07:15 – 07:30 | Shower & Change | Fresh clothes on! |
| 7 | 07:30 – 08:00 | Prepare & Eat Breakfast | Eggs · milk · protein · fruits · salad |
| 8 | 08:00 – 08:15 | Pack Lunch Box | Sandwich / wrap / salad |
| 9 | 08:15 – 08:30 | Pack Backpack | iPad · keyboard · mouse · headset · chargers |
| 10 | 08:30 – 08:50 | Walk / Cycle to Library | John C. Hitt Library |
| 11 | 08:50 – 09:00 | Arrive at Library | Find quiet spot · settle in |
| 12 | 09:00 – 12:00 | Deep-Dive Time (Morning) | Intensive study · read · work on subjects |
| 13 | 12:00 – 12:30 | Lunch Break | Eat · relax · walk around |
| 14 | 12:30 – 15:00 | Deep-Dive Time (Afternoon) | Subject 2 focus |
| 15 | 15:00 – 16:30 | In-Classroom Lecture (Thursdays) | Or extended study time |
| 16 | 16:30 – 17:00 | Walk Back to Dorm | Change into casual clothes |
| 17 | 17:00 – 17:30 | Dinner Preparation | Check fridge · follow meal plan · note grocery needs |
| 18 | 17:30 – 18:30 | Jogging / Running Time | Track your route · stay consistent |
| 19 | 18:30 – 19:00 | Campus Exploration | Cycle / walk · discover cafes & new spots |
| 20 | 19:00 – 20:00 | Dinner Time | Eat the meal you prepared |
| 21 | 20:00 – 20:15 | Evening Stroll | Walk around dorm · Neptune 157 |
| 22 | 20:15 – 21:00 | Free Time | Chess · checkers · scrabble · cards · Carrom |
| 23 | 21:00 | Lights Out — Sleep Well | 8 hours · consistent schedule every night |

---

## 4. Output Format

- **File type:** PDF
- **Output filename:** `daily_schedule.pdf`
- **Page size:** A4 (210 × 297 mm / 595 × 842 pts)
- **Orientation:** Portrait
- **Background:** Solid white
- **Margins:** Narrow — 8 mm on all four sides
- **Fit:** All 23 schedule cards + title + motivational block must fit on a single page with no overflow

---

## 5. Page Layout

The page is divided into three vertical zones from top to bottom:

### 5.1 Title Zone
- Centred at the top of the page
- Main heading: `🎓 MY DAILY ROUTINE — UNIVERSITY LIFE` — bold, 15pt, olive green (`#27500A`)
- Subtitle: `Stay disciplined · Stay consistent · Own your day` — regular, 8pt, muted grey (`#757575`)

### 5.2 Schedule Cards Zone
- Occupies the bulk of the page between the title and the motivational block
- Contains all 23 timeslot cards stacked vertically
- Cards are distributed evenly across the available height — card height is computed dynamically so all 23 cards fill the space without gaps or overflow
- Inter-card gap: 1.2 mm
- Each card has 2 mm rounded corners

### 5.3 Motivational Block (bottom)
- Fixed height: ~22 mm
- Sits at the bottom of the page above the bottom margin
- Contains a quote, attribution, and a short motivational paragraph
- Text is word-wrapped within the box using a `Frame` + `Paragraph` renderer (not raw `drawString`) to prevent overflow
- Internal top padding: 0.5 pt

---

## 6. Card Design

Each timeslot is rendered as a card (rounded rectangle). Cards have three internal columns:

| Column | Width | Content |
|---|---|---|
| Time | 30 mm | HH:MM or HH:MM – HH:MM in bold |
| Emoji | 7 mm | Contextual emoji icon |
| Label | Remaining width | Primary task name (line 1) + sub-description (line 2, italic, smaller) |

### Label typography
- Primary task name: Helvetica-Bold, up to 8 pt (scaled to card height)
- Sub-description (when present): Helvetica-Oblique, up to 6.8 pt, muted grey (`#555555`)

### Normal card style
- Fill: light grey `#F5F5F5`
- Border: `#BDBDBD`, 0.6 pt stroke
- Time text colour: dark olive `#27500A`

### Key (highlighted) card style
Key tasks are identified by keyword match against: `wake up`, `gym session`, `deep-dive`, `jogging`, `dinner time`

- Fill: light olive `#EAF3DE`
- Border: olive green `#3B6D11`, 1.5 pt stroke
- Left accent bar: 3 mm wide solid olive green strip on the left edge of the card
- Time text colour: olive green `#3B6D11`
- Task label: Helvetica-Bold

---

## 7. Colour Palette (Final — Olive Green theme)

| Role | Hex | Usage |
|---|---|---|
| Accent / border (key) | `#3B6D11` | Key card border, accent bar, quote border |
| Fill (key cards) | `#EAF3DE` | Key card background |
| Text on key cards (time) | `#27500A` | Time column, title, quote text |
| Fill (normal cards) | `#F5F5F5` | Standard card background |
| Border (normal cards) | `#BDBDBD` | Standard card border |
| Body text | `#212121` | Task labels |
| Sub-description text | `#555555` | Italic secondary line in cards |
| Quote block fill | `#FFF8E1` | Warm cream background |
| Subtitle / muted | `#757575` | Page subtitle |

> **Note:** The original design used Rose Magenta (`#C2185B` / `#FCE4EC`). Olive Green was chosen by the user from a presented palette of six options (A–F).

---

## 8. Motivational Block

Located at the very bottom of the page inside a warm cream (`#FFF8E1`) rounded box with an olive green border.

**Quote (bold italic, 7.5 pt, olive green):**
> "Lost time is never found again."

**Attribution (italic, 6.8 pt, olive green):**
> — Benjamin Franklin

**Body text (regular, 6.5 pt, dark, centred, word-wrapped):**
> Every minute of your day is a brick in the foundation of your future. A disciplined routine is not a cage — it is the scaffold on which champions are built. Show up on time, every time. The world rewards those who respect the clock.

Text rendering uses ReportLab's `Paragraph` + `Frame` API (not `canvas.drawString`) to ensure proper word-wrap within the box boundaries.

---

## 9. Technical Implementation

- **Language:** Python 3
- **Library:** ReportLab (`reportlab`)
- **Script:** `generate_schedule.py` (saved in project root)
- **Key ReportLab APIs used:**
  - `canvas.Canvas` — page drawing surface
  - `canvas.roundRect` — card and box backgrounds
  - `Paragraph` + `Frame` — word-wrapped text in the motivational block
  - `ParagraphStyle` — typography definitions for the quote block
- Card height is computed at runtime: `card_h = (available_height - (n-1) * gap) / n`, where `n = 23`, ensuring all cards fill the page exactly regardless of content changes

---

## 10. Project File Structure

```
routine_maker/
├── timeslot_breakdown.md     # Input: raw schedule timeslots and task descriptions
├── format.md                 # Input: layout and visual format requirements
├── generate_schedule.py      # Python script that generates the PDF
├── daily_schedule.pdf        # Output: the final print-ready schedule card
└── specs.md                  # This file: full project specifications
```

---

## 11. Print Instructions

1. Print `daily_schedule.pdf` in **colour** on A4 paper
2. Laminate the printed page
3. Affix to the inside of the dorm room door using glue tape or adhesive strips

---

# Weekly Gym Workout Plan — Specifications

## 12. Project Context

The student attends the UCF Recreation and Wellness Center (RWC) for his morning gym session (06:00–07:00 daily per the daily schedule). He is a beginner building strength and stamina for the first time. In addition to the morning gym session, he commits to a separate one-hour evening cardio block at 17:30–18:30 daily (jogging, running, cycling, or swimming). Morning sessions must therefore be kept at **moderate intensity** — challenging enough to build strength, but not so draining that he lacks energy for the evening activity.

**Facility:** UCF Recreation and Wellness Center — Main Campus
Website: https://rwc.sswb.ucf.edu
Phone: 407-823-2408 | Email: ucfrec@ucf.edu

**RWC Main Facility Hours (Summer 2026):**
Mon–Thu: 06:00–24:00 | Fri: 06:00–21:00 | Sat: 09:00–21:00 | Sun: 12:00–18:00

> The student's 06:00 gym slot fits within Mon–Fri RWC opening hours.

---

## 13. Weekly Workout Structure

### 13.1 Weekly Split

| Day | Focus Area | Intensity |
|---|---|---|
| Monday | Core & Functional Strength | Moderate |
| Tuesday | Upper Body — Push (Chest · Shoulders · Triceps) | Moderate |
| Wednesday | Lower Body (Quads · Hamstrings · Glutes · Calves) | Moderate |
| Thursday | Back Strength (Lats · Traps · Rear Delts) | Moderate |
| Friday | Arms & Biceps (Biceps · Forearms · Light Triceps) | Light–Moderate |
| Saturday | Full Body Light Circuit (Active Gym Day) | Light |
| **Sunday** | **REST DAY — full recovery** | — |

### 13.2 Session Time Breakdown (60 minutes total)

| Phase | Duration | Purpose |
|---|---|---|
| Warm-up | 8–10 min | Raise heart rate, mobilise joints, reduce injury risk |
| Main Workout | 40–45 min | Targeted strength work for the day's muscle group |
| Cool-down & Stretch | 8–10 min | Lower heart rate, static stretches, flexibility |

### 13.3 Beginner Training Parameters

- Sets per exercise: 3
- Reps per set: 12–15 (focus on form, not max weight)
- Rest between sets: 60–90 seconds
- Rest between exercises: 90 seconds
- Progressive overload: increase weight by 2.5–5 lb every 1–2 weeks once form is solid
- Hydrate: bring a full water bottle; drink between every set

---

## 14. Daily Workout Content

### Monday — Core & Functional Strength

**Warm-up (8 min):** 5 min light treadmill walk → dynamic stretches (leg swings, hip circles, arm circles)

**Main (42 min):**
1. Plank — 3 × 45 sec hold
2. Dead Bug — 3 × 12 reps each side
3. Cable Crunch or Crunch Machine — 3 × 15
4. Pallof Press (cable anti-rotation) — 3 × 12 each side
5. Dumbbell Romanian Deadlift (light) — 3 × 12 (core + posterior chain)
6. Bird Dog — 3 × 12 each side
7. Farmer's Carry (dumbbells) — 3 × 30 m walk

**Cool-down (10 min):** Child's pose · cat-cow · lying spinal twist · hip flexor stretch

---

### Tuesday — Upper Body Push (Chest · Shoulders · Triceps)

**Warm-up (8 min):** Arm circles → band pull-aparts → 5 min light rowing machine

**Main (42 min):**
1. Dumbbell Bench Press — 3 × 12
2. Incline Dumbbell Press — 3 × 12
3. Cable Chest Fly — 3 × 15
4. Dumbbell Shoulder Press — 3 × 12
5. Dumbbell Lateral Raise — 3 × 15
6. Tricep Rope Pushdown (cable) — 3 × 15
7. Overhead Dumbbell Tricep Extension — 3 × 12

**Cool-down (10 min):** Chest doorway stretch · shoulder cross-body stretch · tricep overhead stretch

---

### Wednesday — Lower Body (Quads · Hamstrings · Glutes · Calves)

**Warm-up (8 min):** 5 min bike (easy pace) → leg swings → bodyweight squats × 10

**Main (42 min):**
1. Goblet Squat (dumbbell) — 3 × 15
2. Leg Press Machine — 3 × 12
3. Dumbbell Walking Lunge — 3 × 10 each leg
4. Seated Leg Curl Machine — 3 × 12
5. Glute Bridge (bodyweight or barbell) — 3 × 15
6. Standing Calf Raise (machine or Smith) — 3 × 20
7. Step-Ups (box, dumbbell in each hand) — 3 × 10 each leg

**Cool-down (10 min):** Quad stretch · hamstring stretch · pigeon pose · calf stretch on wall

---

### Thursday — Back Strength (Lats · Traps · Rear Delts)

**Warm-up (8 min):** 5 min rowing machine (light) → cat-cow × 10 → shoulder rotations

**Main (42 min):**
1. Lat Pulldown (cable) — 3 × 12
2. Seated Cable Row — 3 × 12
3. Dumbbell Single-Arm Row — 3 × 12 each side
4. Face Pull (cable rope) — 3 × 15
5. Dumbbell Bent-Over Rear Delt Fly — 3 × 15
6. Shrugs (dumbbell) — 3 × 15
7. TRX Row or Assisted Pull-Up Machine — 3 × 10

**Cool-down (10 min):** Lat stretch (hanging or doorway) · child's pose · thoracic rotation stretch

---

### Friday — Arms & Biceps (Biceps · Forearms · Light Triceps)

**Warm-up (8 min):** 5 min light elliptical → wrist circles → arm swings

**Main (42 min):**
1. Dumbbell Bicep Curl — 3 × 15
2. Hammer Curl — 3 × 15
3. Cable Bicep Curl — 3 × 15
4. Incline Dumbbell Curl — 3 × 12
5. Barbell or EZ-Bar Curl — 3 × 12
6. Wrist Curls (dumbbell, seated) — 3 × 20
7. Tricep Overhead Rope Extension (cable) — 3 × 15 (light, keeps arms balanced)

**Cool-down (10 min):** Bicep wall stretch · wrist flexor/extensor stretch · forearm massage roll

---

### Saturday — Full Body Light Circuit (Active Recovery Day)

**Warm-up (8 min):** 5 min walk/jog on treadmill → full body dynamic stretch

**Main Circuit (42 min) — 3 rounds, 45 sec work / 15 sec rest each:**
1. Bodyweight Squat
2. Push-Up (or knee push-up)
3. TRX Row
4. Reverse Lunge (bodyweight)
5. Plank Hold
6. Dumbbell Shoulder Press (light)
7. Jumping Jacks or Step Touches (low impact cardio)

**Cool-down (10 min):** Full body stretch routine — hold each stretch 30 sec

---

### Sunday — REST DAY

No gym. Prioritise sleep, light walking, hydration, and nutrition. The body builds muscle during recovery, not during the workout.

---

## 15. Evening Cardio Session (Separate — 17:30–18:30)

This is an additional daily commitment and is NOT part of the morning gym session. The student rotates between the following activities:

| Activity | Where at UCF |
|---|---|
| Jogging / Running | Campus running paths, RWC Park |
| Cycling | Campus cycle routes |
| Swimming | RWC Lap Pool (Mon–Fri: 06:00–19:00, Sat–Sun: 11:00–17:00) |

> Because of this double-session day, morning gym sessions are intentionally kept at **moderate load** — heavy compound lifts (deadlifts, barbell squats at max) are deliberately avoided to preserve energy and prevent overtraining.

---

## 16. RWC Instructor-Led Sessions for Beginners

The following programmes at UCF RWC are specifically suited for a beginner who wants to build strength, stamina, and fitness:

### 16.1 Fitness Assessment (Strongly Recommended — Start Here)
- **What it is:** A one-on-one session with a Certified Personal Trainer who conducts a complete baseline measurement of your fitness level — including body composition analysis — and provides personalised recommendations.
- **Why it matters:** Knowing your starting point helps you track progress and set realistic goals.
- **How to book:** Sign up at https://ucf.qualtrics.com/jfe/form/SV_2uFJIOmriZfGWhw
- **Locations:** RWC Main (Floor 1, adjacent to Basketball Court #1) · RWC Downtown (Room 264)

### 16.2 Personal Training
- **What it is:** One-on-one sessions with a nationally certified trainer (ACE, ACSM, ISSA, NASM, or NSCA). Trainers build a custom program around the student's specific goals and health factors.
- **How to start:** New clients complete an Initial Consultation (fitness assessment + goal-setting) first. Visit the Personal Training Packages page for registration forms and rates.
- **Availability:** RWC Main — by appointment only | RWC Downtown — walk-ins welcome during hours of operation
- **Contact:** fitness@ucf.edu | 407-823-2408

### 16.3 Group Exercise Classes (Free for UCF Students)
The RWC runs 60+ instructor-led group classes per week. Formats relevant to a beginner building strength and stamina:

| Class Format | Best for |
|---|---|
| KnightFit | Functional training, full-body strength + cardio — great beginner class |
| Cycle / Cycle + Strength | Low-impact cardio + leg strength |
| HIIT | High-intensity intervals, builds stamina (start after 4–6 weeks of base fitness) |
| Barre | Core, balance, and lower body stability |
| Pilates | Core strength, posture, flexibility |
| Yoga | Flexibility, recovery, breathing, mental focus |

- **How to reserve:** Visit https://ucfrwc.org → sign in with UCF NID → book up to 24h before class
- **Arrive:** At least 15 min early to secure reserved spot
- **Cost:** Free for enrolled UCF students
- **Contact:** fitness@ucf.edu

### 16.4 Strength & Conditioning (For Later — Once Base Fitness is Established)
Once the student has built a consistent base (approx. 8–12 weeks in), the RWC offers Strength & Conditioning programmes focused on speed, agility, coordination, and technique. Requires minimum group size; contact fitness@ucf.edu for details.

---

## 17. Workout Plan Output Files

| File | Format | Print |
|---|---|---|
| `weekly_workout_plan.pdf` | A4 PDF | Black & white printable |
| `weekly_workout_plan.md` | Markdown | Interactive — for editing and updates |

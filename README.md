# Routine Maker — UCF Student Life Planner

A Claude Cowork project for managing your daily schedule, weekly gym workout plan, and weekly meal plan as a first-year Engineering student at UCF.

---

## What's in This Project

| File / Folder | What it is |
|---|---|
| `OUTPUTS/daily_schedule.pdf` | Colour print-ready daily schedule card (door poster) |
| `OUTPUTS/weekly_workout_plan.pdf` | B&W printable weekly gym plan (3 pages) |
| `OUTPUTS/weekly_meal_plan.pdf` | B&W printable weekly meal plan (landscape, 1 page) |
| `INPUTS/weekly_workout_plan.md` | Your interactive workout plan — edit and ask Claude to update |
| `INPUTS/weekly_meal_input.md` | Your weekly grocery & meal preference input — fill before each Publix run |
| `INPUTS/specs.md` | Full project specifications (reference document) |
| `INPUTS/timeslot_breakdown.md` | Your daily schedule timeslots (source of truth) |
| `INPUTS/format.md` | Visual format rules for the daily schedule card |
| `generate_schedule.py` | Script that generates `daily_schedule.pdf` |
| `generate_workout.py` | Script that generates `weekly_workout_plan.pdf` |
| `generate_meal_plan.py` | Script that generates `weekly_meal_plan.pdf` |

---

## Part 1 — Getting the Project on Your Machine

### Step 1: Install Git
If you don't already have Git installed, download it from https://git-scm.com and follow the installer.

To verify: open Terminal (Mac) or Command Prompt (Windows) and run:
```bash
git --version
```

### Step 2: Clone the Repository
Navigate to where you want to store the project on your machine, then run:
```bash
git clone git@github.com:amitrajpurkar/routine_maker.git
```
Replace `<your-repo-url>` with the actual GitHub repository URL (e.g. `https://github.com/yourusername/routine_maker.git`).

This creates a `routine_maker` folder on your computer with all the files.

### Step 3: Pull Updates (When Changes Are Made)
If the project has been updated and you want to sync your local copy:
```bash
cd routine_maker
git pull
```

### Step 4: Push Your Changes Back to GitHub
After you make edits (to input files, preferences, etc.) and want to save them:
```bash
cd routine_maker
git add .
git commit -m "Updated meal input for this week"
git push
```

---

## Part 2 — Opening This Project in Claude Desktop (Cowork)

### Step 1: Install Claude Desktop
Download Claude Desktop from https://claude.ai/download and sign in with your Anthropic account.

### Step 2: Open Cowork Mode
In Claude Desktop, click the **Cowork** icon or open a new Cowork session. Cowork is the mode that gives Claude direct access to your files so it can read, edit, and generate documents for you.

### Step 3: Connect Your Project Folder
When Cowork asks you to select a folder (or click **"Select folder"** / **"Connect folder"**), navigate to the `routine_maker` folder you cloned in Part 1 and select it.

Claude will now have access to all the files in this project and can read, edit, and regenerate any of your plans.

### Step 4: You're Ready
You can now talk to Claude in plain English. Examples of things you can say:
- *"Show me my weekly meal plan"*
- *"I updated my meal input file — regenerate my meal plan PDF"*
- *"Change my gym session on Friday to a rest day"*
- *"Add 15 minutes of meditation to my daily schedule after waking up"*

---

## Part 3 — Adjusting Your Daily Schedule

Your daily schedule is driven by two input files:

- **`INPUTS/timeslot_breakdown.md`** — the list of every timeslot and what happens in it
- **`INPUTS/format.md`** — the visual style rules for the printed card

### How to make changes

**Option A — Tell Claude directly (easiest):**
Open Cowork and say something like:
> *"Move my gym session from 06:00 to 06:30 and shift everything after it by 30 minutes."*
> *"Add a 15-minute journaling block after dinner."*
> *"Change my library arrival time to 09:15."*

Claude will update `timeslot_breakdown.md` and regenerate `OUTPUTS/daily_schedule.pdf` for you.

**Option B — Edit the file yourself:**
Open `INPUTS/timeslot_breakdown.md` in any text editor, make your changes to the timeslots and descriptions, save the file, then tell Claude:
> *"I updated my timeslot file. Please regenerate the daily schedule PDF."*

**Tip:** After any change to the daily schedule, print the new PDF in colour, laminate it, and replace the one on your door.

---

## Part 4 — Adjusting Your Weekly Workout Plan

Your workout plan lives in two places:

- **`INPUTS/weekly_workout_plan.md`** — the full interactive markdown version you can read and edit
- **`OUTPUTS/weekly_workout_plan.pdf`** — the printable B&W PDF (regenerated from the markdown)

### How to make changes

**Option A — Tell Claude directly:**
> *"Replace Monday's core workout with an upper body push day."*
> *"I want to add pull-ups to my Thursday back workout."*
> *"Swap Saturday's light circuit for a rest day and move Sunday's rest to Saturday."*
> *"I've been at this for 6 weeks — can you make the plan more challenging?"*

Claude will update `INPUTS/weekly_workout_plan.md` and regenerate the PDF.

**Option B — Edit the markdown yourself:**
Open `INPUTS/weekly_workout_plan.md`, tick off completed workouts, note the weights you used, make any changes you want to exercises or structure, then tell Claude:
> *"I've made some edits to my workout markdown. Please regenerate the workout plan PDF."*

**Option C — Use the 4-week tracker in the PDF:**
The last page of `weekly_workout_plan.pdf` has a progress tracker. Print it, tick off each session as you complete it, note weight increases, and at the end of 4 weeks bring the notes back to Claude:
> *"It's been 4 weeks. I've been increasing weight on most exercises. Can you progress my plan to Phase 2?"*

---

## Part 5 — Adjusting Your Weekly Meal Plan

Your meal plan uses a dedicated input file designed for weekly updates:

- **`INPUTS/weekly_meal_input.md`** — fill this in before every Publix trip
- **`OUTPUTS/weekly_meal_plan.pdf`** — the printable meal plan (regenerated from your input)

### The weekly update loop (every Tuesday or Wednesday)

1. **Open `INPUTS/weekly_meal_input.md`** in any text editor or ask Claude to open it.

2. **Fill in the sections:**
   - **Section 2 — Current Stock:** tick off what you still have in your fridge, freezer, and pantry
   - **Section 3 — Shopping List:** list what you need to buy at Publix this week
   - **Section 4 — Meal Preferences:** note any changes to breakfast, lunch, snack, or dinner for the week
   - **Section 5 — Notes for Claude:** anything else (e.g. "I have a friend over Saturday", "no tuna this week", "I'm out of tortillas")

3. **Save the file**, then tell Claude:
   > *"I've updated my meal input file for this week. Please adjust my meal plan and regenerate the PDF."*

4. Claude reads your input, adapts the meal plan around what you have and what you want, and saves the updated PDF to `OUTPUTS/weekly_meal_plan.pdf`.

5. Print the new meal plan and stick it inside your fridge or on the wall above your desk.

### Quick meal-related things you can ask Claude
> *"I only have 2 Ready Rice packets left — plan around that."*
> *"I don't want tuna this week, replace it with canned chicken."*
> *"Add a protein shake to my daily snack."*
> *"What can I make for dinner tonight with just chicken strips, rice, and frozen broccoli?"*
> *"I'm really busy this week — give me the simplest possible dinners."*

---

## Part 6 — Project Folder Structure

```
routine_maker/
├── README.md                    ← you are here
├── INPUTS/
│   ├── timeslot_breakdown.md    ← edit to change daily schedule
│   ├── format.md                ← visual rules for schedule card
│   ├── specs.md                 ← full project specifications
│   ├── weekly_workout_plan.md   ← interactive workout plan
│   └── weekly_meal_input.md     ← fill in weekly before grocery run
├── OUTPUTS/
│   ├── daily_schedule.pdf       ← print in colour, laminate, door poster
│   ├── weekly_workout_plan.pdf  ← print B&W, 3 pages
│   └── weekly_meal_plan.pdf     ← print B&W, 1 page landscape
├── generate_schedule.py         ← regenerates daily_schedule.pdf
├── generate_workout.py          ← regenerates weekly_workout_plan.pdf
└── generate_meal_plan.py        ← regenerates weekly_meal_plan.pdf
```

---

## Quick Reference — What to Say to Claude

| What you want | What to say |
|---|---|
| Change a timeslot | *"Move [task] from [time] to [new time]"* |
| Regenerate daily schedule PDF | *"Regenerate my daily schedule PDF"* |
| Change a gym exercise | *"Replace [exercise] on [day] with [new exercise]"* |
| Make workout harder | *"I've been training for X weeks — progress my workout plan"* |
| Regenerate workout PDF | *"Regenerate my workout plan PDF"* |
| Weekly meal update | *"I updated my meal input file — regenerate my meal plan"* |
| Quick dinner idea | *"What can I microwave for dinner with [ingredients]?"* |
| Grocery help | *"I'm going to Publix — what do I need based on this week's plan?"* |

---

## Tips for Getting the Most Out of Claude in This Project

- **Be specific** — instead of "change my workout", say "add face pulls to Thursday's back day and remove shrugs"
- **Reference the files by name** — Claude knows where everything lives in this project
- **Update your input files regularly** — the meal plan and workout plan get smarter as you give Claude more real information about what you have and how you're progressing
- **Ask Claude to explain** — if you don't know what an exercise is or why a meal was chosen, just ask

---

*Project built with Claude Cowork · UCF Engineering Student · Neptune 157 · 2026*

# Habit Tracker CLI

A command-line habit tracker written in Python.
This project demonstrates building a small persistent CLI application using argparse, JSON storage, and datetime-based streak tracking.

## Features

* Create and track multiple habits
* Log updates with automatic timestamps
* Attach flexible metadata to updates
* Automatic streak calculation (24‑hour window)
* Optional colored CLI output
* Rainbow streak indicator for active streaks
* JSON‑based persistent storage
* Modular CLI architecture

## Project Architecture

The project is intentionally split into layers to demonstrate clean CLI design.

```
main.py      → CLI argument parsing
tracker.py   → business logic and data handling
display.py   → formatted CLI output
colors.py    → color helpers and rainbow styling
```

This structure makes the logic reusable and keeps presentation separate from data operations.


## Installation

Clone the repository:

```bash
git clone https://github.com/yuvrajpuri/portfolio.git
cd portfolio/habit_tracker_cli
```

Install dependencies:
```cmd
pip install -r requirements.txt
```

# Usage

All commands are run through `main.py`.

## Create a Habit

```bash
python main.py create reading
```

---

## Update a Habit

```bash
python main.py update reading
```

Each update automatically logs a timestamp.

---

## Update With Metadata

Metadata can be attached to any update.

```bash
python main.py update reading --meta mood focused
```

Multiple metadata entries can be provided:

```bash
python main.py update reading --meta mood great --meta location library
```

---

## List Habits

View a summary of all habits:

```bash
python main.py list
```

Example output:

```
reading
  Streak: 4
  Last logged: 2026-03-15T19:04:20+00:00
```

---

## View Detailed Habit Information

```bash
python main.py list reading
```

Example output:

```
Habit: reading
🔥 Streak: 4 🔥

Logs: 4
  2026-03-12T20:00:12+00:00
  2026-03-13T20:04:55+00:00
  2026-03-14T20:10:03+00:00
  2026-03-15T19:04:20+00:00

Metadata:
  mood: ['focused', 'great']
```

---

# Color Output

Color output is enabled by default.

Disable it using:

```bash
python main.py -nc list
```

or

```bash
python main.py --no-color list
```

---

## Streak Logic

A streak is counted when consecutive updates occur within **24 hours** of each other.

Rules:

* Updates must occur within a 24‑hour window
* Streaks shorter than **3 entries return 0**
* Active streaks trigger a **rainbow display** in the CLI


## Data Format

Habit data is stored locally in `data.json`:

```
{
  "habit": {
    "reading": {
      "created": "2026-03-15",
      "logs": [],
      "metadata": {}
    }
  }
}
```

# Testing

Tests are written using **pytest** and validate:

* habit creation
* duplicate handling
* update logging
* metadata storage
* streak logic

Run tests with:

```bash
pytest
```

---
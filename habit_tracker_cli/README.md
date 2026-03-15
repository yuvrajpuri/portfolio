# Habit Tracker CLI

A command-line habit tracker written in Python.
This project demonstrates building a small persistent CLI application using argparse, JSON storage, and datetime-based streak tracking.

## Concepts Demonstrated

* Command-line interfaces with `argparse`
* JSON-based data persistence
* Datetime parsing and timezone handling
* Streak calculation logic
* Flexible metadata storage using dictionaries
* Modular helper functions

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

## Running the Program

From the project directory:

```
python tracker.py create reading
```

## Example Commands

Create a habit:

```
python tracker.py create reading
```

Update a habit:

```
python tracker.py update reading
```

Update with metadata:

```
python tracker.py update reading --meta mood focused
```

Add multiple metadata entries:

```
python tracker.py update reading --meta mood great --meta location library
```

List habits:

```
python tracker.py list
```

View detailed habit information:

```
python tracker.py list reading
```

## Example Output

```
reading
    Streak: 4
    Last logged: 2026-03-15T19:04:20+00:00
```

## Streak Logic

A streak is counted when consecutive habit updates occur within **24 hours** of each other.

Streaks shorter than **3 entries return 0**, preventing accidental short streaks.

## Running Tests

Run the test suite with:

```cmd
python -m pytest -v
```

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
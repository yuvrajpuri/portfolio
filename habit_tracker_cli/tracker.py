# Problem: Make Habit tracker - track your habits that you've created. Do this as a way of taking accountability for yourself.
# Features: make it capable of tracking multiple habits; make it capable of giving a satisfying output; make it keep logs / metadata you track

import argparse
import json
import os
from datetime import date
import datetime

DATA_FILE = "data.json"

def create_habit(habit: str):
    # json_string = json.dumps(data)        If we dump a json_string, it adds backslashes to the result
    
    # Step 1: check for already existing habits
    if os.path.exists(DATA_FILE):
        try:
            with open(DATA_FILE, "r", encoding="utf-8") as file:
                current_data = json.load(file)      # Get already existing data
                print(f"Prior data found: {current_data}")
                if not isinstance(current_data, dict):
                    raise ValueError("JSON root must be a dictionary.")
        except (json.JSONDecodeError, ValueError) as e:
            print(f"Error reading JSON: {e}. Starting with empty dictionary")
            current_data = {}       # Make empty dict to start

        # Step 2: Make new habit
        if "habit" not in current_data or not isinstance(current_data["habit"], dict):
            current_data["habit"] = {}      # Turn it to dict

        if habit in current_data["habit"]:
            print(f"Habit '{habit}' already exists.")
            return

        current_data["habit"][habit] = {}     # Make new habit dict
        current_data["habit"][habit].update(
            {
            "created": date.today().isoformat(),
            "logs": [],
            "metadata": {},
            }
        )


        # Step 3: write it back to the file - we essentially overwrite it
        try:
            save_tracker(current_data)
            
            print("data.json updated successfully.")
        except OSError as e:
            print(f"Error writing to file: {e}")

    # Step 1b: if it doesn't exist, make a brand new one with your brand new habit.
    else:
        print("data.json doesn't exist - making something new instead.")
        data = {
            "habit": {
                habit: {
                    "created": date.today().isoformat(),
                    "logs": [],
                    "metadata": {},
                }
            }
        }
        save_tracker(data)

def get_habits() -> dict:
    if os.path.exists(DATA_FILE):
        try:
            with open(DATA_FILE, "r") as file:
                return json.load(file)
        except Exception as e:
            print(f"Error in reading file: {e}")
            return
    else:
        raise OSError("data.json not found")


def update_habit_date(habit: str, tracker: dict) -> None:
    """
    Helper function. 
    When we make an update to the habit, it also adds the date the change occurred to the logs.
    """
    tracker["habit"][habit].setdefault("logs", [])
    tracker["habit"][habit]["logs"].append(datetime.datetime.now().astimezone().isoformat())

def update_habit_metadata(habit: str, tracker: dict, **kwargs) -> None:
    """
    Helper function. Add metadata entries to a habit.
    If the key is already there, append it to its list. 
    """

    # Ensure metadata exists
    metadata = tracker["habit"][habit].setdefault("metadata", {})

    # Start going through the kwargs
    for key, value in kwargs.items():
        
        # convert date format in case it is a date
        if isinstance(value, (datetime.date, datetime.datetime)):
            value = value.isoformat()
            
        # make sure the metadata key exists
        metadata.setdefault(key, [])

        # append the new value to it
        metadata[key].append(value)

def save_tracker(tracker: dict) -> None:
    """Saves the tracker data, overwriting the data.json"""
    with open(DATA_FILE, "w",encoding="utf-8") as file:
        json.dump(tracker, file, indent=4, ensure_ascii=False)

def update_tracker(habit: str, **kwargs) -> None:
    """
    Update the habit tracker for a specific habit. 
    You can add keyword arguments to this, but every update's datetime is logged no matter what.
    """

    tracker = get_habits()      # Already does the check for if the path exists

    if habit not in tracker["habit"]:       # Check if your habit exists
        print("Habit not found.")
        return

    # Always update the date log - means an update occurred even if you don't have anything to report
    update_habit_date(habit, tracker)

    if kwargs:
        update_habit_metadata(habit, tracker, **kwargs)
    save_tracker(tracker)

def return_streak(habit: str, tracker: dict) -> int:
    """
    Return current log update streak. Return 0 unless:
    The streak is longer than 2 and that the entries are within 24 hours of each other.
    """

    # check if the logs exist first
    logs = tracker["habit"][habit].get("logs", [])
    if not logs:
        return 0
    
    dates = [datetime.datetime.fromisoformat(log) for log in logs]
    dates.sort(reverse=True)
    streak = 1
    
    for i in range(len(dates) - 1):
        delta = dates[i] - dates[i+1]

        if delta <= datetime.timedelta(hours=24):
            streak+=1
        else:
            break
    
    return streak if streak > 2 else 0

def parse_value(value: str):
    """
    Attempt to convert CLI string values into useful Python types.
    """

    # Try datetime first
    try:
        return datetime.datetime.fromisoformat(value)
    except ValueError:
        pass

    # Try date
    try:
        return datetime.date.fromisoformat(value)
    except ValueError:
        pass

    # Otherwise leave as string
    return value

def list_habits(habit: str | None = None) -> None:
    tracker = get_habits()

    if not tracker or "habit" not in tracker:
        print("No habits found.")
        return
    
    if habit:
        if habit not in tracker["habit"]:
            print("Habit not found.")
            return

        streak = return_streak(habit, tracker)
        logs = tracker["habit"][habit].get("logs", [])
        metadata = tracker["habit"][habit].get("metadata", {})

        # All the data about a given habit
        print(f"Habit : {habit}")
        print(f"Streak: {streak}")
        print(f"Logs: {len(logs)}")
        for log in logs:
            print(f"\t{log}")
        print("\nMetadata:")
        for key, values in metadata.items():
            print(f"\t{key}: {values}")
        
        return


    # If habit is not specified
    for habit_name in sorted(tracker["habit"]):
        streak = return_streak(habit_name, tracker)

        logs = tracker["habit"][habit_name].get("logs", [])
        last_log = logs[-1] if logs else "Never"

        print(f"{habit_name}")
        print(f"\tStreak: {streak}")
        print(f"\tLast logged: {last_log}")
        print()
        

def main():
        # Argument parsers
    parser = argparse.ArgumentParser(description="Habit Tracker CLI")

    subparsers = parser.add_subparsers(dest="command")

    # create command
    create_parser = subparsers.add_parser("create", help="Create a new habit")
    create_parser.add_argument("habit")

    # update command
    update_parser = subparsers.add_parser("update", help="Update a habit")
    update_parser.add_argument("habit")
    update_parser.add_argument(
        "--meta",
        nargs=2,
        action="append",
        metavar=("KEY", "VALUE"),
        help="Add metadata entries"
    )

    # list command
    list_parser = subparsers.add_parser("list", help="List habits")
    list_parser.add_argument("habit", nargs="?", default=None)
    args = parser.parse_args()

    if args.command == "create":
        create_habit(args.habit)

    elif args.command == "update":
        kwargs = {}

        if args.meta:
            for key, value in args.meta:
                kwargs[key] = parse_value(value)

        update_tracker(args.habit, **kwargs)

    elif args.command == "list":
        list_habits(args.habit)

    else:
        parser.print_help()


if __name__ == "__main__":
    main()
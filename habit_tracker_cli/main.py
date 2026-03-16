import argparse
import tracker
from display import Display


def main():

    # Argument parser
    parser = argparse.ArgumentParser(description="Habit Tracker CLI")

    parser.add_argument(
        "--no-color",
        "-nc",
        action="store_true",
        help="Disable colored output"
    )

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

    # Initialize display layer
    display = Display(use_color=not args.no_color)

    # -----------------------------
    # CREATE
    # -----------------------------
    if args.command == "create":

        created = tracker.create_habit(args.habit)

        if created:
            display.habit_created(args.habit)
        else:
            display.habit_duplicate(args.habit)

    # -----------------------------
    # UPDATE
    # -----------------------------
    elif args.command == "update":

        metadata = {}

        if args.meta:
            for key, value in args.meta:
                metadata[key] = tracker.parse_value(value)

        success = tracker.update_tracker(args.habit, **metadata)

        if success:
            display.habit_updated(args.habit)
        else:
            display.habit_not_found(args.habit)

    # -----------------------------
    # LIST
    # -----------------------------
    elif args.command == "list":

        data = tracker.list_habits(args.habit)

        if args.habit:
            display.show_habit(data)
        else:
            display.list_habits(data)

    else:
        parser.print_help()


if __name__ == "__main__":
    main()
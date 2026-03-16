import coloring


class Display:
    """
    Handles all CLI output formatting for the habit tracker.
    """

    def __init__(self, use_color: bool = True):
        self.use_color = use_color

    def _print(self, text: str, section: str | None = None):
        """
        Internal print helper that applies color if enabled.
        """
        if self.use_color and section:
            print(coloring.color_text(text, section))
        else:
            print(text)

    # -----------------------------
    # Status Messages
    # -----------------------------

    def habit_created(self, habit: str):
        self._print(f"✔ Habit '{habit}' created", "success")

    def habit_duplicate(self, habit: str):
        self._print(f"Habit '{habit}' already exists", "error")

    def habit_not_found(self, habit: str):
        self._print(f"Habit '{habit}' not found", "error")

    def habit_updated(self, habit: str):
        self._print(f"✔ Habit '{habit}' updated", "success")

    # -----------------------------
    # List All Habits
    # -----------------------------

    def list_habits(self, habits: list):
        """
        Display summary view of all habits.
        """

        if not habits:
            self._print("No habits found.", "error")
            return

        for habit in habits:

            name = habit["habit"]
            streak = habit["streak"]
            last_log = habit["last_log"] or "Never"

            self._print(name, "header")
            self._print(f"\tStreak: {streak}", "created")
            self._print(f"\tLast logged: {last_log}", "log")

            print()

    # -----------------------------
    # Detailed Habit View
    # -----------------------------

    def show_habit(self, habit_data: dict):
        """
        Display detailed information about a single habit.
        """

        if not habit_data:
            self._print("Habit not found.", "error")
            return

        name = habit_data["habit"]
        streak = habit_data["streak"]
        logs = habit_data["logs"]
        metadata = habit_data["metadata"]

        self._print(f"Habit: {name}", "header")

        # Rainbow streak mode
        if streak >= 3 and self.use_color:
            print(coloring.rainbow_text(f"🔥 Streak: {streak} 🔥"))
        else:
            self._print(f"Streak: {streak}", "created")

        self._print(f"Logs: {len(logs)}", "log")

        for log in logs:
            self._print(f"\t{log}", "log")

        if metadata:
            self._print("\nMetadata:", "meta")

            for key, values in metadata.items():
                self._print(f"\t{key}: {values}", "meta")
from colorama import Fore, Style, init

init(autoreset=True)

COLORS = {
    "header": Fore.MAGENTA + Style.BRIGHT,
    "created": Fore.CYAN,
    "log": Fore.GREEN,
    "meta": Fore.YELLOW,
    "error": Fore.RED + Style.BRIGHT,
    "success": Fore.GREEN + Style.BRIGHT,
    "default": Style.RESET_ALL
}

def cprint(text: str, section: str = "default"):
    """Print text using a predefined color section."""
    color = COLORS.get(section, COLORS["default"])
    print(color + str(text))

def color_text(text: str, section: str = "default") -> str:
    """Return colored text instead of printing."""
    color = COLORS.get(section, COLORS["default"])
    return color + str(text)

RAINBOW = [
    Fore.RED,
    Fore.YELLOW,
    Fore.GREEN,
    Fore.CYAN,
    Fore.BLUE,
    Fore.MAGENTA,
]

def rainbow_text(text: str) -> str:
    """Return rainbow-colored text."""
    colored = ""

    for i, char in enumerate(text):
        colored += RAINBOW[i % len(RAINBOW)] + char

    return colored

def streak_banner(streak: int):
    """Print a rainbow streak banner."""
    message = f"🔥 STREAK ACTIVE: {streak} 🔥"
    print(rainbow_text(message))


# Helper functions for automatically printing results with the coloring
def header(text):
    cprint(text, "header")


def created(text):
    cprint(text, "created")


def log(text):
    cprint(text, "log")


def metadata(text):
    cprint(text, "meta")


def success(text):
    cprint(text, "success")


def error(text):
    cprint(text, "error")
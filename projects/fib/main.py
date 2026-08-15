import os
import subprocess as sub
import re
import shutil
from typing import Any

# Try to use colorama on Windows for reliable colors; fall back to ANSI codes.
try:
    import colorama

    colorama.init()
    from colorama import Fore, Style

    COLORS: dict[str, str] = {
        "RED": Fore.RED,
        "GREEN": Fore.GREEN,
        "YELLOW": Fore.YELLOW,
        "CYAN": Fore.CYAN,
        "MAGENTA": Fore.MAGENTA,
        "WHITE": Fore.WHITE,
        "DIM": Fore.LIGHTBLACK_EX,
        "RESET": Style.RESET_ALL,
    }
except ImportError:
    COLORS: dict[str, str] = {
        "RED": "\u001b[31m",
        "GREEN": "\u001b[32m",
        "YELLOW": "\u001b[33m",
        "CYAN": "\u001b[36m",
        "MAGENTA": "\u001b[35m",
        "WHITE": "\u001b[37m",
        "DIM": "\u001b[90m",
        "RESET": "\u001b[0m",
    }

try:
    import gmpy2
except ImportError:
    gmpy2: Any = None


def clear() -> None:
    """Clear the terminal screen on Windows or Unix."""
    cmd = "cls" if os.name == "nt" else "clear"
    sub.run(cmd, shell=True)


def fib(n: int) -> int:
    """Fast Fibonacci calculation for n >= 0, using gmpy2 when available."""
    if n < 0:
        raise ValueError("Input must be a non-negative integer.")

    if gmpy2 is not None:
        return int(gmpy2.fib(n))

    def _fib_pair(k: int) -> tuple[int, int]:
        if k == 0:
            return 0, 1
        a, b = _fib_pair(k >> 1)
        c = a * ((b << 1) - a)
        d = a * a + b * b
        if k & 1:
            return d, c + d
        return c, d

    return _fib_pair(n)[0]


def strip_ansi(s: str) -> str:
    """Remove ANSI escape sequences for accurate width calculations."""
    return re.sub(r"\x1b\[[0-9;]*m", "", s)


def boxed_text(lines: list[str], width: int | None = None) -> str:
    """Draw a box around the provided lines. Width auto-adapts to terminal size if not provided."""
    clean_lines = [strip_ansi(line) for line in lines]
    content_width = max((len(line) for line in clean_lines), default=0)
    term_width = shutil.get_terminal_size((80, 20)).columns

    # decide final width (including box borders)
    target_inner = content_width + 2  # padding inside
    if width is None:
        inner = min(max(target_inner, 10), max(10, term_width - 4))
    else:
        inner = min(width - 2, term_width - 4)
    horizontal = "─" * inner

    output = [f"┌{horizontal}┐"]
    for line in lines:
        clean = strip_ansi(line)
        # pad based on clean length, keep original coloring at left
        padded_colored = line + " " * (inner - len(clean))
        output.append(f"│{padded_colored}│")
    output.append(f"└{horizontal}┘")
    return "\n".join(output)


def print_banner() -> None:
    banner = [
        f"{COLORS['CYAN']}╔══════════════════════════════════════════╗{COLORS['RESET']}",
        f"{COLORS['CYAN']}║{COLORS['WHITE']}          Fibonacci TUI Explorer         {COLORS['CYAN']}║{COLORS['RESET']}",
        f"{COLORS['CYAN']}╚══════════════════════════════════════════╝{COLORS['RESET']}",
        "",
        f"{COLORS['MAGENTA']}Interactive terminal Fibonacci calculator with sequence preview and result styling.{COLORS['RESET']}",
    ]
    print("\n".join(banner))


def print_options() -> None:
    print()
    print(f"{COLORS['YELLOW']}Choose a mode:{COLORS['RESET']}")
    print(f"  {COLORS['GREEN']}1{COLORS['RESET']}. Single Fibonacci number")
    print(f"  {COLORS['GREEN']}2{COLORS['RESET']}. Full sequence to N")
    print(f"  {COLORS['GREEN']}3{COLORS['RESET']}. Quit")


def prompt_choice(prompt: str, valid: set[str]) -> str:
    while True:
        choice = input(f"{COLORS['CYAN']}{prompt}{COLORS['RESET']} ").strip()
        if choice in valid:
            return choice
        print(
            f"{COLORS['RED']}Please enter one of: {', '.join(sorted(valid))}.{COLORS['RESET']}"
        )


def prompt_int(prompt: str) -> int:
    while True:
        raw = input(f"{COLORS['CYAN']}{prompt}{COLORS['RESET']} ").strip()
        if not raw:
            print(
                f"{COLORS['RED']}Input cannot be empty. Enter a non-negative integer.{COLORS['RESET']}"
            )
            continue
        if raw.lower() in {"q", "quit", "exit"}:
            raise KeyboardInterrupt
        if raw.isdigit():
            value = int(raw)
            return value
        print(
            f"{COLORS['RED']}Invalid input. Please enter a non-negative integer.{COLORS['RESET']}"
        )


def format_int(v: int) -> str:
    """Human-friendly integer formatting with commas."""
    try:
        return f"{v:,}"
    except Exception:
        return str(v)


def show_result(n: int, value: int) -> None:
    lines = [
        f"Fibonacci number at position {COLORS['YELLOW']}{n}{COLORS['RESET']}",
        "",
        f"{COLORS['GREEN']}{format_int(value)}{COLORS['RESET']}",
    ]
    box = boxed_text(lines)
    print()
    print(box)


def show_sequence(n: int, sequence: list[int]) -> None:
    header = [f"Full sequence to position {COLORS['YELLOW']}{n}{COLORS['RESET']}", ""]
    entries = [
        f"{i:>3}: {COLORS['GREEN']}{format_int(value)}{COLORS['RESET']}"
        for i, value in enumerate(sequence)
    ]

    term_lines = shutil.get_terminal_size((80, 20)).lines
    page_size = max(8, term_lines - 8)
    total = len(entries)
    page = 0

    while True:
        start = page * page_size
        end = min(start + page_size, total)
        page_lines = header + entries[start:end]
        print()
        print(boxed_text(page_lines))
        if end >= total:
            break
        prompt = f"{COLORS['CYAN']}Showing {start+1}-{end} of {total}. Press [Enter] next, 'p' prev, 'q' quit:{COLORS['RESET']} "
        action = input(prompt).strip().lower()
        if action in {"q", "quit"}:
            break
        if action == "p" and page > 0:
            page -= 1
            continue
        page += 1


def main() -> None:
    try:
        while True:
            clear()
            print_banner()
            print_options()

            choice = prompt_choice("Enter your choice [1-3]:", {"1", "2", "3"})
            if choice == "3":
                print(
                    f"\n{COLORS['MAGENTA']}Goodbye! Thanks for exploring Fibonacci.{COLORS['RESET']}"
                )
                return

            n = prompt_int("Enter a non-negative Fibonacci index (or 'q' to quit):")
            if n < 0:
                print(f"{COLORS['RED']}Index must be non-negative.{COLORS['RESET']}")
                continue

            if choice == "1":
                value = fib(n)
                show_result(n, value)
            else:
                sequence = [fib(i) for i in range(n + 1)]
                show_sequence(n, sequence)

            print()
            action = prompt_choice(
                "Press 1 to compute again, 2 to change mode, 3 to quit:",
                {"1", "2", "3"},
            )
            if action == "3":
                print(f"\n{COLORS['MAGENTA']}Goodbye!{COLORS['RESET']}")
                return
            if action == "2":
                continue
            # if action == '1', loop back with same mode selection
    except KeyboardInterrupt:
        print(f"\n{COLORS['MAGENTA']}Interrupted. Goodbye!{COLORS['RESET']}")


if __name__ == "__main__":
    main()

import os
import subprocess as sub

# Try to use colorama on Windows for reliable colors; fall back to ANSI codes.
try:
    import colorama

    colorama.init()
    from colorama import Fore, Style

    COLORS = {
        "RED": Fore.RED,
        "GREEN": Fore.GREEN,
        "YELLOW": Fore.YELLOW,
        "CYAN": Fore.CYAN,
        "MAGENTA": Fore.MAGENTA,
        "WHITE": Fore.WHITE,
        "RESET": Style.RESET_ALL,
    }
except Exception:
    COLORS = {
        "RED": "\u001b[31m",
        "GREEN": "\u001b[32m",
        "YELLOW": "\u001b[33m",
        "CYAN": "\u001b[36m",
        "MAGENTA": "\u001b[35m",
        "WHITE": "\u001b[37m",
        "RESET": "\u001b[0m",
    }

try:
    import gmpy2
except ImportError:
    gmpy2 = None


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


def boxed_text(lines: list[str], width: int) -> str:
    horizontal = "─" * (width - 2)
    output = [f"┌{horizontal}┐"]
    for line in lines:
        padded = line.ljust(width - 2)
        output.append(f"│{padded}│")
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


def show_result(n: int, value: int) -> None:
    lines = [
        f"Fibonacci number at position {COLORS['YELLOW']}{n}{COLORS['RESET']}",
        "",
        f"{COLORS['GREEN']}{value}{COLORS['RESET']}",
    ]
    width = (
        max(
            len(line.replace(COLORS["RESET"], "").replace(COLORS["YELLOW"], ""))
            for line in lines
        )
        + 6
    )
    box = boxed_text(lines, width)
    print()
    print(box)


def show_sequence(n: int, sequence: list[int]) -> None:
    lines = [f"Full sequence to position {COLORS['YELLOW']}{n}{COLORS['RESET']}", ""]
    lines.extend(
        f"{i:>3}: {COLORS['GREEN']}{value}{COLORS['RESET']}"
        for i, value in enumerate(sequence)
    )
    width = (
        max(
            len(
                line.replace(COLORS["RESET"], "")
                .replace(COLORS["YELLOW"], "")
                .replace(COLORS["GREEN"], "")
            )
            for line in lines
        )
        + 4
    )
    box = boxed_text(lines, width)
    print()
    print(box)


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

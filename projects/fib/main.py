import os
import sys
import subprocess as sub

import argparse


# Try to use colorama on Windows for reliable colors; fall back to ANSI codes.
try:
    import colorama
    colorama.init()
    from colorama import Fore, Style
    COLORS = {
        'RED': Fore.RED,
        'GREEN': Fore.GREEN,
        'YELLOW': Fore.YELLOW,
        'CYAN': Fore.CYAN,
        'RESET': Style.RESET_ALL,
    }
except Exception:
    COLORS = {
        'RED': '\u001b[31m',
        'GREEN': '\u001b[32m',
        'YELLOW': '\u001b[33m',
        'CYAN': '\u001b[36m',
        'RESET': '\u001b[0m',
    }


def clear():
    """Clear the terminal using subprocess (safe, preferred over os.system)."""
    cmd = "cls" if os.name == "nt" else "clear"
    # shell=True is needed for built-in shell commands like 'cls' on Windows.
    sub.run(cmd, shell=True)


def fib(n: int) -> int:
    """Iterative Fibonacci for n >= 0."""
    if n < 0:
        raise ValueError("Input must be a non-negative integer.")
    a, b = 0, 1
    for _ in range(n):
        a, b = b, a + b
    return a


def parse_args():
    parser = argparse.ArgumentParser(description="Colorful Fibonacci utility")
    parser.add_argument('n', type=int, help='Index (non-negative integer) of Fibonacci number')
    parser.add_argument('--sequence', '-s', action='store_true', help='Print the full sequence up to n')
    parser.add_argument('--no-clear', action='store_true', help='Do not clear the screen before printing')
    return parser.parse_args()


def main():
    args = parse_args()

    if args.n < 0:
        print(f"{COLORS['RED']}Error: n must be non-negative{COLORS['RESET']}")
        sys.exit(2)

    if not args.no_clear:
        clear()

    try:
        if args.sequence:
            seq = [fib(i) for i in range(args.n + 1)]
            print(f"{COLORS['CYAN']}Fibonacci sequence up to position {args.n}:{COLORS['RESET']}")
            for i, val in enumerate(seq):
                print(f" {COLORS['YELLOW']}{i:3d}{COLORS['RESET']}: {COLORS['GREEN']}{val}{COLORS['RESET']}")
        else:
            result = fib(args.n)
            print(f"{COLORS['CYAN']}Fibonacci number at position {COLORS['YELLOW']}{args.n}{COLORS['RESET']}")
            print(f"{COLORS['GREEN']}{result}{COLORS['RESET']}")
    except Exception as e:
        print(f"{COLORS['RED']}fib: {e}{COLORS['RESET']}")
        sys.exit(1)


if __name__ == "__main__":
    main()

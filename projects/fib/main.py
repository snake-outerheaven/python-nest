import os
import sys
import subprocess as sub
import time as tm


def clear():
    cmd = "cls" if os.name == "nt" else "clear"
    sub.run(cmd, shell=True)


def fib(n):
    if n < 0:
        raise ValueError("Input must be a non-negative integer.")
    elif n == 0:
        return 0
    elif n == 1:
        return 1
    else:
        a, b = 0, 1
        for _ in range(2, n + 1):
            a, b = b, a + b
        return b


def main():

    try:
        if len(sys.argv) < 2:
            raise ValueError("Please provide a number as an argument.")
        n = int(sys.argv[1])
        result = fib(n)
        print(f"The result of the corresponding fib in position {n} is {result}")

    except Exception as e:
        print(f"fib: {e}")
        tm.sleep(3)
        clear()


if __name__ == "__main__":
    main()

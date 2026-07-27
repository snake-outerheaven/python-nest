import os
import subprocess as sub
import time as tm


def clear():
    cmd = "cls" if os.name == "nt" else "clear"
    sub.run(cmd, shell=True)


def fib(n):
    if n < 0:
        raise ValueError(f"the input must be positive!")
    if n <= 1:
        return n

    return fib(n - 1) + fib(n - 2)


def main():
    while True:
        try:
            n = int(input("Enter a valid integer: "))
            result = fib(n)
            print(f"The result of the corresponding fib to {n} is {result}")

            break

        except Exception as e:
            print(f"fib: {e}")
            tm.sleep(1.5)
            clear()
            continue


if __name__ == "__main__":
    main()

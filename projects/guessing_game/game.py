import random as rd
import sys
import time as tm


def spinner(n, string):
    for i in range(n):
        for c in "/|-\\":
            sys.stdout.write(f"\rLoading {c}")
            sys.stdout.flush()
            tm.sleep(0.2)
    print(f"\r{string}   ")


def getUserName():
    username = str(input("Type your username to play the game: "))
    if username.lower() in {"no", "n"}:
        raise Exception("User said no to entering the name, leaving the game.")
    ans = str(input(f"Do you confirm {username}? (Y/N): "))
    if ans.lower() != "y":
        raise NameError("Wrong answer buddy")
    return username


def getLimits():
    while True:
        try:
            min_val = int(input("Type the lower limit: "))
            max_val = int(input("Type the upper limit: "))
            if min_val > max_val:
                print("Min cannot be greater than max. Try again.")
                continue
            return min_val, max_val
        except ValueError:
            print("Invalid input! Please type numbers only.")


def playRound(secret):
    tries = 0
    while True:
        try:
            guess = int(input("Enter your guess: "))
            tries += 1
            if guess < secret:
                print("The secret number is higher!")
            elif guess > secret:
                print("The secret number is lower!")
            else:
                print(f"You got it in {tries} {'try' if tries == 1 else 'tries'}!")
                return
        except ValueError:
            print("Please enter a valid number.")


def main():
    try:
        user = getUserName()
        print(f"Welcome, {user}!")
        spinner(3, "Starting random number module...")
        min_val, max_val = getLimits()
        secret = rd.randint(min_val, max_val)
        playRound(secret)
    except Exception as e:
        print(f"Exception raised: {e}")


if __name__ == "__main__":
    main()

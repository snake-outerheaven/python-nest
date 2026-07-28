import time as tm
import sys
import subprocess as sub
import random as rd
import os


def spinner(n, string):
    for i in range(n):
        for c in "/|-\\":
            sys.stdout.write(f"\rLoading {c}")
            sys.stdout.flush()
            tm.sleep(0.2)
    print(f"\r{string}   ")


def clear():
    cmd = "cls" if os.name == "nt" else "clear"
    sub.run(cmd, shell=True)


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
                return tries
        except ValueError:
            print("Please enter a valid number.")


def saveGame(user, secret, tries):
    saveString = f"|User: {user}|\t|Secret num: {secret}|\t|{f'{tries} try' if tries == 1 else f'{tries} tries'}|"
    with open("GameLog.txt", "a") as saveFile:
        saveFile.write(saveString)
    os.close(saveFile)
    return saveString


def main():
    try:
        clear()
        user = getUserName()
        print(f"Welcome, {user}!")
        spinner(3, "Starting random number module...")
        min_val, max_val = getLimits()
        secret = rd.randint(min_val, max_val)
        tries = playRound(secret)
        spinner(3, "Saving game")
        saveString = saveGame(user, secret, tries)
        print(f"Game saved! Log -> {saveString}")
    except Exception as e:
        print(f"Exception raised: {e}")


if __name__ == "__main__":
    main()

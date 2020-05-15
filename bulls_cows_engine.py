# "Bulls & Cows" engine.

import random

_holder = []


def make_up_a_number():
    print("Число загадано.")
    global _holder

    _holder = random.sample(range(0, 10), 5)
    if _holder[0] == 0:
        _holder = _holder[1:]
    else:
        _holder = _holder[:4]

    _holder = "".join([str(number) for number in _holder])


def check_the_number(user_guess):
    bull_counter = 0
    cow_counter = 0

    for i, num in enumerate(user_guess):
        if user_guess[i] == _holder[i]:
            bull_counter += 1
        elif num in _holder:
            cow_counter += 1
    return {"bulls": bull_counter, "cows": cow_counter}


def game_over(user_guess):
    if check_the_number(user_guess)["bulls"] == 4:
        return True
    else:
        return False


def either_the_input_correct(user_guess):
    if not user_guess.isdigit():
        return False
    elif len(user_guess) > 4:
        return False
    elif len(set(user_guess)) < 4:
        return False
    elif int(user_guess[0]) == 0:
        return False
    else:
        return True

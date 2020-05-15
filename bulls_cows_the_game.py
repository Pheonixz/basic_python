# A game named "Bulls & Cows".
# https://en.wikipedia.org/wiki/Bulls_and_Cows


import bulls_cows_engine
from termcolor import cprint

bulls_cows_engine.make_up_a_number()
guess_counter = 0
user_guess = None

while True:
    guess_counter += 1
    cprint("Введите 4 цифры числа:", "green")

    while True:
        user_guess = input("> ")
        if not bulls_cows_engine.either_the_input_correct(user_guess):
            cprint(
                f"{user_guess} не подходит! Введите число из 4 цифр. "
                f"Цифры не должны повторяться. Первая цифра не должна быть 0: ", "red"
            )
        else:
            break

    cprint(f"Игрок проверяет число {user_guess}", "blue")
    game_round = bulls_cows_engine.check_the_number(user_guess)

    if bulls_cows_engine.game_over(user_guess):
        cprint(f"Игра окончена. Количество ходов - {guess_counter + 1}. Хотите ещё партию?", "blue")
        choose = input("Да / Нет > ")
        if choose == "Да":
            bulls_cows_engine.make_up_a_number()
            guess_counter = 0
        elif choose == "Нет":
            break
        else:
            cprint('Расцениваем это как "Нет"', "yellow")
            break

    cprint(f"Количество быков - {game_round['bulls']}, количество коров - {game_round['cows']}", "yellow")



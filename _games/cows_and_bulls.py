# cow - good digit in a bad spot
# bull - good digit in good spot
import random


def compare_numbers(number1, number2):
    cows = 0
    bulls = 0

    for i in range(len(usr_input)):
        if usr_input[i] == gen_number[i]:
            cows += 1
        elif usr_input[i] != gen_number[i] and usr_input[i] in gen_number:
            bulls += 1

    return [cows, bulls]


if __name__ == "__main__":
    print("Zgadnij liczbę z przedziału 1000-9999")
    print("wpisz quit aby wyjść")
    is_win = False
    usr_tries = 0
    gen_number = str(random.randint(1000, 9999))

    while True:
        usr_input = input("Podaj liczbę 1000-9999: ")
        if usr_input == "quit":
            break

        try:
            usr_input_number = int(usr_input)
        except ValueError:
            print("niepoprawna wartość")
            continue

        if usr_input_number < 1000 or usr_input_number > 9999:
            print("wartość spoza dopuszczalnego przedziału")

        guess_result = compare_numbers(gen_number, usr_input)

        if guess_result[0] == 4:
            is_win = True
            break
        else:
            print("cows - " + str(guess_result[0]) + " bulls - " + str(guess_result[1]))
            usr_tries += 1

    if is_win:
        print("koniec gry - wygrałeś")
        print("ilość prób: " + str(usr_tries))
        print("wygenerowana liczba - " + gen_number)
    else:
        print("koniec gry - przegrałeś")
        print("ilość prób: " + str(usr_tries))
        print("wygenerowana liczba - " + gen_number)

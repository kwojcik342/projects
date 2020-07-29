game_options = ["rock", "paper", "scissors"]
rock_beats = ["scissors"]
paper_beats = ["rock"]
scissors_beats = ["paper"]

break_phrase = "quit"
choice_p1 = str
choice_p2 = str

print("dostępne wybory: ")
print(game_options)
print("wpisz " + break_phrase + " aby zakończyć grę")
print("")

while True:
    choice_p1 = input("Wybór gracza 1: ")
    if choice_p1 == break_phrase:
        break
    if choice_p1 not in game_options:
        print("niepoprawny ruch")
        continue

    choice_p2 = input("Wybór gracza 2: ")
    if choice_p2 == break_phrase:
        break
    if choice_p2 not in game_options:
        print("niepoprawny ruch")
        continue

    if choice_p1 == choice_p2:
        print("remis!")
    elif choice_p1 == "rock" and choice_p2 in rock_beats:
        print("gracz 1 wygrywa")
    elif choice_p1 == "paper" and choice_p2 in paper_beats:
        print("gracz 1 wygrywa")
    elif choice_p1 == "scissors" and choice_p2 in scissors_beats:
        print("gracz 1 wygrywa")
    else:
        print("gracz 2 wygrywa")

print("koniec gry!")

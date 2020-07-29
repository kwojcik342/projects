# klasa do gry w wisielca


class Hangman:
    def __init__(self, random_word):
        self.random_word = random_word
        self.rand_word_len = len(random_word)
        self.player_guess = ["_"]*self.rand_word_len
        self.tried_letters = []

    def print_player_guess(self):
        # wypisanie aktualnego stanu zgadniętych liter i kresek w miejsce nieodgadniętych
        print(" ".join(self.player_guess))

    def check_letter(self, in_letter):
        # weryfikacja czy podana litera występuje w wylosowanym słowie
        match_counter = 0
        if in_letter in self.tried_letters:
            return 2
        else:
            for letter_idx in range(self.rand_word_len):
                if self.random_word[letter_idx].upper() == in_letter.upper():
                    self.player_guess[letter_idx] = in_letter.upper()
                    match_counter += 1
            self.tried_letters.append(in_letter)
            if match_counter > 0:
                return 1
            else:
                return 0

    def is_win(self):
        # weryfikacja czy gracz odgadł już wszystkie litery
        if "_" in self.player_guess:
            return False
        else:
            return True

    def run_game(self):
        # głowna funkcja do prowadzenia gry
        tries = 6
        player_score = False

        # print(self.random_word)
        print("Odgadnij poniższe słowo.")
        print(" ".join(self.player_guess))
        print("Dostępna ilość prób: " + str(tries))

        while tries > 0:
            letter_result = self.check_letter(input("podaj litere: "))
            if letter_result == 1:
                if self.is_win():
                    player_score = True
                    break
                else:
                    print("Pozostała ilość prób: " + str(tries))
                    self.print_player_guess()
            elif letter_result == 2:
                print("Podałeś już wcześniej taką literę.")
            else:
                tries -= 1
                print("Pozostała ilość prób: " + str(tries))
                self.print_player_guess()

        if player_score:
            print("Wygrałeś!")
            print("Szukane słowo: " + "".join(self.random_word))
        else:
            print("Przegrałeś!")
            print("Szukane słowo: " + "".join(self.random_word))

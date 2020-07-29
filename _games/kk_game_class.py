# klasa do gry kółko i krzyżyk
# 1 = x = krzyżyk
# 2 = o = kółko


class TTT:
    def __init__(self, board_width, board_height):
        self.board_width = board_width
        self.board_height = board_height
        self.board_state = [[0]*board_width for i in range(board_height)]

    def print_current_state(self):
        # techniczna, tylko do weryfikacji działania
        print(self.board_state)

    def draw_board(self):
        # rysowanie aktualnego stanu planszy
        def draw_horizontal(width):
            # rysowanie poziomych kresek
            for i in range(width):
                if i == width - 1:
                    print(" ___ ")
                else:
                    print(" ___", end="")

        def draw_vertical(width, cur_line):
            # rysowanie kresek pionowych i aktualnego stanu pól
            for i in range(width):
                if i == width - 1:
                    if self.board_state[cur_line][i] == 0:
                        print("|   |")
                    elif self.board_state[cur_line][i] == 1:
                        print("| x |")
                    elif self.board_state[cur_line][i] == 2:
                        print("| o |")
                else:
                    if self.board_state[cur_line][i] == 0:
                        print("|   ", end="")
                    elif self.board_state[cur_line][i] == 1:
                        print("| x ", end="")
                    elif self.board_state[cur_line][i] == 2:
                        print("| o ", end="")
        for line in range(self.board_height):
            if line == self.board_height - 1:
                draw_horizontal(self.board_width)
                draw_vertical(self.board_width, line)
                draw_horizontal(self.board_width)
            else:
                draw_horizontal(self.board_width)
                draw_vertical(self.board_width, line)

    def set_player_move(self, player, width, height):
        # wstawienie ruchu gracza do planszy
        if player not in [1, 2]:
            return -2  # błędny gracz
        if width > self.board_width or width < 0:
            return -3  # niepoprawne współżędne
        if height > self.board_height or height < 0:
            return -3  # niepoprawne współżędne
        if player == 1:
            if self.board_state[height][width] == 0:
                self.board_state[height][width] = 1
                return 1
            else:
                return -4
        else:
            if self.board_state[height][width] == 0:
                self.board_state[height][width] = 2
                return 1
            else:
                return -4

    def check_win(self):
        # weryfikacja czy aktualny stan planszy daje komuś zwycięstwo
        p1_score = 0
        p2_score = 0
        for i in range(self.board_width):
            p1_score = 0
            p2_score = 0
            for j in range(self.board_height):
                if self.board_state[j][i] == 0:
                    p1_score = 0
                    p2_score = 0
                elif self.board_state[j][i] == 1:
                    p1_score += 1
                    p2_score = 0
                elif self.board_state[j][i] == 2:
                    p1_score = 0
                    p2_score += 1
                if p1_score == 3:
                    return 1
                elif p2_score == 3:
                    return 2
        for i in range(self.board_height):
            p1_score = 0
            p2_score = 0
            for j in range(self.board_width):
                if self.board_state[i][j] == 0:
                    p1_score = 0
                    p2_score = 0
                elif self.board_state[i][j] == 1:
                    p1_score += 1
                    p2_score = 0
                elif self.board_state[i][j] == 2:
                    p1_score = 0
                    p2_score += 1
                if p1_score == 3:
                    return 1
                elif p2_score == 3:
                    return 2
        for j in range(self.board_height):
            p1_score = 0
            p2_score = 0
            i = j
            k = 0
            while i < self.board_height and k < self.board_height:
                if self.board_state[i][k] == 0:
                    p1_score = 0
                    p2_score = 0
                elif self.board_state[i][k] == 1:
                    p1_score += 1
                    p2_score = 0
                elif self.board_state[i][k] == 2:
                    p1_score = 0
                    p2_score += 1
                if p1_score == 3:
                    return 1
                elif p2_score == 3:
                    return 2
                i += 1
                k += 1
        for j in range(self.board_width):
            p1_score = 0
            p2_score = 0
            i = j
            k = 0
            while i < self.board_height and k < self.board_height:
                if self.board_state[k][i] == 0:
                    p1_score = 0
                    p2_score = 0
                elif self.board_state[k][i] == 1:
                    p1_score += 1
                    p2_score = 0
                elif self.board_state[k][i] == 2:
                    p1_score = 0
                    p2_score += 1
                if p1_score == 3:
                    return 1
                elif p2_score == 3:
                    return 2
                i += 1
                k += 1
        return 0

    def run_game(self):
        # głowna funkcja do prowadzenia gry
        game_winner = 0
        player_turn = False
        p_input = ""

        print("wspolzedne podawaj w formacie: x y")
        print("wpisz quit aby wyjsc")

        while True:
            self.draw_board()
            # self.print_current_state()

            player_turn = True
            while player_turn:
                p_input = input("Gracz 1 - wspolzedne: ")
                if p_input == "quit":
                    break

                coord = p_input.split()
                try:
                    sm_result = self.set_player_move(1, int(coord[0]), int(coord[1]))
                    if sm_result == -4:
                        print("wspolzedne sa juz wykorzystane")
                    if sm_result == -3:
                        print("niepoprawne wspolrzedne")
                    if sm_result == 1:
                        player_turn = False
                except ValueError:
                    print("niepoprawne wspolrzedne")

            if p_input == "quit":
                break
            print(self.check_win())
            if self.check_win() == 1:
                game_winner = 1
                break

            self.draw_board()
            # self.print_current_state()

            player_turn = True
            while player_turn:
                p_input = input("Gracz 2 - wspolzedne: ")
                if p_input == "quit":
                    break

                coord = p_input.split()
                try:
                    sm_result = self.set_player_move(2, int(coord[0]), int(coord[1]))
                    if sm_result == -4:
                        print("wspolzedne sa juz wykorzystane")
                    if sm_result == -3:
                        print("niepoprawne wspolrzedne")
                    if sm_result == 1:
                        player_turn = False
                except ValueError:
                    print("niepoprawne wspolrzedne")

            if p_input == "quit":
                break

            print(self.check_win())
            if self.check_win() == 2:
                game_winner = 2
                break

        if game_winner in [1, 2]:
            self.draw_board()
            print("koniec gry. wygrał gracz: " + str(game_winner))
        else:
            self.draw_board()
            print("koniec gry. brak wygranych")

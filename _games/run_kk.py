from kk_game_class import TTT
import sys

print("kółko i krzyżyk")
try:
    board_size = int(input("Podaj wymiar planszy (np. 3): "))
except ValueError:
    print("Błędna wartość")
    sys.exit(-1)

my_game = TTT(board_size, board_size)
my_game.run_game()

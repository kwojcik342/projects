import random
from hangaman_class import Hangman

# english words allowed in scrabble
f_words = open("sowpods.txt", "r")

words_arr = f_words.readlines()
words_cnt = len(words_arr)
random_word = words_arr[random.randint(0, words_cnt-1)].strip()

f_words.close()

my_hang = Hangman(random_word)
my_hang.run_game()

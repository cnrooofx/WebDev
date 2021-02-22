
import ast
from random import randint


def generate_password():
    read_file = open('wordlist.txt', 'r')
    word_dict = ast.literal_eval(read_file.read())
    words = []
    for i in range(3):
        dice = ''
        for j in range(5):
            rand_num = randint(1, 6)
            dice += str(rand_num)
        words += [word_dict[dice]]
    return '-'.join(words)

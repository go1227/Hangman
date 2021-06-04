__author__ = "Guilherme Ortiz"
__version__ = "1.3"
__date_last_modification__ = "6/4/2021"
__python_version__ = "3"

fail_drawing = [
    [' _ _ _ _ _', '|        |  ', '|        O', '|      - | -', '|       / \\', '|'],
    [' _ _ _ _ _', '|        |  ', '|        O', '|      - | -', '|       /   ', '|'],
    [' _ _ _ _ _', '|        |  ', '|        O', '|      - | -', '|           ', '|'],
    [' _ _ _ _ _', '|        |  ', '|        O', '|      - |  ', '|           ', '|'],
    [' _ _ _ _ _', '|        |  ', '|        O', '|        |  ', '|           ', '|'],
    [' _ _ _ _ _', '|        |  ', '|        O', '|           ', '|           ', '|'],
    [' _ _ _ _ _', '|        |  ', '|         ', '|           ', '|           ', '|'],
    [' _ _ _ _ _', '|           ', '|         ', '|           ', '|           ', '|']]

# Program that will grab a random word text file to use it in the Hangman game

import os
import re
import random

file_path = 'backupwords.txt'
if not (os.path.isfile(file_path) and os.access(file_path, os.R_OK)):
    print("Missing file OR not readable - ABORT")
    exit()

# Part 1: random word should be min 4 letters - max 10 letters.
random_word = ""

letter_qty = -1
valid_entry = False
while valid_entry is False:
    letter_qty = input("How many letters are in your word? [min 4, max 10]:\n")
    if letter_qty.isdigit():
        if 4 <= int(letter_qty) <= 10:
            valid_entry = True
    else:
        print("This is an invalid number!!\n")

backup_word_pool = []
file = open("backupwords.txt", "r")
for line in file:
    line = line.strip('\n').upper()
    if len(line) == int(letter_qty):
        backup_word_pool.append(line)
file.close()

random_word = backup_word_pool[random.randint(1, len(backup_word_pool) - 1)]


# print("This is the word I found for you: '" + random_word + "'")


# Part 2:
# -------------------
#    Hangman game
# -------------------
# No "clear screen" function available. Solution: a series of \n were introduced with the intent of clearing the screen.
# Purely cosmetic and can be easily modified
class hangman:
    def __init__(self, guess_word):
        self.__guess_word = guess_word
        self.__user_choices = set()
        self.__new_letter = ""

    def __repr__(self):
        return "{} ({!r})".format({self.__class__}, {self.__guess_word})

    def get_user_input_letter(self):
        return sorted(self.__user_choices)

    def get_random_word(self):
        return self.__guess_word.upper()

    def add_new_letter(self, new_letter):
        self.__user_choices.add(new_letter)


# Every time the user enters a word, we should show the game progress at that point
def show_game_progress(matches, attempts, game_obj):
    draw_man(attempts)
    partial_result = "| "
    for i in game_obj.get_random_word():
        if i in game_obj.get_user_input_letter():
            partial_result = partial_result + " " + i
        else:
            partial_result = partial_result + " _"
    print(partial_result)
    # print("----------------Matches: " + str(matches))
    # print("----------------attempts: " + str(attempts))
    # print("----------------Current selection of letters: " + str(game.get_user_input_letter()).upper())


# Returns number of matching letters for every user input
def get_matches(val, game_obj):
    tmp = 0
    for i in game_obj.get_random_word():
        if i == val:
            tmp += 1
    return tmp


# Draws on screen the hangman (except for the actual letters already entered by the user)
def draw_man(fail):
    for i in range(len(fail_drawing[fail])):
        print(fail_drawing[fail][i])


fail_limit = 7  # Maximum number of attempts (with 7 strokes we can draw the man hanging = game over)
game = hangman(random_word)
matches = 0
user_choices = ""

while fail_limit > 0:
    # print("HANGMAN DRAWING: " + str(fail_limit))
    show_game_progress(matches, fail_limit, game)

    if matches == len(random_word):
        print("\n\n\n\n\n\n\n\n************ CONGRATULATIONS!! ****************")
        print("\nYou guessed the word '" + random_word + "'. Congratulations!\n\n\n\n")
        exit()
    else:
        if fail_limit < 7:
            user_choices = str(game.get_user_input_letter()).upper()
        if len(user_choices) > 0:  # The following output should only be printed AFTER the user entered at least one letter
            print("\nHere are your current choices so far: " + user_choices)
        letter = input("\n==> Enter a new letter:")
        letter = letter.upper()
        if not re.search('[A-Z]', letter) or len(letter) != 1:  # Only 1 character is accepted and it must be between A and Z
            print("This is not a valid letter. Please try again!")
        else:
            if user_choices.find(letter) == -1:
                game.add_new_letter(letter)
                tmp = get_matches(letter, game)
                matches += tmp
                if tmp == 0:
                    fail_limit -= 1  # No match was found using the user's letter: reduce the number of attempts he/she can have
            else:
                print("\nAttention: You have already tried this letter!")

draw_man(0)
print("\n\n\n--->> I'm sorry, but you failed <<---\n\nThe word was '" + random_word + "'")
exit()

__author__ = "Guilherme Ortiz"
__version__ = "1.0"
__date_last_modification__ = "1/10/2018"
__python_version__ = "3"

#Program that will grab a random word from the internet and will use it for the hangman game
from urllib.request import urlopen
import time
import re


# Part 1: pull a random word from the web, according to the user specification (min 4 letters - max 10 letters).
is_eligible_word = False
random_word = ""

letter_qty = -1
valid_entry = False
while valid_entry is False:
    letter_qty = input("How many letters are in your word? [min 4, max 10]:\n")
    if (letter_qty.isdigit()):
        if (int(letter_qty) >= 4 and int(letter_qty) <= 10):
            valid_entry = True
    else:
        print("This is an invalid number!!\n")

print("\nPlease wait. I'm looking on the web for a word with " + letter_qty + " characters....")

#start an interal basic timer, where the process should automatically abort after more than 30 seconds
#if a matching word can't be found for any reason (timeout or the website didn't random generate a valid word)
time.perf_counter()

current_letter_qty = -1

while is_eligible_word != True:
    link = "http://jimpix.co.uk/generators/word-generator.asp"
    try:
        f = urlopen(link)
        myfile = str(f.read())
    except:
        print("ALERT: There was an error while trying to load the site [" + link + "].\nPlease contact the technical support.")
        exit()

    result = myfile.find("&bull;") #We must find at least one bullet point, because that's where the key words are.
    if (result == -1):
        print("ALERT: There was an error while trying to load the site [" + link + "].\nPlease contact the technical support.")
        exit()
    tmp = str(myfile[result-12:result]).rstrip().lstrip()

    #print("Checking this string... [" + tmp + "]")

    if (tmp.find(">") != -1):
        gt_position = tmp.find(">")
        random_word = tmp[gt_position+1:].upper()
        if len(random_word) == int(letter_qty):
            is_eligible_word = True

    if round(time.perf_counter()) > 30:
        print("\n\nWe tried to find a word with " + letter_qty + " characters but it was taking too long to find one.")
        print("The program has automatically stopped the execution to prevent further technical issues.")
        exit()

#print("This is the word I found for you: '" + random_word + "'")


# Part 2:
#-------------------
#    Hangman game
#-------------------
#Since there is no "clear screen" function for PyCharm, a series of \n were introduced with the intent of clearing the screen.
#This is just cosmetic and can be easily modified
class hangman:
    def __init__(self, guess_word):
        self.__guess_word = guess_word
        self.__user_choices = set()
        self.__new_letter = ""
    def getEnteredUserLetters(self):
        return sorted(self.__user_choices)
    def getRandomWord(self):
        return self.__guess_word.upper()
    def addNewLetter(self, new_letter):
        self.__user_choices.add(new_letter)


#Every time the user enters a word, we should show the game progress at that point.
def show_game_progress(matches, attempts, game_obj):
    partial_result = "\n\n\n\n\n"
    for i in game_obj.getRandomWord():
        if i in game_obj.getEnteredUserLetters():
            partial_result = partial_result + " " + i
        else:
            partial_result = partial_result + " _"
    print(partial_result)
    '''print("----------------Matches: " + str(matches))
    print("----------------attempts: " + str(attempts))
    print("----------------Current selection of letters: " + str(game.getEnteredUserLetters()).upper())'''


#Returns the number of matching letters for every user input
def getMatches(letter, game_obj):
    tmp = 0
    for i in game_obj.getRandomWord():
        if i == letter:
            tmp += 1
    return tmp

fail_limit = 7 #Maximum number of attempts (with 7 strokes we can draw the man hanging = game over)
game = hangman(random_word)
matches = 0
user_choices = ""

while fail_limit > 0:
    #print("HANGMAN DRAWING: " + str(fail_limit))
    show_game_progress(matches, fail_limit, game)

    if (matches == len(random_word)):
        print("\n\n\n\n\n\n\n\n************ CONGRATULATIONS!! ****************")
        print("\nYou guessed the word '" + random_word + "' in " + str(fail_limit+8) + " attempts.\n\n\n\n")
        exit()
    else:
        if fail_limit < 7:
            user_choices = str(game.getEnteredUserLetters()).upper()
        if len(user_choices) > 0: #The following output should only be printed AFTER the user entered at least one letter
            print("\nHere are your current choices so far: " + user_choices)
        letter = input("\n==> Enter a new letter:")
        letter = letter.upper()
        if not re.search('[A-Z]', letter) or len(letter) != 1: #Only 1 character is accepted and it must be between A and Z
            print("This is not a valid letter. Please try again!")
        else:
            if user_choices.find(letter) == -1:
                game.addNewLetter(letter)
                tmp = getMatches(letter, game)
                matches += tmp
                if tmp == 0:
                    fail_limit -= 1  #No match was found using the user's letter: reduce the number of attempts he/she can have
            else:
                print("\nAttention: You have already tried this letter!")

print("\n\n\n--->> I'm sorry, but you failed <<---\n\nThe word was '" + random_word + "'")
exit()
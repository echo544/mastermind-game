"""
############# Project information #############

Project title: Mastermind game
Project goal: Recreate game in Python, to be played in the terminal.

Project start date:         22 Sept 2023
Project "completion" date:    18 Oct 2023
Days spent working on it:   22-24 Sept 2023, 26 Sept 2023, 17-19 Oct 2023, 2 Jan 2024

############# Improvements #############

Considering:
- Clean up this DONE1 DONE2 thing in feedback (check whiteclear function).
- Store number of guesses by player. Make sure any incomplete guesses or guesses typed in with "quit" or "help" are not stored.
- Check if all instances of "result = []" are necessary.
- Change colour library or directly print with terminal colours (test with terminal) so that colours will always show up correctly.
    - Choose one that supports colours from the original game (orange/blue/green/purple/yellow/pink for guessing, red/white for feedback).
- Visual colour selector?

Scrapped:
- Choose number of colours in the code. | Staying true to the original game, which only has 4 colours.
- Add a leaderboard. | Would require an additional text file... I want this to be one file that can be run locally offline.
- Check sum of instances of colours (in array) is 4, or use dictionary? | Not necessary, different logic employed.

Completed:
- Display coloured dots instead of text. | 23 Sept 2023
- Display coloured dots in one line instead of 4. | 18 Oct 2023
- Ignore capitalisation of all inputs. | 2 Jan 2024
- Add option to quit game or ask for instructions (and additional info). | 2 Jan 2024
"""

############# Import libraries #############

import colorama                 # for display of coloured dots
from colorama import Fore, Style
colorama.init(autoreset=True)
import random                   # for shuffling colours
import copy                     # to preserve contents of code array

############# Define functions #############

# To generate a 4-colour code
colours = ["RED", "BLUE", "GREEN", "YELLOW", "MAGENTA", "CYAN"]
code = []                       # define global variable
def generate():
    global code
    for i in range(4):
        code.append(random.choice(colours))
    return code

# To print coloured dots (for code and feedback)
def colourdisplay(array):
    for i in array:
        if i == "RED":
            print(Fore.RED + "●" + Style.RESET_ALL, end=' ')
        elif i == "BLUE":
            print(Fore.BLUE + "●" + Style.RESET_ALL, end=' ')
        elif i == "GREEN":
            print(Fore.GREEN + "●" + Style.RESET_ALL, end=' ')
        elif i == "YELLOW":
            print(Fore.YELLOW + "●" + Style.RESET_ALL, end=' ')
        elif i == "MAGENTA":
            print(Fore.MAGENTA + "●" + Style.RESET_ALL, end=' ')
        elif i == "CYAN":
            print(Fore.CYAN + "●" + Style.RESET_ALL, end=' ')
        elif i == "BLACK":      # feedback colour (correct position)
            print(Fore.BLACK + "●" + Style.RESET_ALL, end=' ')
        elif i == "WHITE":      # feedback colour (wrong position)
            print(Fore.WHITE + "●" + Style.RESET_ALL, end=' ')

# For adding white dots to feedback array (used later)
result = []                     # define global variable
def whiteclear(code_i, guessarray, codearray):
    global result
    stopcounter = 0

    for counter in range(4):
        if stopcounter != 1 and codearray[code_i] == guessarray[counter]:
            result.append("WHITE")
            guessarray[counter] = "DONE"
            stopcounter += 1
            #print(result, guessarray) # for testing

# To provide feedback (b/w dots) on guesses
def feedback(guessarray, codearray):
    global result               # but not "code" array because it's currently empty
    codearraycopy = copy.deepcopy(codearray) # preserve code array contents

    for i in range(4):          # add black dots first
        if codearraycopy[i] == guessarray[i]:
            result.append("BLACK")
            guessarray[i] = "DONE1"
            codearraycopy[i] = "DONE2"
    
    for i in range(4):          # add white dots after replacements
        whiteclear(i, guessarray, codearraycopy)

    random.shuffle(result)
    colourdisplay(result)
    print(" ")
    #print(codearraycopy, guessarray, result) # for testing

    if result != ["BLACK", "BLACK", "BLACK", "BLACK"]:
        result = []             # resets feedback array only if guess is wrong

############# Play the game #############

print("Welcome to mastermind! \nThere are 6 colours for you to choose from: RED, BLUE, GREEN, YELLOW, MAGENTA, and CYAN.")
print("Type HELP for instructions and QUIT at any point to exit the game.")

code = generate()
#code = ["GREEN", "CYAN", "GREEN", "RED"] # for testing
guess = [" "]                   # initialise guess array (length will be checked)

while result != ["BLACK", "BLACK", "BLACK", "BLACK"]:
    while len(guess) != 4 or guess[0] not in colours or guess[1] not in colours or guess[2] not in colours or guess[3] not in colours:
        
        # QUIT and HELP (can be lone inputs, inserted into the middle of a guess, or an "out of range" element)
        if "QUIT" in [g.upper() for g in guess]:
            print("Thanks for playing!")
            exit()
        if "HELP" in [g.upper() for g in guess]:
            print("\nHow to play: \n- You have to guess the 4-colour code (case-insensitive). \n- After each guess, you will receive feedback in the form of black and white dots. \n- A black dot means you have a correct colour in the correct position. \n- A white dot means you have a correct colour in the wrong position. \n- The order of the feedback dots are randomised. \n\nMore info: \n- The game can be run offline if you run it while online at least once (to import the necessary libraries). \n- The colours works best in a Mac Terminal, and needs to be run in a dedicated Python terminal or in a Python environment. \n")
        
        # Change guess into an array (ignoring capitalisation)
        guess = input("Type in four colours, separated by a space: ").upper()
        guess = guess.split(" ")
        #print(guess) # for testing
    colourdisplay(guess)

    print(" ")
    print("Thinking...")
    result = []                 # clear feedback array
    feedback(guess, code)

    if result == ["BLACK", "BLACK", "BLACK", "BLACK"]:
        print("Well done, you guessed the code!")
        print(code)
        break

    guess = [" "]               # clear guess array
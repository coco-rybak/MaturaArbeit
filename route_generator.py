import random

# to do :
# turn the functions into while statements so that it keeps asking for valid input
# figure out how the points can work as integers
# integrate a random generator in accordance with what was chosen to later convert to a .JSON file

#first test to see how the random import works
def random_hold():
    holds= ["crimp", "jug", "sloper", "pinch", "pocket"]
    print(random.choice(holds))

#makes user choose a difficulty
def difficulty_choice():
    difficulties = ["3", "4", "5", "6a", "7a", "8a", "6b", "7b", "8b", "6c", "7c", "8c"]
    print("What grade for the route do you want?")
    difficulty = input()
    if difficulty not in difficulties:
        print("Please choose a valid difficulty")

    else:
        print(f" {difficulty}")

#makes user choose a hold type
def hold_choice():
    holds = ["crimp", "jug", "sloper", "pinch", "pocket"]
    print("Is there a specific type of hold you want? If you don't care which, please type \"does not matter\"")
    hold_choice = input()
    if hold_choice in holds:
        print ("You have chosen the hold type" f"{hold_choice}" ". Excellent choice.")
    elif hold_choice == "does not matter":
        hold_choice = random.choice(holds)
        print ("Since you were too weak to make a decision, the computer has decided the hold type " f"{hold_choice} " "for you, an excellent choice.")
    else:
        print ("Nothing was chosen, not even randomness. Try again.")

'''
#french scale to interval translation (amount of points for the generator)
def converter_grade():
    "3" = 30
    "4" = 40
    "5" = 50
    "6a" = 60
    "6b" = 63
    "6c" = 67
    "7a" = 70
    "7b" = 73
    "7c" = 77
    "8a" = 80
    "8b" = 83
    "8c" = 87
'''

if __name__ == '__main__':
    difficulty_choice()
    hold_choice()
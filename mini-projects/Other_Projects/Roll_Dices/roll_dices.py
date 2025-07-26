import random

#! Roll the Dice

# ? Strategy
# loop until user press n
# Ask you for input
# If input is y
# generate two number
# print those number
# if input is n
# print thank you message
# terminate the program
# Else
# print Invalid Choice
# continue

while True:
    choice = input("Roll the Dice? (y/n) ")
    if choice == "y" or choice == "Y":
        die1 = random.randint(1, 6)
        die2 = random.randint(1, 6)
        final_result = die1, die2
        print(final_result)
    elif choice == "n" or choice == "N":
        print("Thanks for Playing ..")
        break
    else:
        print("Invalid Choice!")

# no_of_dice = int(input("How many dices you want to roll"))

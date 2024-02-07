# pseudo code:
# prompt user to enter name
# ... age
# ... house number
# ... street name
# print out a sentence containing all the inputted user data above

# collect user input
user_name = input("What is your name? ")
user_age = input("What is your age? ")
user_house_number = input("What is your house number? ")
user_street_name = input("What is your street name? ")

# print formatted string containing all user inputs
print(f"You are {user_name}. You are {user_age} years old. You live at house number {user_house_number} on {user_street_name}.")

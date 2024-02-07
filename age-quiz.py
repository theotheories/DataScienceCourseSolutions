# ● The program you create in
# this ﬁle will be used to output a variety of responses determined by the
# data the user enters.
# ● Tips:
# o You should use the if-elif-else statement structure to create the
# program.
# o Note that the order in which you set up the conditions is
# important; you will need to work out what makes sense in terms
# of the logical tests applied to the ages.

# ● Write code to take in a user’s age and store it in an integer variable called
# age.
# ask user for age, cast to int
age = int(input("What is your age in years? "))

# ordering clauses in a way that makes sense, counting down in age:
# ● Assume that the oldest someone can be is 100; if the user enters a
# higher number, output the message "Sorry, you're dead.".
if age > 100:
    print("Sorry, you're dead.")

# ● If the user is 65 or older, output the message "Enjoy your retirement!"
elif age >= 65:
    print("Enjoy your retirement!")

# ● If the user is 40 or over, output the message "You're over the hill."
elif age >= 40:
    print("You're over the hill.")

# ● If the user is 21, output the message "Congrats on your 21st!"
elif age == 21:
    print("Congrats on your 21st!")

# ● If the user is under 13, output the message "You qualify for the kiddie
# discount."
elif age < 13:
    print("You qualify for the kiddie discount.")

# ● For any other age, output the message "Age is but a number."
else:
    print("Age is but a number.")

# Original:
# print "Welcome to the error program"
#     print "\n"
# SYNTAX ERRORS:
# SyntaxError: Missing parentheses in call to 'print'.
print("Welcome to the error program")
# IndentationError: unexpected indent. & SyntaxError: Missing parentheses
print("\n")

# Original:
# # Variables declaring the user's age, casting the str to an int, and printing the result
# age_Str == "24 years old"
# age = int(age_Str)
# print("I'm" + age + "years old.")


# # Errors above:
# Indentation level incorrect (SYNTAX ERROR)
# "years old" is repeated in age_Str and in the print() argument
# SYNTAX ERROR: == equality operator used instead of = assignment operator
# RUNTIME ERROR: int() can only be used with characters that represent numbers, so remove " years old"
# RUNTIME ERROR: age is an int now so shouldn't be concatenated in the print function.

# Logical errors:
# Variables declaring the user's age, casting the str to an int, and printing the result
# Fixed:
age_Str = "24"
age = int(age_Str)
print("I'm " + age_Str + " years old.")

# Original:
# years_from_now = "3"
# total_years = age + years_from_now
# print "The total number of years:" + "answer_years"

# Errors in the above:
# LOGICAL ERROR: If years_from_now is stored as string, it can't be added to age which is int
# SYNTAX ERROR: indentation error
# SYNTAX ERROR: print is missing parentheses
# SYNTAX ERROR: answer_years should be passed as a variable reference, not as a literal string.
# SYNTAX ERROR: answer_years was not defined yet. use total_years instead.
# there should be a space after colon like ""... years: "
# SYNTAX ERROR: total_years should be cast to a string before attempting concatenation with + operator

# Variables declaring additional years and printing the total years of age
# LOGICAL ERRORS:
years_from_now = 3
total_years = age + years_from_now

print("The total number of years: " + str(total_years))

# Original:
# Variable to calculate the total amount of months from the total amount of years and printing the result
# total_months = total * 12
# print "In 3 years and 6 months, I'll be " + total_months + " months old"

# Errors above:
# SYNTAX ERROR: total wasn't defined. it's meant to be total_years.
# LOGICAL ERROR: they forgot to add the six months, so update the line total_months =... line
# SYNTAX ERROR: missed parentheses for print().
# SYNTAX ERROR: cast to string before attempting concatenation with the + operator


# LOGICAL ERROR - calculation incorrect if months is not included:
total_months = total_years * 12 + 6
print("In 3 years and 6 months, I'll be " + str(total_months) + " months old")

# HINT, 330 months is the correct answer

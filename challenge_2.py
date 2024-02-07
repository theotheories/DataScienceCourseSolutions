# Write Python code to take the name of a user's favourite restaurant and
# store it in a variable called string_fav.

string_fav = input("Enter your favourite restaurant: ")

# ● Below this, write a statement to take in the user's favourite number. Use
# casting to store it in an integer variable called int_fav.

int_fav = int(input("Enter your favourite whole number: "))

# ● Print out both of these using two separate print statements below what
# you have written. Be careful!

print(f"Fave restaurant: {string_fav}")
print(f"Fave number: {str(int_fav)}")

# ● Once this is working, try to cast string_fav to an integer. What happens?
# Add a comment in your code to explain why this is.

string_fav_as_int = int(string_fav)

# ValueError: invalid literal for int() with base 10: "Morley's"

# The characters in the restaurant string do not make sense as numbers.
# You can't have a length of "apple" centimetres, for example.

# It is hinting about higher-base systems using characters to represent numbers
# because e.g. hexadecimal uses a b c d e f characters to represent what we call in decimal as numbers 10 to
# 15 in a single digit, allowing you to count to 15 before having to "carry the one" ie increment the next column
# and start counting the unit column from zero again.

# Ask the user to enter a sentence using the input() method. Save the user’s response in a variable called str_manip.

str_manip = input("Enter a sentence: ")

#  Using this string value, write the code to do the following:
# ○ Calculate and display the length of str_manip.

print(f"Length of your sentence: {len(str_manip)} characters.")
# ○ Find the last letter in str_manip sentence. Replace every occurrence
# of this letter in str_manip with ‘@’.
# ■ e.g. if str_manip= “This is a bunch of words”, the output would
# be: “Thi@ i@ a bunch of word@”

print(f"Last letter in your sentence: {str_manip[-1]}")
print(
    f"Replacing that character with @: {str_manip.replace(str_manip[-1], '@')}")

# ○ Print the last 3 characters in str_manipbackwards.
# ■ e.g. if str_manip= “This is a bunch of words”, the output would
# be: “sdr”.

print(
    f"The last three characters in your sentence backwards: {str_manip[-1:-4:-1]}")

# ○ Create a ﬁve-letter word that is made up of the ﬁrst three characters
# and the last two characters in str_manip.
# ■ e.g. if str_manip = “This is a bunch of words”, the output
# would be: “Thids”.

print(
    f"The first three letters in your sentence then the last two letters, making a five-letter word: {str_manip[:3]}{str_manip[-2:]}")

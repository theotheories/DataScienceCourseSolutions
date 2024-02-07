# Desired pattern:
# *
# **
# ***
# ****
# *****
# ****
# ***
# **
# *

# Ask user how wide to make the star pattern.
# Then store the widest part simply as a star character repeated n times.
width = int(
    input("How many units wide do you want your arrow star pattern to be?\n"))
widest_part_of_pattern = "*" * width

# For loop to repeat code to make the pattern
# Double the total width because we count up to the width then back down to zero.
for i in range(width*2):
    slice_end = i
    if i > width:
        # Start decreasing the count once we are past the midway point
        slice_end = width - i
    # All the cleverness resides in the string slice method
    print(widest_part_of_pattern[:slice_end])

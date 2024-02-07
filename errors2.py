# This example program is meant to demonstrate errors.
# There are some errors in this program. Run the program, look at the error messages, and find and fix the errors.

# Original:
# animal = Lion
# animal_type = "cub"
# number_of_teeth = 16


# SYNTAX ERROR: Lion is not defined. It should be a string.
animal = "Lion"
animal_type = "cub"
number_of_teeth = 16


# Original:
# full_spec = "This is a {animal}. It is a {number_of_teeth} and it has {animal_type} teeth"

# SYNTAX/LOGICAL ERROR: The variables were not being formatted into the string. We need to use an f-string.
# LOGICAL ERROR: number_of_teeth and animal_type were in the wrong order
full_spec = (
    f"This is a {animal}. It is a {animal_type} and it has {number_of_teeth} teeth"
)

# Original:
# print full_spec

# SYNTAX ERROR: Missing parentheses in call to 'print'. Did you mean print(...)?
print(full_spec)

# Here is my function to calculate average of a supplied list of integers (or floats)
def calculate_average(num_list):
    sum = 0
    # Compilation (Syntax) error 1: Missing colon at the end of the for loop statement:
    for num in num_list
        sum += num
    # Logical error: No runtime or syntax errors, but you don't need to add one to the length. Avg = sum/(num of nums)
    average = sum / (len(num_list)+1)
    return average

# Runtime error: "3" is a string/character, not an integer; won't be able to add or divide it:
numbers = [1, 2, "3", 4, 5]

# Compilation (Syntax) error 2: The function name is misspelled:
average = calculate_averag(numbers)

print(f"The average is: {average}")

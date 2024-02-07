# Pseudocode:
# Continually ask user to enter a number
# Add the number entered to the total
# Repeat, unless user has entered -1
# If -1 then exit loop and don't add -1 to the total
# Calculate the average of numbers entered, excluding the -1

# Set variables
user_selected_num = 0.0
count_of_numbers_supplied = 0
running_total_of_user_selected_nums = 0.0

# Output width display constant
output_character_width = 80

# Print welcome messages
print("=" * output_character_width)
print("Welcome to the average calculator.")
print("I will calculate the averages of numbers you give to me.")
print("Enter '-1' when you have finished entering numbers to average.")
print("=" * output_character_width)

# While loop to repeatedly ask user for another number
# Add to running total and increment counter
while user_selected_num != -1.0:
    user_selected_num = float(
        input("Enter the next number to add to the grand total, or '-1' when finished.\n"))
    if user_selected_num == -1.0:
        # Don't increment count or add to running total if -1 entered
        continue
    count_of_numbers_supplied += 1
    running_total_of_user_selected_nums += user_selected_num

# Print outputs, formatted
print("=" * output_character_width)
print(f"{count_of_numbers_supplied} numbers supplied.".center(
    output_character_width, " "))
print(f"{running_total_of_user_selected_nums:.4f} is the grand total.".center(
    output_character_width, " "))
print(f"Avg: {running_total_of_user_selected_nums/count_of_numbers_supplied:.4f}.".center(output_character_width, " "))
print("=" * output_character_width)

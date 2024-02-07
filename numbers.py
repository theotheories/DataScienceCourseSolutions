# Ask the user to enter three different integers.

int1 = int(input("Enter a whole number: "))
int2 = int(input("Enter a second whole number: "))
int3 = int(input("Enter a third number: "))

# ● Then print out:
# ○ The sum of all the numbers

print(f"Sum: {int1 + int2 + int3}")

# ○ The ﬁrst number minus the second number

print(f"First minus second number: {int1 - int2}")

# ○ The third number multiplied by the ﬁrst number

print(f"Third number multiplied by first number: {int3 * int1}")

# ○ The sum of all three numbers divided by the third number

print(
    f"The sum of all three numbers divided by the third number: {(int1 + int2 + int3) / int3}")

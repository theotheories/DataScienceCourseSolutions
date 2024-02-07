# Here is my function that calculates the factorial of a number.
# I wrote in a logical error, so every time it will return 0 instead of the correct answer.
# The range of the loop starts from 0 instead of 1.
# This is a logical error because the factorial of a number is defined as the product of all positive integers up to that number.
# Multiplication by 0  instead results in 0.
# The correct range should start from 1, not 0.
# Moreover, factorial multiplications include the number itself.
# range(end) will stop at end-1, so we need to account for this in the code.


def factorial(n):
    fact = 1
    # Logical error here. 0 should be excluded from the factorial, but range() starts at 0 by default.
    # Logical error part 2: range(n) stops at n-1.
    for i in range(n):
        fact *= i
    return fact


print(factorial(5))

# This is how it should be coded instead:


def fixed_factorial(n):
    fact = 1
    # Add a start argument to range(start, end) instead of only range(end) above:
    # start=1, end=n+1 - this will give the correct integers.
    for i in range(1, n + 1):
        fact *= i
    return fact


print(fixed_factorial(5))

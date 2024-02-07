# import math to get the sqrt() function

import math

# ● Ask the user to enter the lengths of all three sides of a triangle.

print("Let me help you find the area of a triangle, by giving me its three side lengths.")
side1 = float(input("Side length 1: "))
side2 = float(input("Side length 2: "))
side3 = float(input("Side length 3: "))

# ● Calculate the area of the triangle.
# ● Print out the area.
# ● Hints:
# ○ If side1, side2 and side3 are the sides of the triangle:
# ■ s = (side1 + side2 + side3)/2 and
# ■ area = √(s(s-a)*(s-b)*(s-c))
# ○ You’ll need to be able to calculate the square root

s = (side1 + side2 + side3)/2
area = math.sqrt(s * (s-side1) * (s-side2) * (s-side3))

print(f"Your triangle has area = {area}")

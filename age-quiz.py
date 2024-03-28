while True:
    try:
        # Get user's age
        age = int(input("What is your age in years? (Enter '0' to exit) "))

        # Exit condition
        if age == 0:
            break

        # Check age and print appropriate message
        if age > 100:
            print("Sorry, you're dead.")
        elif age >= 65:
            print("Enjoy your retirement!")
        elif age >= 40:
            print("You're over the hill.")
        elif age == 21:
            print("Congrats on your 21st!")
        elif age < 13:
            print("You qualify for the kiddie discount.")
        else:
            print("Age is but a number.")
    except ValueError:
        # Handle non-integer input
        print("Please enter a valid integer for age.")

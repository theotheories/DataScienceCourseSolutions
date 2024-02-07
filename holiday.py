# Function to calculate hotel cost
def hotel_cost(num_nights):
    cost_per_night = 100  
    return num_nights * cost_per_night  # Total hotel cost

# Function to calculate plane cost
def plane_cost(city_flight):
    # Cost varies based on the city
    flight_costs = {"astrolabe": 200, "a": 200, "bangaroo": 300, "b": 300, "carnidingle": 400, "c": 400}
    return flight_costs.get(city_flight, 500)  # Default cost is 500

# Function to calculate car rental cost
def car_rental(rental_days):
    cost_per_day = 50  
    return rental_days * cost_per_day  # Total car rental cost

# Function to calculate total holiday cost
def holiday_cost(city_flight, num_nights, rental_days):
    # Total cost is the sum of hotel, plane, and car rental costs
    return hotel_cost(num_nights) + plane_cost(city_flight) + car_rental(rental_days)


# ASCII doodle
print("="*80 + "\n" +
"""
         S   E   V    E   N             P    E    N    G    U    I   N    S 
      __        __        __        __         __        __        __       
    _|__|_    _|__|_    _|__|_    _|__|_     _|__|_    _|__|_    _|__|_   
     ( o>      ( o>      ( o>      ( o>       ( o>      ( o>      ( o>     
     
   T  R   A   V   E   L             A   G   E   N   T  S               (c)2023
     
================================================================================
~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~  Holiday Expense Calculator Tool    ~ ~ ~ ~ ~~ ~ ~ ~ ~
================================================================================
""")

# Get user input
print("Flight options: Astrolabe (£200), Bangaroo (£300), Carnidingle (£400)")
print("All other destinations: £500")
city_flight = input("Enter the city you will be flying to: ").lower()
num_nights = int(input("Enter the number of nights you will be staying at a hotel: "))
rental_days = int(input("Enter the number of days for which you will be hiring a car: "))

# Calculate total cost
total_cost = holiday_cost(city_flight, num_nights, rental_days)

# Print the result in a stylish way
print("\n")
print("="*80)
print("HOLIDAY COST SUMMARY".center(80))
print("="*80)
print(f"Destination: ".ljust(30) + city_flight.upper().ljust(19) + "|"+ f"Flight Cost: £{plane_cost(city_flight):,.2f}".rjust(30))
print(f"Hotel stay: ".ljust(30) + f"{num_nights:,} nights".ljust(19) + "|" + f"Cost: £{hotel_cost(num_nights):,.2f}".rjust(30))
print(f"Car rental: ".ljust(30) + f"{rental_days:,} days".ljust(19) + "|" + f"Cost: £{car_rental(rental_days):,.2f}".rjust(30))
print("-"*80)
print(f"Total cost of your holiday:".ljust(50) + f"£{total_cost:,.2f}".rjust(30))
print("="*80)
print("Remember, the best things in life are free. The second best are very expensive.".center(80))
print("So, enjoy your holiday, from all of us here at Seven Penguins!".center(80))
print("="*80)
# Create a list called menu
menu = ["Coffee", "Tea", "Sandwich", "Cake"]

# Create a dictionary called stock
stock = {
    "Coffee": 50,
    "Tea": 100,
    "Sandwich": 20,
    "Cake": 10
}

# Create another dictionary called price
price = {
    "Coffee": 2.0,
    "Tea": 1.5,
    "Sandwich": 5.0,
    "Cake": 3.5
}

# Calculate the total stock worth in the cafe
total_stock_worth = 0
for item in menu:
    item_value = stock[item] * price[item]
    total_stock_worth += item_value

# Print out the result of the calculation, formatted to 2dp
print(f"The total stock worth in the cafe is: £{total_stock_worth:.2f}")

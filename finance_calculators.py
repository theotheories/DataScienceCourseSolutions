import math

# User guidance message strings set here
welcome_title = "Finnegan Finance"
welcome_subtitle = "Making Interest Interesting"
investment_calc_title = "Investment Interest Calculator"
bond_calc_title = "Bond Home Loan Calculator"
program_explanation_text = f"We offer two calculators: {investment_calc_title}, and {bond_calc_title}."
investment_calc_explanation_1 = "Calculate the amount of interest"
investment_calc_explanation_2 = "you'll earn on your investment"
investment_calc_choice = "Type 'Investment' to select"
bond_calc_explanation_1 = "Calculate the amount you'll"
bond_calc_explanation_2 = "have to pay on a home loan"
bond_calc_choice = "Type 'Bond' to select"
output_title = "Your results"
deposit_output_title = "Deposit amount:"
annual_interest_rate_output_title = "Annual interest rate:"
monthly_interest_rate_output_title = "Monthly interest rate:"
num_years_invested_title = "Number of years invested:"
num_months_repaying_title = "Number of months repaying:"
present_value_title = "Present house value:"
simple_or_compound_title = "Simple or compound interest:"
interest_accrued_title = "Interest accrued:"
total_amount_after_interest_title = "Grand total including interest:"
monthly_repayment_title = "Monthly repayment:"

# Variables related to output width and visual layout set here
character_width_of_output = 100
subsection_width = int((character_width_of_output - 2) / 2)
horizontal_section_dividing_line_character = "="
horizontal_subsection_dividing_line_character = "-"
vertical_subsection_divider = "||"
vertical_whitespace_padder = "\n"
horizontal_whitespace_padder = " "
horizontal_shading_padder = "#"
horizontal_accounting_bottom_line_padder = "_"
horizontal_visual_divider_line = horizontal_section_dividing_line_character * \
    character_width_of_output
subsection_horizontal_divider_line = horizontal_subsection_dividing_line_character * subsection_width

# Define function to handle investment interest calculator


def investment_interest_calculator(deposit_amount, interest_rate_percentage, num_years_invested, simple_or_compound):
    if simple_or_compound == "S":
        return deposit_amount * (1 + interest_rate_percentage * num_years_invested)
    else:
        return deposit_amount * math.pow((1 + interest_rate_percentage), num_years_invested)

# Define function to handle bond home loan calculator


def bond_home_loan_calculator(present_house_value, monthly_interest_rate_percentage, num_months_repaying_bond):
    return (monthly_interest_rate_percentage * present_house_value)/(1 - (1 + monthly_interest_rate_percentage)**(-num_months_repaying_bond))


# Print onboarding title messages to console, formatted for user experience with shading, centering, and dividers
print(horizontal_visual_divider_line)
print(f"{welcome_title.center(len(welcome_subtitle) + 4, ' ').upper():{horizontal_shading_padder}^{character_width_of_output}}")
print(f"{welcome_subtitle.center(len(welcome_subtitle) + 4, ' ').lower():{horizontal_shading_padder}^{character_width_of_output}}")
print(horizontal_visual_divider_line + vertical_whitespace_padder)

# Print program explanation text, centered with whitespace around
print(program_explanation_text.center(character_width_of_output,
      horizontal_whitespace_padder) + vertical_whitespace_padder)

# Print Investment Interest Calculator and Bond Home Loan Calculator explanatory text boxes
print(subsection_horizontal_divider_line,
      subsection_horizontal_divider_line, sep=vertical_subsection_divider)
print(vertical_subsection_divider.center(
    character_width_of_output, horizontal_whitespace_padder))

# Textbox titles, centred within subsections, and subsections vertically divided
print(investment_calc_title.upper().center(subsection_width, horizontal_whitespace_padder),
      bond_calc_title.upper().center(subsection_width, horizontal_whitespace_padder), sep=vertical_subsection_divider)
print(vertical_subsection_divider.center(
    character_width_of_output, horizontal_whitespace_padder))

# Textbox explanation text, centred in each subsection
print(investment_calc_explanation_1.center(subsection_width, horizontal_whitespace_padder),
      bond_calc_explanation_1.center(subsection_width, horizontal_whitespace_padder), sep=vertical_subsection_divider)
print(investment_calc_explanation_2.center(subsection_width, horizontal_whitespace_padder),
      bond_calc_explanation_2.center(subsection_width, horizontal_whitespace_padder), sep=vertical_subsection_divider)
print(vertical_subsection_divider.center(
    character_width_of_output, horizontal_whitespace_padder))

# Inform user how to select investment or bond and close subsections area
print(investment_calc_choice.center(subsection_width, horizontal_whitespace_padder), bond_calc_choice.center(
    subsection_width, horizontal_whitespace_padder), sep=vertical_subsection_divider)
print(vertical_subsection_divider.center(
    character_width_of_output, horizontal_whitespace_padder))
print(subsection_horizontal_divider_line,
      subsection_horizontal_divider_line + vertical_whitespace_padder, sep=vertical_subsection_divider)

# Collect user choice of desired calculator. Make case insensitive with str.lower() function
# Check that user's input is valid before proceeding
user_calc_selection_valid = False
while user_calc_selection_valid is not True:
    user_calc_selection_string = input(
        "Choose your desired calculator (type 'Investment' or 'Bond'):\n").lower()

    if user_calc_selection_string in ["investment", "bond", "i", "b"]:
        user_calc_selection_valid = True
    else:
        print("Not a valid input. Check spelling and type again.")

# User has selected the investment interest calculator
if user_calc_selection_string in ["investment", "i"]:
    # Print title that confirms user's choice of calculator
    print(vertical_whitespace_padder + horizontal_visual_divider_line)
    print(f"{investment_calc_title.center(len(investment_calc_title) + 4, ' ').upper():{horizontal_shading_padder}^{character_width_of_output}}")
    print(horizontal_visual_divider_line + vertical_whitespace_padder)

    # Gather required values from user
    deposit_amount = float(input("How much did you initially deposit?\n"))
    interest_float = float(input(
        "What is your annual interest rate? e.g., if you had 4% interest, then you'd enter '4'.\n"))
    interest_percentage = interest_float / 100
    simple_or_compound = input(
        "Simple or compound interest? Enter either 'S' or 'C'.\n").upper()
    num_years_deposited = int(
        input("How many years will you keep your money invested?\n"))

    # Pass values to the investment interest calculator function, round to 2dp, add £/% symbol
    raw_total_after_interest = investment_interest_calculator(
        deposit_amount, interest_percentage, num_years_deposited, simple_or_compound)
    total_amount_after_interest_string_with_currency_symbol = f"£{raw_total_after_interest:.2f}"
    interest_only_2dp_formatted_with_currency_symbol = f"£{(raw_total_after_interest - deposit_amount):.2f}"
    deposit_amount_2dp_formatted_with_currency_symbol = f"£{deposit_amount:.2f}"
    annual_interest_with_percentage_symbol = f"{interest_float}%"

    # Display formatted inputs
    print(vertical_whitespace_padder + horizontal_visual_divider_line)
    print(f"{output_title.center(len(output_title) + 4, ' ').upper():{horizontal_shading_padder}^{character_width_of_output}}")
    print(horizontal_visual_divider_line + vertical_whitespace_padder)
    print(f"{deposit_output_title:{horizontal_accounting_bottom_line_padder}<{character_width_of_output - len(deposit_amount_2dp_formatted_with_currency_symbol)}}{deposit_amount_2dp_formatted_with_currency_symbol}")
    print(f"{annual_interest_rate_output_title:{horizontal_accounting_bottom_line_padder}<{character_width_of_output - len(annual_interest_with_percentage_symbol)}}{annual_interest_with_percentage_symbol}")
    print(f"{simple_or_compound_title:{horizontal_accounting_bottom_line_padder}<{character_width_of_output - len(simple_or_compound)}}{simple_or_compound}")
    print(f"{num_years_invested_title:{horizontal_accounting_bottom_line_padder}<{character_width_of_output - len(str(num_years_deposited))}}{num_years_deposited}")

    # Display formatted final outputs
    print(vertical_whitespace_padder + horizontal_visual_divider_line)
    print(f"{interest_accrued_title.upper()} {interest_only_2dp_formatted_with_currency_symbol}".center(
        character_width_of_output, horizontal_whitespace_padder))
    print(f"{total_amount_after_interest_title.upper()} {total_amount_after_interest_string_with_currency_symbol}".center(
        character_width_of_output, horizontal_whitespace_padder))
    print(horizontal_visual_divider_line)

# User has selected the bond home loan calculator
else:
    # Print title that confirms user's choice of calculator
    print(horizontal_visual_divider_line)
    print(f"{bond_calc_title.center(len(bond_calc_title) + 4, ' ').upper():{horizontal_shading_padder}^{character_width_of_output}}")
    print(horizontal_visual_divider_line + vertical_whitespace_padder)

    # Gather required values from user
    current_house_value = int(
        input("How much is the house currently worth?\n"))
    annual_interest_float = float(input(
        "What is your annual interest rate? e.g., if you had 4% interest, then you'd enter '4'.\n"))
    monthly_interest_percentage = (annual_interest_float / 100) / 12
    monthly_interest_display_percentage = annual_interest_float / 12
    num_months_repaying = int(
        input("How many months will you pay the bond over?\n"))

    # Pass values to the bond home loan calculator function, round to 2dp, convert to string, add £/% symbol
    repayment_value = bond_home_loan_calculator(
        current_house_value, monthly_interest_percentage, num_months_repaying)
    repayment_value_rounded_with_currency_symbol = f"£{repayment_value:.2f}"
    current_house_value_with_currency_symbol = f"£{current_house_value}"
    monthly_interest_display_percentage_rounded_with_percentage_symbol = f"{monthly_interest_display_percentage:.2f}%"
    annual_interest_with_percentage_symbol = f"{annual_interest_float}%"

    # Display formatted inputs
    print(vertical_whitespace_padder + horizontal_visual_divider_line)
    print(f"{output_title.center(len(output_title) + 4, ' ').upper():{horizontal_shading_padder}^{character_width_of_output}}")
    print(horizontal_visual_divider_line + vertical_whitespace_padder)
    print(f"{present_value_title:{horizontal_accounting_bottom_line_padder}<{character_width_of_output - len(current_house_value_with_currency_symbol)}}{current_house_value_with_currency_symbol}")
    print(f"{annual_interest_rate_output_title:{horizontal_accounting_bottom_line_padder}<{character_width_of_output - len(annual_interest_with_percentage_symbol)}}{annual_interest_with_percentage_symbol}")
    print(f"{monthly_interest_rate_output_title:{horizontal_accounting_bottom_line_padder}<{character_width_of_output - len(monthly_interest_display_percentage_rounded_with_percentage_symbol)}}{monthly_interest_display_percentage_rounded_with_percentage_symbol}")
    print(f"{num_months_repaying_title:{horizontal_accounting_bottom_line_padder}<{character_width_of_output - len(str(num_months_repaying))}}{num_months_repaying}")

    # Display formatted final output
    print(vertical_whitespace_padder + horizontal_visual_divider_line)
    print(f"{monthly_repayment_title.upper()} {repayment_value_rounded_with_currency_symbol}".center(
        character_width_of_output, horizontal_whitespace_padder))
    print(horizontal_visual_divider_line)

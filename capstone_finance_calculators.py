from datetime import datetime
import math
import os
import time
import webbrowser

# Rich python library imports for visual design
from rich.align import Align
from rich.console import Console
from rich.columns import Columns
from rich.panel import Panel
from rich.progress import (
    BarColumn,
    Progress,
    SpinnerColumn,
    TaskProgressColumn,
    TextColumn,
    TimeRemainingColumn,
    TimeElapsedColumn,
)
from rich.prompt import Confirm, FloatPrompt, IntPrompt, Prompt
from rich.rule import Rule
from rich.table import Column, Table
from rich.terminal_theme import MONOKAI
from rich.text import Text


# ----DEFINE FUNCTIONS including DOCSTRINGS ----
def gather_user_input_values(calculator_type: str) -> dict:
    """
    Gather user input values for different calculator types (mortgage or investment interest) via
    interactive prompts. All user inputs are validated to be above zero and of the correct type.

    Parameters:
        - calculator_type (str): The type of calculator for which inputs are being gathered.
        "m" for mortgage payment, "i" for investment interest.

    Returns:
        - dict: A dictionary containing the gathered inputs relevant to the selected calculator
        type. Keys are strings with descriptive names, and values are either floats or ints.
    """
    # Validation checking variable to check values above zero
    valid_input = False

    if calculator_type == "m":

        # FloatPrompt.ask() and IntPrompt.ask() will check user has inputted a string which can be cast to the correct datatype
        while not valid_input:
            console.print(
                "[b]All of your answers must be 0 or above, and months should be less than 12"
            )
            present_dwelling_value = FloatPrompt.ask(
                "What is the current value of the dwelling?"
            )
            monthly_interest = FloatPrompt.ask(
                "What is your monthly interest rate? Type 0 if you only know your annual rate"
            )
            annual_interest = FloatPrompt.ask(
                "What is the annual interest rate? Type 0 if you gave your monthly rate"
            )
            years_repaying = IntPrompt.ask(
                "How many full years on the mortgage? You can specify additional months in the next question"
            )
            months_repaying = IntPrompt.ask(
                "How many months on top of the full years above will you be paying off the mortgage?"
            )

            # Validate inputs or try again
            if (
                all(
                    x >= 0
                    for x in (
                        present_dwelling_value,
                        monthly_interest,
                        annual_interest,
                        years_repaying,
                        months_repaying,
                    )
                )
                and months_repaying < 12
            ):
                valid_input = True

                # Account for users that didn't give either annual or monthly, with maths from other interest
                if monthly_interest == 0 and annual_interest != 0:
                    monthly_interest = annual_interest / 12

                elif annual_interest == 0 and monthly_interest != 0:
                    annual_interest = monthly_interest * 12

                elif monthly_interest != 0 and annual_interest != 0:
                    console.print(
                        "You have given both a monthly interest rate and an annual interest rate."
                    )
                    console.print(
                        "The monthly interest rate will overwrite the annual interest rate."
                    )

                    annual_interest = monthly_interest * 12
                    console.print(
                        f"Monthly rate: {monthly_interest:.1f}%, Annual rate: {annual_interest:.1f}%"
                    )
                    time.sleep(1)

        return {
            "Dwelling Value (£)": present_dwelling_value,
            "Annual Interest (%)": annual_interest,
            "Monthly Interest (%)": monthly_interest,
            "Repayment Duration (years)": years_repaying,
            "Repayment Duration (additional months)": months_repaying,
        }

    elif calculator_type == "i":

        # FloatPrompt.ask() and IntPrompt.ask() will check user has inputted a string which can be cast to the correct datatype
        while not valid_input:
            console.print("[b]All of your answers must be 0 or above")
            deposit = FloatPrompt.ask(
                "What amount is currently deposited in your investment?"
            )
            annual_interest = FloatPrompt.ask(
                "What is the annual interest rate on your investment?"
            )
            years = IntPrompt.ask("How many years will you keep your money invested?")

            # Validate inputs or try again
            if all(x >= 0 for x in (deposit, annual_interest, years)):
                valid_input = True

        return {
            "Deposit (£)": deposit,
            "Annual Interest (%)": annual_interest,
            "Investment Duration (years)": years,
        }

    # Guard case, unreachable code due to user being prompted to choose only m or i inclusive
    else:
        console.print("Unrecognised calculator chosen. Starting again...")
        time.sleep(4)
        main()


def interest_calculator(
    deposit: float, annual_interest: float, years: int, compound_simple: str
) -> dict:
    """
    Calculate the interest and the total after simple or compound interest accrues on a principal deposit.

    Parameters:
        - deposit (float): The principal amount deposited. Must be a non-negative value.
        - annual_interest (float): The annual interest rate as a percentage (e.g., 4 for 4%). Must
        be a non-negative value.
        - years (int): The number of years of interest accrual. Must be a non-negative value.
        - compound_simple (str): User choice of simple or compound interest, "s" or "c".

    Returns:
        - dict: The first value is the accrued interest on the principal deposit, and
        the second value is the total amount including the initial deposit and accrued interest.
        The keys are strings with descriptive names.

    Example:
        >>> interest_calculator(1000, 5, 5, "s")
        {
            "Accrued Interest (£)": 250.0,
            "Total incl. Deposit and Interest (£)": 1250.0
        }
    """
    if compound_simple == "s":
        annual_interest_percentage = annual_interest / 100
        interest = deposit * annual_interest_percentage * years
        total = deposit + interest

    elif compound_simple == "c":
        annual_interest_percentage = annual_interest / 100
        total = deposit * math.pow((1 + annual_interest_percentage), years)
        interest = total - deposit

    return {
        "Accrued Interest (£)": interest,
        "Total incl. Deposit and Interest (£)": total,
    }


def mortgage_payment(
    present_dwelling_value: float,
    annual_interest: float = 0,
    monthly_interest: float = 0,
    years_repaying: int = 0,
    months_repaying: int = 0,
) -> dict:
    """
    Calculate the total and monthly repayments for a mortgage payment.

    Parameters:
        - present_dwelling_value (float): The current value of the property. Must be a non-negative
        value.
        - annual_interest (float): The annual interest rate, expressed as a percentage. Used if
        no monthly interest rate is provided. Must be a non-negative value.
        - monthly_interest (float): The monthly interest rate, expressed as a percentage. Takes
        precedence over the annual interest rate if provided. Must be a non-negative value.
        - years_repaying (int): The number of full years over which the loan will be repaid. Must
        be a non-negative value.
        - months_repaying (int): The additional months over which the loan will be repaid, on top
        of the full years. Must be a non-negative value.

    Returns:
        - dict: The first value is the monthly repayment amount, and the second value is the total
        repayment amount over the entire loan period. The keys are strings with descriptive names.

    Example:
        >>> mortgage_payment(1000, 5, 0, 5, 0)
        {
            "Monthly Repayment (£)": 21.27,
            "Total Repayment (£)": 1276.28
        }
    """
    # Tally up the repayment months by adding years and months
    total_repayment_months = years_repaying * 12 + months_repaying

    # Convert annual percentage to monthly percentage if no monthly percentage provided
    if monthly_interest == 0:
        monthly_interest = annual_interest / 12

    # Convert to percentage
    monthly_interest = monthly_interest / 100

    # Calculation with mortgage repayment formula
    denominator = 1 - math.pow((1 + monthly_interest), -total_repayment_months)
    # Catch where total repayment months is 0 because this will give 1-1 =
    try:
        monthly_repayment = (monthly_interest * present_dwelling_value) / denominator
    except ZeroDivisionError:
        monthly_repayment = 0

    total_repayment = monthly_repayment * total_repayment_months

    return {
        "Monthly Repayment (£)": monthly_repayment,
        "Total Repayment (£)": total_repayment,
    }


def simulate_work(progress: Progress) -> None:
    """
    Simulate work by updating a progress bar over time to enhance user experience during calculations.

    Parameters:
        - progress (Progress): An object representing the progress bar to be updated.

    Returns:
        - No return value. The function is responsible for displaying a progress bar.
    """
    task = progress.add_task("[cyan]Calculations", total=100)

    for _ in range(100):
        time.sleep(0.05)  # Simulate work by sleeping then updating
        progress.update(task, advance=1)


def print_calculation_summary_table(
    calc_choice: str, inputs: dict, final_results: dict, exporting_console: Console
) -> None:
    """
    Create and display a table summarising the user's calculation choices, inputs, and the final results.

    This function dynamically generates a table based on the type of calculation chosen by the user,
    populating it with the provided inputs and the calculation's final results. The final results include
    both the interest and total for simple/compound interest calculations or the monthly and total repayments
    for mortgage calculations. The table is then displayed in the console, centred and formatted for readability.

    Parameters:
        - calc_choice (str): Identifier for the calculation type chosen by the user. Accepts "si" for
        simple interest, "ci" for compound interest, and "m" for mortgage payment,
        which influences the table's title.
        - inputs_dict (dict): A dictionary of the user's inputs where keys are descriptive labels and
        values are the corresponding inputs provided by the user.
        - final_results (dict): Dict with results of the calculation to be displayed in the table,
        including both a primary and secondary result, such as interest and total amount in the case of interest,
        or monthly and total repayments in the case of mortgage repayment cal.
        - exporting_console (Console): Temporary Console instance to fill with just table results,
        to ensure correct export to svg/html/text.

    Returns:
        - No return value. This function outputs directly to the terminal.
    """
    table_title_map = {
        "si": "Simple Interest Results",
        "ci": "Compound Interest Results",
        "m": "Mortgage Payment Results",
    }
    title = table_title_map.get(calc_choice, "Results")

    table = Table(
        title=title,
        caption="Thank you for using our services",
        expand=True,
        show_edge=True,
        show_header=False,
        show_lines=True,
        leading=1,
    )

    for descriptive_label, value in inputs.items():
        # Account for best formatting of inputs based on their meaning
        if "£" in descriptive_label:
            table.add_row(f"{descriptive_label}", f"{value:,.2f}")
        elif "%" in descriptive_label:
            table.add_row(f"{descriptive_label}", f"{value:,.1f}")
        else:
            table.add_row(f"{descriptive_label}", f"{value:,}")

    # Underline the important calculated values from final_results dict
    for descriptive_label, value in final_results.items():
        table.add_row(f"[u]{descriptive_label}", f"[u]{value:,.2f}")

    table.columns[0].style = "cyan"
    table.columns[1].style = "bold magenta"
    table.columns[1].justify = "right"

    exporting_console.print(Align.center(table))


def clear_console_and_print_header(local_console: Console = None) -> None:
    """
    Clears the console and prints the header bar which is defined outside the function scope,
    unless a specific console instance is passed (such as when exporting a receipt).
    A new line is printed to space the header out from the other rendered console contents.

    Parameters:
        - local_console (Console): Optional param, representing the Console instance to be cleared.
        The console instance could represent where the table of results is printed, to be
        exported as a receipt. The header should be printed on the receipt. If no console instance
        is passed, this defaults to the global console instance defined in the global scope.

    Returns:
        - No return value. This is responsible for updating the console display at the start of a
        new section, or at the point of receipt export.
    """
    if local_console is None:
        local_console = console  # Use global console

    local_console.clear()
    local_console.print(header)
    local_console.print()  # Spacing line


def export_receipt(export_format: str, export_console: Console) -> None:
    """
    Exports the table of user inputs plus the calculation result to a file, and opens the exported file.

    The function supports exporting to image (SVG), webpage (HTML), or text format.
    After exporting, the file is automatically opened in the default application.

    Parameters:
        - export_format (str): The format for exporting the receipt. Choices are "image",
        "webpage", "text".
        - exporting_console (Console): Temporary Console to fill with just table results,
        to ensure correct export to image (SVG)/webpage (HTML)/text.

    Returns:
        - No return value. This function will open the exported receipt in a new window.
    """
    filename_map = {
        "image": "receipt.svg",
        "webpage": "receipt.html",
        "text": "receipt.txt",
    }
    filename = filename_map.get(export_format, "receipt.svg")

    # Use the absolute path of the current working directory
    absolute_file_path = os.path.join(os.getcwd(), filename)

    if export_format == "image":
        export_console.save_svg(
            absolute_file_path, title="Finnegan Finance Calculators", theme=MONOKAI
        )
    elif export_format == "webpage":
        export_console.save_html(absolute_file_path, theme=MONOKAI)
    elif export_format == "text":
        export_console.save_text(absolute_file_path)
    else:
        console.print("Unsupported format. Defaulting to image export.")
        export_console.save_svg(
            absolute_file_path, title="Finnegan Finance Calculators", theme=MONOKAI
        )

    console.print()  # Spacing line
    console.print(
        f'[b]Exported your [u]{export_format}[/] receipt to [link={absolute_file_path}]"{absolute_file_path}".',
        "[b]It should open now, else you can find it in your file explorer.",
        sep="\n",
        justify="center",
    )
    console.print()  # Spacing line

    # Open the exported file
    webbrowser.open(absolute_file_path)


# ----VISUAL INTERFACE CREATION SECTION----
# Instantiate a Rich Python library Console object, record=True allows export of receipts at the end
console = Console(record=True)


# ----HEADER BAR SECTION----
# Make a grid to contain titles and the time
grid = Table.grid(expand=True)
grid.add_column(justify="left", ratio=1)
grid.add_column(justify="center", ratio=2)
grid.add_column(justify="right", ratio=1)

# Fill in the content of the grid, use rich's inline BBCode-style markdown syntax to stylise the text
# Use datetime's formatting options for a readable date
grid.add_row(
    "[i]Finnegan Finance",
    "[b]Investment Interest and Mortgage Calculators",
    datetime.now().strftime("%a %b %d, %Y, %I:%M%p"),
)
# Create panel for header with titles and clock
header = Panel(grid, style="red on white")


# ----WELCOME and CALCULATOR CHOICE SECTION----
# Display a centred welcome message
welcome = Panel(
    Text(
        "We offer two calculators: Investment Interest Calculator, and Mortgage Payment Calculator",
        style="blue",
        justify="center",
        overflow="fold",
    ),
    title="[i][green]Welcome",
    title_align="left",
    subtitle="[b][red]Make your choice below",
    subtitle_align="right",
)


# ----DESCRIBE THE CALCULATORS SECTION----
explain_calcs = Columns(
    [
        Panel(
            Text.from_markup(
                """
Calculate the amount of interest you'll earn in the future on your investment.

• You can choose [u]simple[/] or [u]compound[/] interest.\n• You'll need:"""
                """ [i]deposit amount, annual %interest rate, years invested
                """
            ),
            style="cyan on deep_sky_blue4",
            padding=(2, 3),
            title="[b]Interest",
            subtitle="[b]Type 'i' to select",
            width=int((console.width - 4) / 2),
            height=16,
        ),
        Panel(
            Text.from_markup(
                """
Calculate the monthly amount you'll have to repay for a mortgage.

• You'll need: [i]present value of dwelling, annual %interest rate,"""
                """ years and months over which your mortgage loan will be repaid
                """
            ),
            style="yellow on dark_green",
            padding=(2, 3),
            title="[b]Mortgage",
            subtitle="[b]Type 'm' to select",
            width=int((console.width - 4) / 2),
            height=16,
        ),
    ],
    equal=True,
    padding=3,
    align="center",
)


# ----EXPLAIN DIFFERENCE BETWEEN SIMPLE OR COMPOUND INTEREST----
explain_interests = Columns(
    [
        Panel(
            """Simple interest is calculated on your initial loan value, and the interest remains"""
            """ at the constant rate based on that principal sum""",
            style="hot_pink3 on chartreuse1",
            padding=(2, 3),
            title="[b]Simple Interest",
            subtitle="[b]Type 's' to select",
            width=int((console.width - 4) / 2),
        ),
        Panel(
            """Compound interest means that the interest rate at each billing period applies to"""
            """ the principal plus interest accumulated""",
            style="dark_violet on light_salmon1",
            padding=(2, 3),
            title="[b]Compound Interest",
            subtitle="[b]Type 'c' to select",
            width=int((console.width - 4) / 2),
        ),
    ],
    equal=True,
    padding=3,
    align="center",
)


# ----DEFINING A PROGRESS BAR TO SIMULATE WORK BEING DONE----
progress = Progress(
    SpinnerColumn(
        spinner_name="runner",
        finished_text="[green]:heavy_check_mark:",
        table_column=Column(None),
    ),
    SpinnerColumn(
        spinner_name="monkey",
        finished_text="[green]:heavy_check_mark:",
        table_column=Column(None),
    ),
    SpinnerColumn(
        spinner_name="earth",
        finished_text="[green]:heavy_check_mark:",
        table_column=Column(None),
    ),
    TextColumn("{task.description}", table_column=Column(ratio=2)),
    BarColumn(bar_width=None, table_column=Column(ratio=5)),
    TaskProgressColumn(table_column=Column(ratio=1)),
    TimeRemainingColumn(table_column=Column(ratio=1)),
    TimeElapsedColumn(table_column=Column(ratio=1)),
    console=console,
    expand=True,
)


# ----PRINTING ALL TO CONSOLE - main()----
def main() -> None:
    # Welcome messages in spread-out graphics
    clear_console_and_print_header()

    console.print(welcome)
    console.print()  # Spacing line
    console.print(explain_calcs)
    console.print()  # Spacing line

    # First branch of user choice (investment or mortgage)
    calc_choice = Prompt.ask("[green]How can we help?", choices=["i", "m"])

    # Investment interest calculator selected
    if calc_choice == "i":
        clear_console_and_print_header()
        console.print(Rule("[red][b]Interest Calculator", style="blue"))
        console.print()  # Spacing line
        console.print(explain_interests)
        console.print()  # Spacing line

        # Second branch of user choice will depend on this answer (simple or compound interest)
        interest_type = Prompt.ask(
            "[green]Which type of interest are we helping you calculate?",
            choices=["s", "c"],
        )

        clear_console_and_print_header()
        if interest_type == "s":
            console.print(Rule("[red][b]Simple Interest Calculator", style="blue"))
            console.print()  # Spacing line

        elif interest_type == "c":
            console.print(Rule("[red][b]Compound Interest Calculator", style="blue"))
            console.print()  # Spacing line

        # Gather user inputs about the balance they want to calculate interest on
        calc_components = gather_user_input_values(calc_choice)

        # calc_components is a dictionary, so convert its values to a list to use the *args syntax
        calc_results = interest_calculator(
            *list(calc_components.values()), compound_simple=interest_type
        )

        # "ci" or "si": This concatenated calc_choice will inform the title of the output table
        calc_choice = interest_type + calc_choice

    # Mortgage calculator selected
    elif calc_choice == "m":
        clear_console_and_print_header()
        console.print(Rule("[red][b]Mortgage Payment Calculator", style="blue"))
        console.print()  # Spacing line

        # Gather user inputs about the mortgage they want to calculate payments on
        calc_components = gather_user_input_values(calc_choice)

        # calc_components is a dictionary, so convert its values to a list to use the *args syntax
        calc_results = mortgage_payment(*list(calc_components.values()))

    # Ask if user would like a receipt, and in which format they desire
    console.print()  # Spacing line
    save = Confirm.ask("After viewing your results, would you like to save a receipt?")
    if save:
        export_format = Prompt.ask(
            "Choose a format for your receipt",
            choices=["image", "webpage", "text"],
            default="image",
        )

    # Progress bar simulates work being done
    with progress:
        console.print()  # Spacing line
        console.print(Rule())
        simulate_work(progress)
        time.sleep(
            1
        )  # Give users a little time to see that all is completed before displaying table

    # Create a temp console to only export the table and header
    clear_console_and_print_header()
    temp_console = Console(record=True)
    clear_console_and_print_header(temp_console)

    # Print table of results
    print_calculation_summary_table(
        calc_choice, calc_components, calc_results, temp_console
    )

    # Export table, if user has requested this
    if save:
        export_receipt(export_format, temp_console)


# This file is meant to be run as a script so this is just cover against import (imagining that the functions could be imported, or display panels etc could be made into a class that could be exported for future use):
if __name__ == "__main__":
    main()

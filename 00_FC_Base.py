# Used to create a dataframe
import pandas

# Used for profit calculations
import math


# Checks that user input is an integer or float. As well as checking if it is more than or equal to 0.
def num_check(question, error, num_type):
    while True:
        try:
            response = num_type(input(question))
            if response <= 0:
                print(error)
            return response
        except ValueError:
            print(error)


# Function to validate yes/no input
def yes_no(question):
    to_check = ["yes", "no"]
    while True:
        response = input(question).lower()
        for var_item in to_check:
            if response == var_item:
                return response
            elif response == var_item[0]:
                return var_item
        print("Please enter either yes or no... ..\n")


# Checks that string input is not blank
def not_blank(question, error):
    while True:
        response = input(question)
        if response == "":
            print(f"{error}. \nPlease try again. \n")
            continue
        return response


# Function to format a number as currency
def currency(x):
    return f"${x:.2f}"


# Function to get expenses (variable or fixed)
def get_expenses(var_fixed):
    item_list = []
    quantity_list = []
    price_list = []
    variable_dict = {
        "Item": item_list,
        "Quantity": quantity_list,
        "Price": price_list
    }
    item_name = ""
    while item_name.lower() != "xxx":
        print()
        # Get item name
        item_name = not_blank("Item name:", "The component name can't be blank.")
        if item_name.lower() == "xxx":
            break

        if var_fixed == "variable":
            # Get quantity for variable expenses
            quantity = num_check("Quantity:", "The amount must be a whole number more than zero", int)
        else:
            quantity = 1
        # Get price for the item
        price = num_check("How much for a single item? $", "The price must be a number <more than 0>", float)
        # Add item, quantity, and price to lists
        item_list.append(item_name)
        quantity_list.append(quantity)
        price_list.append(price)

    # Create a DataFrame from the lists
    expense_frame = pandas.DataFrame(variable_dict)
    expense_frame = expense_frame.set_index('Item')

    # Calculate cost of each component
    expense_frame['Cost'] = expense_frame['Quantity'] * expense_frame['Price']

    # Calculate the subtotal
    sub_total = expense_frame['Cost'].sum()

    # Format price and cost columns as currency
    expense_frame[['Price', 'Cost']] = expense_frame[['Price', 'Cost']].applymap(currency)

    return [expense_frame, sub_total]


# Function to print expenses
def expense_print(heading, frame, subtotal):
    print("**** {} Costs ****".format(heading))
    print(frame)
    print()
    print(" {} Costs: ${:.2f}".format(heading, subtotal))
    return ""


def profit_goal(total_costs):
    error = "Please enter a valid profit goal\n"
    while True:
        response = input("What is your profit goal (eg 500 or 50%): ")
        if response[0] == "$":
            profit_type = "$"
            amount = response[1:]

        elif response[-1] == "%":
            profit_type = "%"
            amount = response[:-1]

        else:
            profit_type = "unknown"
            amount = response

        try:
            amount = float(amount)
            if amount <= 0:
                print(error)
                continue

        except ValueError:
            print(error)
            continue

        if profit_type == "unknown" and amount >= 100:
            dollar_type = yes_no(f'Do you mean ${amount:.2f}. ie {amount:.2f} dollars? ')

            if dollar_type == "yes":
                profit_type = "$"

            else:
                profit_type = "%"

        elif profit_type == "unknown" and amount < 100:
            percent_type = yes_no(f"Do you mean {amount}%?, y / n ")
            if percent_type == "yes":
                profit_type = "%"
            else:
                profit_type = "$"
        if profit_type == "$":
            return amount
        else:
            goal = (amount / 100) * total_costs
            return goal


def round_up(amount, round_to):
    return int(math.ceil(amount / round_to)) * round_to


# Main Routine goes here

# Prompt the user to enter the product name
product_name = not_blank("Product name: ", "The product name can't be blank.")
how_many = num_check("How many items will you be producing? ", "The number of items must be whole number more than 0",
                     int)

print()
print("Please enter the variable costs below")

# Get variable expenses
variable_expenses = get_expenses("variable")
variable_frame = variable_expenses[0]
variable_sub = variable_expenses[1]

# Get fixed expenses if available
print()
have_fixed = yes_no("Do you have fixed costs (y / n)? ")
# Check if the user has fixed costs and obtain the expenses if available
if have_fixed == "yes":
    fixed_expenses = get_expenses("fixed")
    fixed_frame = fixed_expenses[0]
    fixed_sub = fixed_expenses[1]
    fixed_txt = pandas.DataFrame.to_string(fixed_frame)
    fixed_total = f" Fixed costs: ${fixed_sub}"
    fixed_heading = "***** Fixed costs *****"
else:
    fixed_sub = 0
    fixed_total = ""
    fixed_txt = ""
    fixed_heading = "**** There are no fixed costs ****"

all_costs = variable_sub + fixed_sub
profit_target = profit_goal(all_costs)
sales_needed = all_costs + profit_target

round_to = num_check("Round to nearest...? $", "Can't be 0", int)
selling_price = sales_needed / how_many
print("Selling Price (unrounded): ${:.2f}".format(selling_price))
recommended_price = round_up(selling_price, round_to)

heading = f" ***** Fundraising - {product_name} *****"

variable_txt = pandas.DataFrame.to_string(variable_frame)


variable_total = f" Variable costs: ${variable_sub:.2f}"

all_costs_txt = f" **** Total costs : ${all_costs:.2f} ****"

variable_heading = "***** Variable costs *****"


profit_info = f"""**** Profit & Sales Target ****
Profit Target: ${profit_target:.2f}
Total sales needed: ${(all_costs + profit_target):.2f} """

pricing_info = f""" **** Pricing *****
Minimum Price: ${selling_price:.2f}
Recommended Price: ${recommended_price:.2f}"""

to_write = [heading, variable_heading, variable_txt, variable_total, fixed_heading, fixed_txt, fixed_total,
            all_costs_txt,
            profit_info, pricing_info
            ]

for item in to_write:
    print(item)
    print()

file_name = "{}.txt".format(product_name)
text_file = open(file_name, "w+")
# heading
for item in to_write:
    text_file.write(item)
    text_file.write("\n\n")
# close file
text_file.close()

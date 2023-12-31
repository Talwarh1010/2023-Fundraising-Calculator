import pandas

def not_blank (question, error):
      while True:
            response =  input(question)
            if response == "":
                print(f"{error}. \nPlease try again. \n")
                continue
            return response

def num_check(question, error, num_type):
    while True:
        try:
            response = num_type(input(question))
            if response <= 0:
                print(error)
            return response
        except ValueError:
            print(error) 
            

#currency formatting function
def currency(x):
    return "${:.2f}".format(x)

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
        # get name, quantity and item
        item_name = not_blank("Item name:",
                                        "The component name can't be  \
                                        blank.")
        if item_name.lower() == "xxx":
                break
        quantity = num_check("Quantity:",
                                        "The amount must be a whole number \
                                        more than zero",
                                        int)
        price = num_check("How much for a single item? $",
                            "The price must be a number <more "
                            "than 0>",float)
                # add item, quantity and price to lists
        item_list.append(item_name)
        quantity_list.append(quantity)
        price_list.append(price)
    expense_frame = pandas.DataFrame(variable_dict)
    expense_frame = expense_frame.set_index('Item')
    # Calculate cost of each component
    expense_frame['Cost'] = expense_frame['Quantity'] \
                                    *expense_frame['Price']
    sub_total = expense_frame['Cost'].sum()
    add_dollars = ['Price', 'Cost']
    for item in add_dollars:
        expense_frame[item] = expense_frame[item].apply(currency)
        
    return [expense_frame, sub_total]
        
    # Find sub total
    
# Get user data
product_name = not_blank("Product name: ",
                                    "The product name can't be blank. ")
#loop to get component, quantity and price

variable_expenses = get_expenses("variable")
variable_frame= variable_expenses[0]
variable_sub = variable_expenses[1]

print()
print(variable_frame)
print()
# Currency Formatting (uses currency function)

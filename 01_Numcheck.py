from urllib import response


def num_check(question, error, num_type):
    while True:
        try:
            response = num_type(input(question))
            if response <= 0:
                print(error)
            return response
        except ValueError:
            print(error)
            
get_int = num_check ("How many do you need?",
                          "Please enter an amount more than 0\n",
                          int)
get_cost = num_check ("How much does it cost? $",
                            "Please enter a number more than 0\n",
                            float)
print(f"You need {get_int}")
print(f"You need {get_cost}")
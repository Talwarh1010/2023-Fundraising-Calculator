def num_check(question, error, num_type):
    while True:
        try:
            response = num_type(input(question))
            if response <= 0:
                print(error)
            return response
        except ValueError:
            print(error)
            
def yes_no(question):
      to_check = ["yes", "no"]
      while True:
            response = input(question).lower()
            for var_item in to_check:
                  if response == var_item:
                      return response
                  elif response == var_item[0]:
                      return var_item
            print ("Please enter either yes or no... ..\n")
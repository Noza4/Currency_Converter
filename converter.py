from Calculate import calculate
from Error import Invalid, CurrencyError
from DB import search_user, save_user, ls, id_ls, save_transaction

valid = False
p_number = ''
while valid is False:
    try:
        p_number = str(input("Enter Your Personal ID: "))
        if len(p_number) != 11:
            raise Invalid
        for i in p_number:
            if i not in id_ls:
                raise Invalid
        valid = True
    except Invalid:
        print("Personal ID Is Invalid ")


if p_number and search_user(p_number) is False:
    name = str(input("Enter Your Name: "))
    lastname = str(input("Enter Your Lastname: "))
    save_user(name, lastname, p_number)


valid = False
w_curr = ''
while valid is False:
    try:
        w_curr = str(input("Enter the first 3 letters of the currency you want: ")).upper()
        if w_curr not in ls:
            raise CurrencyError
        else:
            valid = True
    except CurrencyError:
        print("This Kind Of Currency Is Not Available")


quantity = int(input("How much you want to convert: "))
get = 0
if quantity >= 1000:
    age = int(input("How Old Are You: "))
    if age <= 18:
        print("You Aren't Old Enough !")
    else:
        get = calculate(quantity, w_curr)
        print(get)

else:
    get = calculate(quantity, w_curr)
    print(get)

save_transaction(p_number, w_curr, quantity, get)

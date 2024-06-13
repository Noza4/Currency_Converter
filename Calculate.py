from API import fetch_data


def calculate(quantity, curr):
    rate = fetch_data(curr)
    result = quantity * rate
    return result

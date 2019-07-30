"""
LH Ventures Python Coding Challenge

This app allows a user to filter on a CSV for products within a specified price range or expiration date range,
with the ability to filter using wildcards.
"""

import csv
from datetime import datetime
from prettytable import PrettyTable

CSV_FILE_NAME = 'products.csv'
USAGE_STRING = (
    "To search for products, enter these four filters in order: PRICE_MIN PRICE_MAX EXPIRES_START EXPIRES_STOP, "
    "with a * to indicate a skipped value. Expiry dates are of the format JUL-01-2019."
)


def _clean_filter_values(filter_string):
    """Clean the filter string of the format PRICE_MIN PRICE_MAX EXPIRES_START EXPIRES_STOP"""
    price_min, price_max, exp_start, exp_stop = filter_string.split()

    if price_min != '*':
        price_min = float(price_min)
    if price_max != '*':
        price_max = float(price_max)
    if exp_start != '*':
        exp_start = datetime.strptime(exp_start, "%b-%d-%Y")  # Example format is JAN-01-2019
    if exp_stop != '*':
        exp_stop = datetime.strptime(exp_stop, "%b-%d-%Y")

    return price_min, price_max, exp_start, exp_stop


def display_table(filter_string='* * * *'):
    """
    Display product table with optional filter values

    User input is formatted as PRICE_MIN PRICE_MAX EXPIRES_START EXPIRES_STOP
        * PRICE_MIN - minimum price (* indicates no minimum)
        * PRICE_MAX - maximum price (* indicates no maximum)
        * EXPIRES_START - earliest expiration date (* indicates no earliest date)
        * EXPIRES_STOP - latest expiration date (* indicates no latest date)
    """

    try:
        price_min, price_max, exp_start, exp_stop = _clean_filter_values(filter_string)
    except Exception:
        print(USAGE_STRING)
        return

    with open(CSV_FILE_NAME, newline='') as csv_file:
        reader = csv.reader(csv_file)
        table = PrettyTable()
        table.field_names = next(reader)  # Provided CSV headers are of the format 'id,name,price,expires'

        for row in reader:
            price = float(row[2])
            exp_date = datetime.strptime(row[3], "%m/%d/%Y")  # Example format is 01/01/2019

            if (
                (price_min == '*' or price_min <= price) and
                (price_max == '*' or price_max >= price) and
                (exp_start == '*' or exp_start <= exp_date) and
                (exp_stop == '*' or exp_stop >= exp_date)
            ):
                table.add_row(row)

        print(table)
        table.clear_rows()


def start():
    """
    Start accepting user input to filter on an existing CSV
    Quit program when user types 'exit'
    """

    print(USAGE_STRING)
    while True:
        filter_string = input('> ')
        if filter_string == 'exit':
            break
        display_table(filter_string)


if __name__ == '__main__':
    start()

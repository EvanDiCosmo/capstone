import urllib.request
import urllib.error
import urllib.parse
import csv
import io
import headings
from typing import List, Optional, Any

# This function accesses the api_request URL and converts
# the contents to a usable Python object and returns it
def call_api ( api_request , heads):
    '''Make http request'''
    response = urllib.request.urlopen(api_request)
    response = response.read()
    csv_text = response.decode()
    csv_array = extract_data(csv_text)

    select_data(csv_array, heads)

def _maybe_number(s: str) -> Any:
    s = s.strip()
    if s == "":
        return s
    # try int then float, otherwise return original string
    try:
        return int(s)
    except ValueError:
        try:
            return float(s)
        except ValueError:
            return s

# function to extract data from a csv with the headers specified in array
# Headers correspond to line (num in headers.txt) - 1
def extract_data(
text: str,
delimiter: str = ",",
skip_initial_space: bool = True,
convert_numbers: bool = False
) -> List[List[Any]]:
    """
    Parse CSV text into a list of rows, where each row is a list of column values.

    - `text` : the CSV content (may be multiple lines)
    - `delimiter` : field delimiter (default ',')
    - `skip_initial_space` : ignore spaces immediately after delimiter
    - `convert_numbers` : try to convert numeric-looking fields to int/float

    Returns: list of rows (list of lists). Zero-indexed: first row is result[0].
    """
    # handle optional BOM at start
    if text.startswith("\ufeff"):
        text = text.lstrip("\ufeff")

    f = io.StringIO(text)
    reader = csv.reader(f, delimiter=delimiter, skipinitialspace=skip_initial_space)
    rows = []
    for row in reader:
        if convert_numbers:
            row = [_maybe_number(cell) for cell in row]
        else:
            # keep raw strings but strip newline artifacts (csv already strips newlines)
            row = [cell for cell in row]
        rows.append(row)
    return rows

def select_data( csv_array, heads ):
    with open("data.csv", "w") as file:
        for x in range(0,len(heads)):
            file.write(csv_array[0][heads[x]]+",")
        file.write("\n")
        for x in range(0,len(heads)):
            file.write(get_value(csv_array, heads[x])+",")
    file.close()

def get_value( csv_array, column):
    return csv_array[1][column]

# returns an array 
# [row][column]
api_object = call_api("https://api.ekmpush.com/readmeter?" \
"meters=300000369&key=MTExOjExMQ&fmt=csv&cnt=1", [0,1,2,3,4])
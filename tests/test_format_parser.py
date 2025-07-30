import sys,os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
from src.core.date_parse import DateParse
from src.core.format_parser import FormatParser
parser_instance = DateParse()
test_inputs = [
    '44561',
    'Q2 2023',
    'Quarter 1 2021',
    'Q4 21',
    'March 15, 2021',
    '15/03/2021',
    '2021-03-15',
    '2021-03-15T12:00:00',
    'not a date',
    '###',
    '59',
    '60',
    '',
    'Muhammad Usman Shahid',
    None
]
print("=== Date Test Results ===\n")
for i, test_input in enumerate(test_inputs, 1):
    result = parser_instance.parse_date(test_input)
    print(f"Test {i:02d} | Input: {repr(test_input)} -> Output: {result} | Type: {type(result)}")


parser = FormatParser()
test_values = [
    "$1,200.00",
    "(1,000.50)",
    "100K",
    "2.5M",
    "PKR 3,500",
    "USD 5.5B",
    "-4,000",
    "4,000-",
    "Rs.7,500"
]

print("=== Currency Test Results ===\n")
for i, val in enumerate(test_values):
    result = parser.clean_amount(val)
    print(f"Test {i+1:02} | Input: {val:<15} --> Output: {result} ({type(result).__name__})")
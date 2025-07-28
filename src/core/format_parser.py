from dateutil import parser
from datetime import datetime, timedelta
import re
class FormatParser:
    def normalize_currency(self, currency):
        currency_symbols = ('$', '₹', '€', '£', '¥', '₽', '₩', 'Rs.', 'Rs', 'USD', 'EUR', 'PKR')
        currency = str(currency).strip()
        for symbol in currency_symbols:
            currency = currency.replace(symbol, '')
        return currency.strip()
    def detect_format(self,value):
        if ',' in value and '.' in value:
            return 'european' if value.rfind(',') > value.rfind('.') else 'american'
        #elif ',' in value:
            #return 'european'
        #else:
            #return 'american'

    def handle_special_formats(self,value):
        value = str(value).strip()
        if value.startswith('(') and value.endswith(')'):
            value = '-' + value[1:-1]
            return value
        if value.endswith('-'):
            value = '-' + value[:-1]
            return value
        multiplier = 1
        if value.endswith(('K', 'k')):
            multiplier = 1_000
            value = value[:-1]
            return str(float(value)*multiplier)
        elif value.endswith(('M', 'm')):
            multiplier = 1_000_000
            value = value[:-1]
            return str(float(value)*multiplier)
        elif value.endswith(('B', 'b')):
            multiplier = 1_000_000_000
            value = value[:-1]
            return str(float(value)*multiplier)
        return value
    def parse_amount(self,value):
        fmt = self.detect_format(value)
        if fmt == 'european':
            value = value.replace('.', '')
            value = value.replace(',', '.')
        else: 
            value = value.replace(',', '')
        return value
    def clean_amount(self, value):
        value = self.normalize_currency(value)
        value = self.handle_special_formats(value)
        value = self.parse_amount(value)
        try:
            return int(float(value))
        except:
            return str(value)


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


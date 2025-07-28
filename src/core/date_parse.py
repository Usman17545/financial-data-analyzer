from dateutil import parser
from datetime import datetime, timedelta
import re
class DateParse:
    def parse_date(self, value):
        value = str(value).strip()
        try:
            if value.isdigit():
                serial = int(value)
                if serial > 59:
                    base = datetime(1899, 12, 30)
                    return base + timedelta(days=serial)
        except:
            pass
        quarter_match = re.match(r'(?:Q([1-4])[\s\-]?(\d{2,4}))|(?:Quarter\s*([1-4])\s+(\d{2,4}))', value, re.IGNORECASE)
        if quarter_match:
            q1, y1, q2, y2 = quarter_match.groups()
            quarter = int(q1 or q2)
            year = int(y1 or y2)
            if year < 100:
                year += 2000
            month = (quarter - 1) * 3 + 1
            return datetime(year, month, 1)
        try:
            return parser.parse(value).date()
        except:
            return str(value)
        
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
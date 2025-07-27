from dateutil import parser
from datetime import datetime, timedelta
import re
class FormatParser:
    def normalize_currency(self, currency):
        currency_symbols = ('$', '₹', '€', '£', '¥', '₽', '₩', 'Rs.', 'Rs', 'USD', 'EUR', 'PKR')
        currency = str(currency).strip()
        for symbol in currency_symbols:
            if currency.startswith(symbol):
                currency = currency[len(symbol):].strip()
        for symbol in currency_symbols:
            if currency.endswith(symbol):
                currency = currency[:-len(symbol)].strip()
        return currency
    def detect_format(self,value):
        if ',' in value and '.' in value:
            return 'european' if value.rfind(',') > value.rfind('.') else 'american'
        elif ',' in value:
            return 'european'
        else:
            return 'american'

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
    def parse_date(self, value):
        value = str(value).strip()
        try:
            if value.isdigit():
                serial = int(value)
                if serial > 59:
                    base = datetime(1899, 12, 30)
                    return (base + timedelta(days=serial)).strftime('%Y-%m-%d')
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
            return f"{year}-{month:02d}-01"
        try:
            dt = parser.parse(value)
            return dt.strftime('%Y-%m-%d')
        except:
            return None


p1 = FormatParser()
s= p1.normalize_currency("2.5m")
s= p1.handle_special_formats(s)
s=p1.parse_amount(s)
print(s)
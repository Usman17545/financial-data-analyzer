from dateutil.parser import parse
class DataTypeDetector:
    def is_date(self,val):
        try:
            parse(val, fuzzy=False)
            return True
        except:
            return False
    def analyze_column(self, data):
        print(f"Analyze Column : {data.name}")
        print(f"Number of Values : {len(data)}")
        print(f"Missing Values : {data.isnull().sum()}")
        print(f"First 5 Values : {data.head(5).tolist()}")
        result = self.detect_column_type(data)
        print(f"Detected Type: {result['type']}")
        print(f"Confidence Scores: Date={result['date_confidence']}, Number={result['number_confidence']}, String={result['string_confidence']}")
    def detect_column_type(self, column_data):
        clean_data = column_data.dropna()
        if clean_data.empty or column_data.isnull().mean() > 0.8:
            print(f"Skipping column '{column_data.name}' (Too many nulls) or (Column is Empty)")
            return {
                "type": "unknown",
                "date_confidence": 0,
                "number_confidence": 0,
                "string_confidence": 0
            }
        col_name = column_data.name.lower()
        if 'date' in col_name or 'period' in col_name:
            return {
                "type": "date",
                "date_confidence": 1,
                "number_confidence": 0,
                "string_confidence": 0
            }
        currency_symbols = ['$', '₹', '€', '£', '¥', '₽', '₩', 'Rs.', 'Rs', 'USD', 'EUR', 'PKR', ',', '%']
        total = len(clean_data)
        number_count = 0
        date_count = 0
        for val in clean_data:
            val_str = str(val).strip()
            if self.is_date(val_str):
                date_count += 1
                continue
            for sym in currency_symbols:
                val_str = val_str.replace(sym, '')
            if val_str.replace('.', '', 1).isdigit():
                number_count += 1
        date_conf = date_count / total
        number_conf = number_count / total
        string_conf = round(1 - max(date_conf, number_conf), 2)
        if date_conf > 0.8:
            dtype = "date"
        elif number_conf > 0.8:
            dtype = "number"
        else:
            dtype = "string"
        return {
            "type": dtype,
            "date_confidence": round(date_conf, 2),
            "number_confidence": round(number_conf, 2),
            "string_confidence": string_conf
        }
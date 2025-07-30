import sys,os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
from src.core.excel_processor import ExcelProcessor
from src.core.type_detector import DataTypeDetector 
processor = ExcelProcessor()
typedetector = DataTypeDetector()
files = [
    #"F:/ML IPYNB/financial-data-parser/data/sample/Customer_Ledger_Entries_FULL.xlsx",
    "F:/ML IPYNB/financial-data-parser/data/sample/KH_Bank.xlsx"
]
for paths in files:
    df1 = processor.load_files(paths)
    sheets = processor.get_sheet_info(df1)     
    for sheet_name,df2 in sheets:
        print(f"\n--- {sheet_name} ---")
        processor.preview_data(sheet_name,df2)
        for column in df2.columns:
            typedetector.analyze_column(df2[column])
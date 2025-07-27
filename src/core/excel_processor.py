import pandas as pd
import os
class ExcelProcessor:
    def __init__(self):
        self.files = {}
    def load_files(self, path):
        try:
            xl = pd.ExcelFile(path, engine="openpyxl")
            print(f"Loaded File Path : {path}")
            file_name = os.path.basename(path)
            print(f"Loaded File Name : {file_name}")
        except Exception as e:
                print(f"Error Loading {path}: {e}")
        return xl
    def get_sheet_info(self, xl):
        sheet_data = []
        for sheet in xl.sheet_names:
            try:
                df_sheet = xl.parse(sheet)
                print(f"Sheet Name : {sheet}")
                print(f"Shape : {df_sheet.shape}")
                print(f"Columns in Sheet : {list(df_sheet.columns)}")
                sheet_data.append((sheet, df_sheet))
            except Exception as e:
                print(f"Error In Loading Sheet {sheet} : {e}") 
        return sheet_data
    def preview_data(self,sheet_name, df, rows = 5):
        try:
            print(f"Sheet Name : {sheet_name}")
            print(df.head(rows))
            return 
        except Exception as e:
            print(f"Error In Loading Sheet {sheet_name} : {e}")



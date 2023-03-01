import pandas as pd
import os


# 1 This function adds a row into a spreadsheet without rewriting a file
def add_a_row_to_xlsx(path: str, df: pd.DataFrame, sheet_title: str = 'Sheet1') -> None:
    if not os.path.exists(path):
        df.to_excel(path, sheet_name=sheet_title, index=False)
    else:
        with pd.ExcelFile(path, engine='openpyxl') as reader:
            sheet_titles = reader.sheet_names
            if sheet_title in sheet_titles:
                info = reader.parse(sheet_name=sheet_title)
                rows = len(info)
                start = rows + 1
                with pd.ExcelWriter(path, mode='a', engine='openpyxl', if_sheet_exists='overlay') as writer:
                    df.to_excel(writer, startrow=start, sheet_name=sheet_title, index=False, header=False)
            else:
                with pd.ExcelWriter(path, mode='a', engine='openpyxl', if_sheet_exists='overlay') as writer:
                    df.to_excel(writer, startrow=0, sheet_name=sheet_title, index=False)



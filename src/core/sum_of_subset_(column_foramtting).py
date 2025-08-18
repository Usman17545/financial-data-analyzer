import pandas as pd

df1 = pd.read_excel('F:/ML IPYNB/financial-data-parser/data/sample/Customer_Ledger_Entries_FULL.xlsx')
df2 = pd.read_excel('F:/ML IPYNB/financial-data-parser/data/sample/KH_Bank.xlsx')

print(df1['Document No.'].count())
print(df1['Amount'].count())

df1_final = df1[['Document No.', 'Amount']].copy()

# Apply unique identifier
df1_final['Document No.'] = (
    df1_final.groupby('Document No.').cumcount() + 1
).astype(str).radd(df1_final['Document No.'] + "_")

target = df2[['Statement.Entry.Amount.Value']].copy()
target['Statement.Entry.Amount.Value'] = target['Statement.Entry.Amount.Value'].apply(lambda x: f"{x:.2f}")
amount_list = list(target['Statement.Entry.Amount.Value'])
ledger_dict = dict(zip(df1_final['Document No.'], df1['Amount']))

target_amount_column = amount_list

print("done")

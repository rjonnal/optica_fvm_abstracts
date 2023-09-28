# Use field_nicknames.py dictionary to create a spreadsheet with shorter
# more programming-friendly headers.

from field_nicknames import nicknames
import pandas as pd

input_df = pd.read_csv('abstracts_2023_original_headers.csv')

new_cols = []

for col in input_df.columns:
    try:
        new_cols.append(nicknames[col])
    except:
        new_cols.append(col)

input_df.columns = new_cols
input_df.to_csv('abstracts_2023.csv')

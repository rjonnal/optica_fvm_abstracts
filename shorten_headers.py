# Use field_nicknames.py dictionary to create a spreadsheet with shorter
# more programming-friendly headers.

from field_nicknames import nicknames
import pandas as pd

input_filename = sys.argv[1]
output_filename = sys.argv[2]

input_df = pd.read_csv(input_filename)

new_cols = []

for col in input_df.columns:
    try:
        new_cols.append(nicknames[col])
    except:
        new_cols.append(col)

input_df.columns = new_cols
input_df.to_csv(output_filename)

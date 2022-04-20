import os
import pandas as pd

DIRPATH = 'data\lnc2rna_data'

n_rows = 0

for filename in os.listdir(DIRPATH):
    f = os.path.join(DIRPATH, filename)
    df = pd.read_csv(f)
    n_rows += df.shape[0]

    print(df.columns)

print(f"Total number of rows: {n_rows}")
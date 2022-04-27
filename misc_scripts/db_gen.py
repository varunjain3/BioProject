from tabnanny import filename_only
import pandas as pd
import re
import os

FILEPATH = 'g4hunter_added_sheets\\g4hunter_added_1Colorectal.csv'

NR_REGEX = r'NR_\d*.\d*'

def gen_lncrna_data(filename):
    df = pd.read_csv(filename)

    cols = list(df.columns[:7])
    cols.append('NCBI Reference Number')

    df = df[cols]
    df = df.drop(['Remarks'], axis=1)
    df = df[:-2]

    # print(df.columns)
    # print(df.head())

    error_rows = []

    df_new = pd.DataFrame()

    for index, row in df.iterrows():
        try:
            nrs = re.findall(NR_REGEX, row[cols[-1]])
            row[-2] = int(len(nrs))
            df_new = df_new.append(row[:-1])
        except:
            error_rows.append(index)

    # print(df_new.tail())
    filename_new = filename.split('\\')[-1]
    print(filename_new, len(error_rows))
    df_new.to_csv(os.path.join('lnccancer_db', filename_new), header=False)

for filename in os.listdir('./g4hunter_added_sheets'):
    filename = os.path.join("g4hunter_added_sheets",filename)
    gen_lncrna_data(filename)
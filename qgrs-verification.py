import pandas as pd
import numpy as np
import os

files = []

LNC2FILLED_PATH = 'data\lnc2rna_filled_data'
QGRS_PATH = 'data\qgrs'

NCBIRNO = 'NCBI Reference Number'
N2G = 'No. of 2G PQS'
N3G = 'No. of 3G PQS'
N4G = 'No. of 4G PQS'

ncbi_to_num = {}

for filename in os.listdir(QGRS_PATH):
    if '.csv' in filename and 'parsed_' not in filename:
        files.append(filename)

for filename in files:
    curdf = pd.read_csv(os.path.join(QGRS_PATH, 'parsed_'+filename))
    curdf[N2G] = curdf[N2G].astype(int)
    curdf[N3G] = curdf[N3G].astype(int)
    curdf[N4G] = curdf[N4G].astype(int)
    for _, row in curdf.iterrows():
        ncbi_to_num[row[NCBIRNO]] = (row[N2G], row[N3G], row[N4G])

mismatches = {}
absentees = {}
correct = 0

for filename in files:
    scrapeddf = pd.read_csv(os.path.join(QGRS_PATH, filename))
    for _, row in scrapeddf.iterrows():
        curtup = (row['# of 2g'], row['# of 3g'], row['# of 4g'])
        curncbi = row[NCBIRNO]

        if curncbi not in ncbi_to_num:
            absentees[curncbi] = curtup

        else:
            if curtup != ncbi_to_num[curncbi]:
                mismatches[curncbi] = {
                    'automated': curtup,
                    'hand-scraped': ncbi_to_num[curncbi],
                    'sheet_name': filename,
                    'qgrs_url': row['tableURL'],
                    'fast_url': row['fasta_url']
                }
            else:
                correct += 1


import json
# dump mismatches to json
with open('data/qgrs/mismatches.json', 'w') as f:
    json.dump(mismatches, f)


print(f"Number of mismatches among hand-scraped and automated: {len(mismatches)}")
print(f"Number of matching: {correct}")
print(f"Number of values not present in hand-scrapped: {len(absentees)}")
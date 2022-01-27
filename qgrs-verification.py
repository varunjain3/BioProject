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

sheet_ncbi_num = {}

for filename in files:
    curdf = pd.read_csv(os.path.join(QGRS_PATH, 'parsed_'+filename))
    curdf[N2G] = curdf[N2G].astype(int)
    curdf[N3G] = curdf[N3G].astype(int)
    curdf[N4G] = curdf[N4G].astype(int)
    for _, row in curdf.iterrows():
        ncbi_to_num[row[NCBIRNO]] = (row[N2G], row[N3G], row[N4G])

mismatches = {}
absentees = {}

for filename in files:
    scrapeddf = pd.read_csv(os.path.join(QGRS_PATH, filename))
    for _, row in scrapeddf.iterrows():
        curtup = (row['# of 2g'], row['# of 3g'], row['# of 4g'])
        curncbi = row[NCBIRNO]

        if curncbi not in sheet_ncbi_num:
            absentees[curncbi] = curtup

        else:
            if curtup != sheet_ncbi_num[curncbi]:
                mismatches[curncbi] = {
                    'scraped_qgrs': curtup,
                    'our_sheet': sheet_ncbi_num[curncbi]
                }

print(mismatches)
# print(absentees)
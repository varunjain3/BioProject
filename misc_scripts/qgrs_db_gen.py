import pandas as pd
import re
import os

FILEPATH = 'g4hunter_added_sheets\\g4hunter_added_1Colorectal.csv'

NR_REGEX = r'NR_\d*.\d*'
NG_REGEX = r'\d+'

done_lncrnas = {}

def process(filepath):

    df = pd.read_csv(filepath)
    df = df[:-2]
    # print(df.columns[-8:])

    cols = ['LncRNA name',
        'NCBI Reference Number', 'Total No. of PQS', 'No. of 2G PQS',
        'No. of 3G PQS', 'No. of 4G PQS', ]
    cols+=list(df.columns[-8:])

    # print(cols)

    df = df[cols]
    # df[cols[2]] = df[cols[2]].apply(lambda x: re.findall(r'NR_\d*.\d*', x))
    # df[cols[4]] = df[cols[4]].apply(lambda x: re.findall(r'\d+', x))
    # df[cols[5]] = df[cols[5]].apply(lambda x: re.findall(r'\d+', x))
    # df[cols[6]] = df[cols[6]].apply(lambda x: re.findall(r'\d+', x))

    error_rows = []

    clean_df = pd.DataFrame()

    for index, row in df.iterrows():
        try:
            lncrna = row[cols[0]]
            if lncrna not in done_lncrnas.keys():
                row[cols[1]] = re.findall(NR_REGEX, row[cols[1]])
                # row[cols[3]] = re.findall(NG_REGEX, row[cols[3]])
                # row[cols[4]] = re.findall(NG_REGEX, row[cols[4]])
                # row[cols[5]] = re.findall(NG_REGEX, row[cols[5]])
                for colno in range(3,len(cols)):
                    row[cols[colno]] = re.findall(NG_REGEX, row[cols[colno]])
                clean_df = clean_df.append(row)
            done_lncrnas[lncrna] = True

        except:
            error_rows.append(index)

    new_data = {
        'lncrnaname': [],
        'n_trans_vars': [],
        'ncbi_ref_id': [],
        'n2g': [],
        'n3g': [],
        'n4g': [],
        'g49tot': [],
        'g492': [],
        'g493': [],
        'g494': [],
        'g414tot': [],
        'g4142': [],
        'g4143': [],
        'g4144': []
    }

    for index, row in clean_df.iterrows():
        ntv = len(row[cols[1]])
        for i in range(ntv):
            new_data['lncrnaname'].append(row[cols[0]])
            new_data['n_trans_vars'].append(ntv)
            new_data['ncbi_ref_id'].append(row[cols[1]][i])
            new_data['n2g'].append(row[cols[3]][i])
            new_data['n3g'].append(row[cols[4]][i])
            new_data['n4g'].append(row[cols[5]][i])
            new_data['g49tot'].append(row[cols[6]][i])
            new_data['g492'].append(row[cols[7]][i])
            new_data['g493'].append(row[cols[8]][i])
            new_data['g494'].append(row[cols[9]][i])
            new_data['g414tot'].append(row[cols[10]][i])
            new_data['g4142'].append(row[cols[11]][i])
            new_data['g4143'].append(row[cols[12]][i])
            new_data['g4144'].append(row[cols[13]][i])

    df_new = pd.DataFrame(new_data)

    # print(df_new.head())

    filename_new = filepath.split('\\')[-1]
    # print(filename_new)
    df_new.to_csv(os.path.join('qgrs_g4_db', filename_new), header=False)

    print(filename_new, len(error_rows))

for filename in os.listdir('./g4hunter_added_sheets'):
    filename = os.path.join("g4hunter_added_sheets",filename)
    process(filename)

# process(FILEPATH)
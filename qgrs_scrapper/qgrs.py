import pandas as pd
import re
import pickle
import sys
from tqdm import tqdm
from utility import get_QGRS_data

# SHEET = 2
def get_qgrs(sheet):

    print(sheet)
    database = pd.read_csv(f"./data/lnc2rna_filled_data/{sheet}")
    # ref_ids = database['NCBI Reference Number'].dropna().reset_index(drop=True)

    new_db = database[database['NCBI Reference Number'].notna()]
    new_db = new_db[new_db['No. of 2G PQS'].notna()]
    new_db = new_db[new_db['No. of 3G PQS'].notna()]
    new_db = new_db[new_db['No. of 4G PQS'].notna()]

    # ref_ids = pd.read_csv(f'./excel_{SHEET}_ncbi_ref_ids.csv', header=None)
    # print(ref_ids.head())
    new_ncbi_ref_list_all = new_db['NCBI Reference Number'].apply(lambda x: re.findall(r'NR_\d*.\d*', x))
    new_2g_list_all = new_db['No. of 2G PQS'].apply(lambda x: re.findall(r'\d+', x))
    new_3g_list_all = new_db['No. of 3G PQS'].apply(lambda x: re.findall(r'\d+', x))
    new_4g_list_all = new_db['No. of 4G PQS'].apply(lambda x: re.findall(r'\d+', x))
    # ncbi_ref_list_all = ref_ids.apply(lambda x: re.findall(r'NR_\d*.\d*', x))

    original_parsed_df = pd.DataFrame(columns = ['NCBI Reference Number', "No. of 2G PQS", "No. of 3G PQS", "No. of 4G PQS"])

    list_nnrla = list(new_ncbi_ref_list_all)

    for i in range(len(list_nnrla)):
        for j in range(len(list_nnrla[i])):
            try:
                cur = {"NCBI Reference Number": list_nnrla[i][j],
                "No. of 2G PQS": new_2g_list_all[i][j],
                "No. of 3G PQS": new_3g_list_all[i][j],
                "No. of 4G PQS": new_4g_list_all[i][j],
                }

                original_parsed_df = original_parsed_df.append(cur, ignore_index=True)

            except:
                print(f"Missing value at: {i}, {j}")

    original_parsed_df.to_csv(f'./data/qgrs/parsed_{sheet}')

    # ncbi_ref_list_all = [['NR_026690.1', 'NR_038264.1', 'NR_047540.1']]
    temp_list = []
    new_ncbi_ref_list_all.apply(lambda x: temp_list.extend(x))
    ncbi_ref_set = set(temp_list)
    print('\nTotal ncbi_ref_ids: ', len(ncbi_ref_set))
    aka_list_all = {}

    df = pd.DataFrame(columns = ['NCBI Reference Number', 'fasta',
       'fasta_url', '# of 2g', '# of 3g', '# of 4g', 'tableURL'])

    for ncbi_ref in tqdm(ncbi_ref_set):
       df = df.append(get_QGRS_data(ncbi_ref),ignore_index=True)

    df.to_csv(f'./data/qgrs/{sheet}', index=False)

if __name__ == "__main__":
    from multiprocessing.pool import ThreadPool as Pool
    pool_size = 9  # your "parallelness"
    pool = Pool(pool_size)

    mapping = [
        "1Colorectal.csv",
        "2Ovarian.csv",
        "3Pancreatic.csv",
        "4Cervical.csv",
        "5Gastric.csv",
        "6Head and neck.csv",
        "7Lung.csv",
        "8Liver.csv",
        "9Prostate.csv",
    ]


    for item in mapping:
            pool.apply_async(get_qgrs, (item,))

    pool.close()
    pool.join()

    # for sheet in mapping:
    #     get_qgrs(sheet)
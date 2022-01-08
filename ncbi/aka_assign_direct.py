import pickle
import pandas as pd
from tqdm import tqdm
import re
# >>> with open('parrot.pkl', 'rb') as f:
# ...   mynewlist = pickle.load(f)


def get_aka_from_ids(aka_list_all, ncbi_ref_list):
    aka = ''
    isval = True

    for ncbi_ref in ncbi_ref_list:
        if isval == False:
            continue
        if aka_list_all[ncbi_ref] == '':
            isval = False
        if aka == '':
            aka = aka_list_all[ncbi_ref]
        elif aka_list_all[ncbi_ref] != aka:
            isval = False

    if isval == False:
        aka = ''
    
    return aka

# mapping between orignal_data and lnc2rna_data
mapping = [
    "1Colorectal.xlsx",
    "2Ovarian.xlsx",
    "3Pancreatic.xlsx",
    "4Cervical.xlsx",
    "5Gastric.xlsx",
    "6Head and neck.xlsx",
    "7Lung.xlsx",
    "8Liver.xlsx",
    "9Prostate.xlsx",
]

for sheet in mapping:
    print(sheet)
    sheet_num = int(sheet[0])
    with open(f'excel_{sheet_num}_aka_list_all.pkl', 'rb') as f:
        aka_list_all = pickle.load(f)

    database = pd.read_excel(f"../data/lnc2rna_filled_data/{sheet}",sheet_name="Validated & Reviewed GQ LncRNAs")
    new = pd.DataFrame(columns=database.columns)

    
    filled = 0
    filled_empty = 0
    for i, row in tqdm(database.iterrows()):
        flag = 1
        if pd.isnull(row).all():
            continue

        if pd.isnull(row["NCBI Reference Number"]):
            flag = 0
        elif not pd.isnull(row["Remarks"]):
            flag = 0

        if flag:
            ncbi_ref_list = re.findall(r'NR_\d*.\d*', row['NCBI Reference Number'])
            aka = get_aka_from_ids(aka_list_all, ncbi_ref_list)
            row['Remarks'] = f'Also Known As: {aka}'
            filled += 1
            if aka == '':
                filled_empty += 1
            # else:
            #     print(f'Change at row {i}\n{row}')
        
        new = new.append(row)
    
    print(f'Total filled: {filled}\nTotal filled empty: {filled_empty}')
    new.to_excel(f"{sheet.split('.')[0]}_remarks.xlsx",sheet_name='Validated & Reviewed GQ LncRNAs',header=1,index=False)
# final_df = pd.DataFrame([ncbi_ref_list_all]).T
# final_df[1] = aka_final
# print(final_df)
# final_df.to_csv(f'excel_{SHEET}.csv', index=False, header=False)
# # print(aka_final)
# print(f'Total entries: {len(aka_final)}\nTotal empty strings: {count, count1+count2}\nEmpty strings of second kind: {count2}')


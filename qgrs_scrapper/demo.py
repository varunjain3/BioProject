from utility import get_QGRS_data
import os
import pandas as pd
import re
from tqdm import tqdm

def qgrs_to_sheet(file):
    data = pd.read_csv(os.path.join(r"ncbi\aka_scraped\dups_removed",file))

    dataset = pd.read_csv(os.path.join(r"data\qgrs",file[13:]))

    new_df = pd.DataFrame(columns=data.columns)

    for i, row in tqdm(data.iterrows()):
        try:
            ncbi_ids = list(map(lambda x: re.findall(r'NR_\d*.\d*', x),[row["NCBI Reference Number"]]))[0]
            _2g = []
            _3g = []
            _4g = []

            for ncbi_id in ncbi_ids:    
                scraped_Data = dataset[dataset["NCBI Reference Number"] == ncbi_id]
                # results = get_QGRS_data(ncbi_id)
                _2g.append(scraped_Data["# of 2g"].values[0])
                _3g.append(scraped_Data["# of 3g"].values[0])
                _4g.append(scraped_Data["# of 4g"].values[0])

            if len(ncbi_ids) != len(_2g):
                raise Exception("Number of 2g sequences does not match number of NCBI IDs")

            row["No. of 2G PQS"] = ",".join(map(str,_2g))
            row["No. of 3G PQS"] = ",".join(map(str,_3g))
            row["No. of 4G PQS"] = ",".join(map(str,_4g))

        except Exception as e:
            print(e)
            print(f"{file} - {row['NCBI Reference Number']}")

        new_df = pd.concat([new_df,pd.DataFrame(row).T],ignore_index=True)

    new_df.to_csv(os.path.join(r"ncbi\aka_scraped\dups_removed\qgrs_filled","qgrs_added_"+file[13:]),index=False)






if __name__ == "__main__":

    temp = ["dups_removed_3Pancreatic.csv","dups_removed_4Cervical.csv"]

    for _,_,files in os.walk(r"ncbi\aka_scraped\dups_removed"):
        for file in files:
            if (not file.endswith(".csv") or "dups_removed_4Cervical.csv" in file) and not "dups_removed" in file  :
                continue 
            temp.append(file)

    for t in temp:
        qgrs_to_sheet(t)
    
    # multiprocess function
    # from multiprocessing import Pool
    # pool = Pool(processes=9)
    # pool.map(qgrs_to_sheet, temp)
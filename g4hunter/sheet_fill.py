import os 
import pandas as pd
import re


from tqdm import tqdm
from final import g4hunter_numgs,g4hunter_seq

DATA_PATH =  r"lncrna_only1"



find_ncbi = lambda x: re.findall(r'NR_\d*.\d*', x)

if __name__ == "__main__":
    for filename in os.listdir(DATA_PATH):
        if filename.endswith(".csv"):
            
            file = pd.read_csv(os.path.join(DATA_PATH, filename))
            dataset = pd.read_csv(os.path.join(r"data\qgrs",filename[11:]))

            df = pd.DataFrame(columns=file.columns)


            for i,row in tqdm(file.iterrows()):
                
                try:
                    for thres in [0.9,1.4]:
                    
                        _2g = []
                        _3g = []
                        _4g = []
                        _total = []

                        ncbi_ids = find_ncbi(row["NCBI Reference Number"])

                        for ncbi_id in ncbi_ids:
                            _2g.append(0)
                            _3g.append(0)
                            _4g.append(0)
                            _total.append(0)

                            scraped_Data = dataset[dataset["NCBI Reference Number"] == ncbi_id]
                            seq = scraped_Data["fasta"].values[0]
                            data = g4hunter_seq(seq,threshold=thres)

                            for k,v in data.items():
                                if v["score"] > 0:
                                    if v['num_g'] == 2:
                                        _2g[-1] += 1
                                        _total[-1] += 1
                                    elif v['num_g'] == 3:
                                        _3g[-1] += 1
                                        _total[-1] += 1
                                    elif v['num_g'] == 4:
                                        _4g[-1] += 1
                                        _total[-1] += 1
                                else:   
                                    continue
                            
                        row[f"G4 Hunter, thres:{thres} TOTAL PQS"] = ",".join(map(str,_total)) 
                        row[f"G4 Hunter, thres:{thres} 2G PQS"] = ",".join(map(str,_2g))
                        row[f"G4 Hunter, thres:{thres} 3G PQS"] = ",".join(map(str,_3g))
                        row[f"G4 Hunter, thres:{thres} 4G PQS"] = ",".join(map(str,_4g))
                except Exception as e:
                    print(e)
                df = pd.concat([df, pd.DataFrame(row).T], ignore_index=True)  
            df.to_csv(f"./g4hunter_added_sheets/{filename}", index=False)               

                        # if v['num_g'] 


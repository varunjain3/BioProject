import pandas as pd
from tqdm import tqdm

# mapping between orignal_data and lnc2rna_data
mapping = {
    "1. Database-LncRNAs-Colorectal Cancer.xlsx": "Colorectal.csv",
    "2. Database-LncRNAs-Ovarian Cancer.xlsx": "Ovarian.csv",
    "3. Database-LncRNAs-Pancreatic Cancer.xlsx": "Pancreatic.csv",
    "4. Database-LncRNAs-Cervical Cancer.xlsx": "Cervical.csv",
    "5. Database-LncRNAs-Gastric Cancer.xlsx": "Gastric.csv",
    "6. Database-LncRNAs-Head and neck Cancer.xlsx": "Head and neck.csv",
    "7. Database-LncRNAs-Lung Cancer.xlsx": "Lung.csv",
    "8. Database-LncRNAs-Liver Cancer.xlsx": "Liver.csv",
    "9. Database-LncRNAs-Prostate Cancer.xlsx": "Prostate.csv",
}

index = 0
for key, value in mapping.items():
        
    database = pd.read_excel(f"./data/orignal_data/{key}",sheet_name="Validated & Reviewed GQ LncRNAs",header=1)

    search = pd.read_csv("./data/lnc2rna_data/{}".format(value))

    new = pd.DataFrame(columns=database.columns)

    fail = 0 
    success = 0
    filled = 0
    for i, row in tqdm(database.iterrows()):
        
        flag = 0
        if pd.isnull(row).all():

            continue
        
        if pd.isnull(row["Cancer name"]):
            flag = 1
        if pd.isnull(row["Methods"]):
            flag = 1
        if pd.isnull(row["Expression pattern"]):
            flag = 1
        if pd.isnull(row["Pubmed ID"]):
            flag = 1
        
        if pd.isnull(row["LncRNA name"]) and i>0:
            temp = new.iloc[-1]
            temp[["Cancer name","Methods","Expression pattern","Pubmed ID"]] = row[["Cancer name","Methods","Expression pattern","Pubmed ID"]]
            row = temp
            


        if flag:
            data = search[search["Lnc/ CircRNA name"] == row["LncRNA name"]]
            if pd.isnull(row["LncRNA name"]) or isinstance(row["LncRNA name"],int):
                new = new.append(row)
                continue

            if len(data) == 0:
                if len(row["LncRNA name"].split()) > 1:
                    data = search[search["Lnc/ CircRNA name"] == row["LncRNA name"].split()[0]]
                    if len(data) == 0:
                        fail += 1
                        new = new.append(row)
                else:
                    fail += 1
                    new = new.append(row)
                

            
            for i, search_data in data.iterrows():
                row["Cancer name"] = search_data["Cancer name"]
                row["Methods"] = search_data["Methods"]
                row["Expression pattern"] = search_data["Expression pattern"]
                row["Pubmed ID"] = search_data["Pubmed ID"]
                new = new.append(row)
                success += 1
            
            
        else:
            filled += 1
            new = new.append(row)

    index += 1 
    print("For file {}: {} success, {} fail, {} already filled".format(key, success, fail, filled))
    new.to_csv("./data/lnc2rna_filled_data/{}{}".format(index,value),index=False)



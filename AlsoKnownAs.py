import bs4
import pandas as pd
import numpy as np
import os


header = 1


sheet_name = "Validated & Reviewed GQ LncRNAs"

for _,_,files in os.walk("./data"):
    for file in files:

        if "~$" in file:
            continue
        try:
            df = pd.read_excel(f"./data/{file}",
                            sheet_name=sheet_name, header=header)
        except:
            print("Correct Sheet Name")
            exit()

        print("Checking for file: ", file)
        for i, row in df.iterrows():
            row_num = i+header+2

            if pd.isnull(row["Cancer name"]):
                print(file, row_num, "Cancer name")
            if pd.isnull(row["Methods"]):
                print(file, row_num, "Methods")
            if pd.isnull(row["Expression pattern"]):
                print(file, row_num, "Expression pattern")
            if pd.isnull(row["Pubmed ID"]):
                print(file, row_num, "Pubmed ID")


print("hello")

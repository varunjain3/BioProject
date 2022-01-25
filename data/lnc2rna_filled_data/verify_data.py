import pandas as pd
import os

for _, _, files in os.walk("./data/lnc2rna_filled_data"):
    for file in files:
        if file.endswith(".csv"):
            file_name = "./data/lnc2rna_filled_data/" + file
            df = pd.read_csv(file_name)
            data = pd.read_csv("./data/lnc2rna_data/" + file[1:])

            names_in_data = list(map(lambda x: x.lower(),set(data["Lnc/ CircRNA name"].values)))
            names_in_df = list(map(lambda x: x.split()[0].lower(),set(df["LncRNA name"].values)))

            with open("verify_data.txt", "a") as f:
                f.write(file_name + ":\n")
                for name in names_in_data:
                    if name not in names_in_df:
                        f.write(name + "\n")
            
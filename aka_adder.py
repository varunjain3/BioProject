import os 
import pandas as pd

DATA_PATH =  r"ncbi\aka_scraped\dups_removed\qgrs_filled"


if __name__ == "__main__":
    for filename in os.listdir(DATA_PATH):
        if filename.endswith(".csv"):
            
            file = pd.read_csv(os.path.join(DATA_PATH, filename))

            df = pd.DataFrame(columns=file.columns)
            for i,row in file.iterrows():
                names = row["LncRNA name"].strip().split("\n")

                if not pd.isna(row["Expression pattern"]):
                    row["Cancer name"] = row["Cancer name"].lower().title()
                if len(names) > 1 and not pd.isna(row["Expression pattern"]):
                    row["LncRNA name"] = names[0]
                    row['aka'] += f"; {'; '.join(names[1:])}"


                df = pd.concat([df, pd.DataFrame(row).T], ignore_index=True)
            
            df.to_csv(f"./lncrna_only1/{filename}", index=False)
                
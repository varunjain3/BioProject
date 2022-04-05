# opens the gene_ids and makes a dictionary

import pandas as pd

lncatlas = {}

with open('data/subcellular/gene_ids.txt') as f:
    gene_ids = f.readlines()
    for gene in gene_ids:
        gene = gene.strip().split(':')
        if gene[1] == " NOT AVAILABLE":
            lncatlas[gene[0]] = None
            continue
        lncatlas[gene[0]] = gene[1]

if __name__ == "__main__":

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
    genes = []
    ids = []

    for sheet in mapping:
        database = pd.read_csv("./data/lnc2rna_filled_data/{sheet}".format(sheet=sheet))
        names = database["LncRNA name"].values
        names = [genes.append(name) for name in names]

    genes = pd.unique(genes)

    for gene in genes:
        for key, value in lncatlas.items():
            if key in gene and not value is None:
                ids += [value]
                break
        else:
            ids += [None]
    
    # make dataframe and write to csv
    df = pd.DataFrame(list(zip(genes, ids)), columns=['gene_id', 'lncatlas_id'])
    df.to_csv('data/subcellular/gene_id_missing.csv', index=False)

    print()

        
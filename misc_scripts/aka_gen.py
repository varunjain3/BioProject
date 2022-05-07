import pandas as pd
import os

FILEPATH = 'g4hunter_added_sheets\\g4hunter_added_1Colorectal.csv'

done_lncrnas = {}
new_data = {
    'lncrnaname': [],
    'aka': []
}

def generate_aka_data(filename):
    df = pd.read_csv(filename)
    cols = ['LncRNA name', 'aka']
    df = df[cols]
    df = df[:-2]
    

    prob = 0

    for index, row in df.iterrows():
        if row[cols[0]] not in done_lncrnas.keys():
            try:
                akas = row[cols[1]].split(';')
                for aka in akas:
                    new_data['lncrnaname'].append(row[cols[0]])
                    new_data['aka'].append(aka)
                done_lncrnas[row[cols[0]]] = True
            except:
                prob+=1
                print(row[cols[1]])

    print(prob)
    # new_df.to_csv('aka_data.csv', header=False)

for filename in os.listdir('./g4hunter_added_sheets'):
    filename = os.path.join("g4hunter_added_sheets",filename)
    generate_aka_data(filename)

new_df = pd.DataFrame(new_data)
new_df.to_csv('aka_db.csv', header=False)
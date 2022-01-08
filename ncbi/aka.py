from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import Select
from selenium.webdriver.edge.options import Options
import pandas as pd
import re
import pickle
import sys
from tqdm import tqdm

# SHEET = 2
def get_aka(SHEET):
    driver = webdriver.Edge('./msedgedriver.exe')

    print(sheet)
    database = pd.read_excel(f"../data/lnc2rna_filled_data/{sheet}",sheet_name="Validated & Reviewed GQ LncRNAs")
    ref_ids = database['NCBI Reference Number'].dropna().reset_index(drop=True)
    # ref_ids = pd.read_csv(f'./excel_{SHEET}_ncbi_ref_ids.csv', header=None)
    # print(ref_ids.head())
    ncbi_ref_list_all = ref_ids.apply(lambda x: re.findall(r'NR_\d*.\d*', x))

    # ncbi_ref_list_all = [['NR_026690.1', 'NR_038264.1', 'NR_047540.1']]
    temp_list = []
    ncbi_ref_list_all.apply(lambda x: temp_list.extend(x))
    ncbi_ref_set = set(temp_list)
    print('Total ncbi_ref_ids: ', len(ncbi_ref_set))
    aka_list_all = {}
    ctr = 1
    for ncbi_ref in tqdm(ncbi_ref_set):
        print(ctr)
        ctr+=1
        # aka_list = ''
        url = f'https://www.ncbi.nlm.nih.gov/nuccore/{ncbi_ref}'
        print(url)
        driver.get(url)

        print(driver.title)

        try: 
            portlet = driver.find_element_by_id('ui-portlet_content-4').find_element_by_tag_name('a')
            gene_url = portlet.get_attribute('href')
        except:
            aka_list_all[ncbi_ref] = ''
            continue
        print(gene_url) 
        driver.get(gene_url)

        try:
            summary = driver.find_element_by_id('summaryDl')
        except:
            pass
        
        try: 
            aka = summary.find_element_by_xpath("./dt[.='Also known as']/following-sibling::dd").text
        except:
            aka = ''

        if aka != '':
            # aka_list.extend([x.strip() for x in aka.split(';')])
            # aka_list = aka
            print(aka)
        else:
            print('Aka not found')

        aka_list_all[ncbi_ref] = aka



        # aka_list_all.append(aka_list)
    print(aka_list_all)

    if len(aka_list_all.values()) == len(ncbi_ref_set):
        with open(f'excel_{SHEET}_aka_list_all.pkl', 'wb') as f:
            pickle.dump(aka_list_all, f)

    # >>> with open('parrot.pkl', 'rb') as f:
    # ...   mynewlist = pickle.load(f)

if __name__ == "__main__":
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
        get_aka(sheet)

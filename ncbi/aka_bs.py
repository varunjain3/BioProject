# from bs4 import BeautifulSoup
# import requests

# ncbi_ref = 'NR_026690.1'
# url = f'https://www.ncbi.nlm.nih.gov/nuccore/{ncbi_ref}'
# print(url)
# page = requests.get(url)
# soup = BeautifulSoup(page.content, 'html.parser')

# print(len(soup.find_all('div', class_ ='portlet')))

# from selenium import webdriver
# from selenium.webdriver.common.keys import Keys
# from selenium.webdriver.support.ui import Select
# from selenium.webdriver.edge.options import Options
from selenium import webdriver
from bs4 import BeautifulSoup
import requests
import pandas as pd
import re
import pickle
import sys
from requests.api import request
from tqdm import tqdm

# SHEET = 2
def get_aka(SHEET):

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
    for ncbi_ref in ncbi_ref_set:
        print(ctr)
        ctr+=1
        # aka_list = ''
        base_url = f'https://www.ncbi.nlm.nih.gov/'
        url1 = f'{base_url}nuccore/{ncbi_ref}'
        print(url1)
        page = requests.get(url1)
        soup = BeautifulSoup(page.text, "html.parser")

        for element in soup.find_all('a', href=True):
            if '/sites/entrez' in element['href']:
                url2 = base_url + element['href'] 
                break
        else:
            print("Not Found for {}".format(url1))

        print(url2)
        page = requests.get(url2)
        soup = BeautifulSoup(page.text, "html.parser")

        for element in soup.find_all('dt', text="Primary source"):
            for sub in element.findNextSiblings():
                if sub.name == 'dd':
                    url3 = sub.find('a', href=True)['href']
                    break

        driver = webdriver.Edge('./msedgedriver.exe')
        url3 = 'https://www.genecards.org/cgi-bin/carddisp.pl?id_type=hgnc&id=44352'
        print(url3)
        # page = driver.get(url3).page_source
        page = requests.get(url3)
        soup = BeautifulSoup(page.text, "html.parser")

        for element in soup.find_all('a', href=True):
            print(element['href'])
            # if 'genecards' in element['href']:
            #     print(element['href'])
            #     break




    #     try: 
    #         portlet = driver.find_element_by_id('ui-portlet_content-4').find_element_by_tag_name('a')
    #         gene_url = portlet.get_attribute('href')
    #     except:
    #         aka_list_all[ncbi_ref] = ''
    #         continue
    #     print(gene_url) 
    #     driver.get(gene_url)

    #     try:
    #         summary = driver.find_element_by_id('summaryDl')
    #     except:
    #         pass
        
    #     try: 
    #         aka = summary.find_element_by_xpath("./dt[.='Also known as']/following-sibling::dd").text
    #     except:
    #         aka = ''

    #     if aka != '':
    #         # aka_list.extend([x.strip() for x in aka.split(';')])
    #         # aka_list = aka
    #         print(aka)
    #     else:
    #         print('Aka not found')

    #     aka_list_all[ncbi_ref] = aka



    #     # aka_list_all.append(aka_list)
    # print(aka_list_all)

    # if len(aka_list_all.values()) == len(ncbi_ref_set):
    #     with open(f'excel_{SHEET}_aka_list_all.pkl', 'wb') as f:
    #         pickle.dump(aka_list_all, f)

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

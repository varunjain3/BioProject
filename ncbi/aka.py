from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import Select
import pandas as pd
import re
import pickle

driver = webdriver.Edge('./msedgedriver.exe')

ref_ids = pd.read_csv('./ncbi_ref_ids.csv', header=None)
# print(ref_ids.head())
ncbi_ref_list_all = ref_ids[0].apply(lambda x: re.findall(r'NR_\d*.\d*', x))
print('Total ncbi_ref_ids: ', len(ncbi_ref_list_all))

# ncbi_ref_list_all = [['NR_026690.1', 'NR_038264.1', 'NR_047540.1']]
aka_list_all = {}
ctr = 1
for ncbi_ref_list in ncbi_ref_list_all:
    print(ctr)
    ctr+=1
    # aka_list = ''
    for ncbi_ref in ncbi_ref_list:
        url = f'https://www.ncbi.nlm.nih.gov/nuccore/{ncbi_ref}'
        print(url)
        driver.get(url)

        print(driver.title)

        # select = Select(driver.find_element_by_id('database'))
        # select.select_by_visible_text('Nucleotide')

        # search_bar = driver.find_element_by_name("term")
        # search_bar.clear()
        # search_bar.send_keys("NR_026690.1")
        # search_bar.send_keys(Keys.RETURN)

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

with open('ncbi_ref_list_all.pkl', 'wb') as f:
    pickle.dump(ncbi_ref_list_all, f)

with open('aka_list_all.pkl', 'wb') as f:
    pickle.dump(aka_list_all, f)

# >>> with open('parrot.pkl', 'rb') as f:
# ...   mynewlist = pickle.load(f)



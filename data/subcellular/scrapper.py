from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import Select
from selenium.webdriver.edge.options import Options
import urllib.request
import pandas as pd
import re
import pickle
import sys
from tqdm import tqdm
import time

# SHEET = 2
def get_graphs_lncAtlas(names):
    driver = webdriver.Edge('./msedgedriver.exe')
    driver.set_window_size(1900, 1080)

    print(sheet)
    
    
    temp_list = []
    print('Total unique genes: ', len(names))
    aka_list_all = {}
    ctr = 1

    url = f'https://lncatlas.crg.eu/'
    print(url)
    driver.get(url)
    print(driver.title)
    checkbox1 = driver.find_element_by_xpath('/html/body/div[2]/div[2]/div[1]/div[3]/div/div/div/div[1]/div[3]/div[1]/div/div/div[1]/label/input')
    checkbox1.click()
    checkbox2 = driver.find_element_by_xpath('/html/body/div[2]/div[2]/div[1]/div[3]/div/div/div/div[1]/div[3]/div[2]/div/div/div[1]/label/input')
    checkbox2.click()

    ratio_img = None
    distribution_image = None
    gene_id_check = None

    for name in tqdm(names):

        print(ctr)
        ctr+=1
        flag = 0
        try: 
            # find input box with xpath and enter the gene name
            input_box = driver.find_element_by_xpath('/html/body/div[2]/div[2]/div[1]/div[3]/div/div/div/div[1]/div[1]/div/input')
            input_box.clear()
            input_box.send_keys(name)
            gobutton = driver.find_element_by_xpath('/html/body/div[2]/div[2]/div[1]/div[3]/div/div/div/div[1]/div[2]/div[3]/button')

            while True:
                try:
                    # find text field by xpath
                    gene_id = driver.find_element_by_xpath('//*[@id="geneId"]')
                    # get the text from the text field
                    gene_id_text = gene_id.get_attribute('value')

                    if gene_id_check is None or gene_id_text != gene_id_check:
                        gene_id_check = gene_id_text
                    elif gene_id_check == gene_id_text:
                        raise('gene_id_text is the same')
                    
                    # append to txt file
                    with open('./data/subcellular/gene_ids.txt','a') as f:
                        f.write(f"{name}: {gene_id_text.split(',')[0]}" + '\n')
                    break
                except Exception:
                    print('waiting')
                    time.sleep(2)
                    try:
                        check_cross = driver.find_element_by_xpath('//*[@id="ID"]/div/i')
                        if check_cross.is_displayed():
                            with open('./data/subcellular/gene_ids.txt','a') as f:
                                f.write(f"{name}: NOT AVAILABLE" + '\n')
                        flag = 1
                        break
                    except Exception:
                        pass

            if flag:
                continue


            
            gobutton.click()
            time.sleep(20)
            
            while True:
                try:
                    img1 = driver.find_element_by_xpath('//*[@id="ratioPlot"]/img')
                    src1 = img1.get_attribute('src')

                    if ratio_img is None or src1 != ratio_img:
                        ratio_img = src1
                    elif ratio_img == src1:
                        raise('ratio image is the same')
                    

                    urllib.request.urlretrieve(src1, f"data\subcellular\images\{name}_ratio.png")
                    img2 = driver.find_element_by_xpath('//*[@id="distributionAlt"]/img')
                    src2 = img2.get_attribute('src')
                    urllib.request.urlretrieve(src2, f"data\subcellular\images\{name}_distribution.png")
                    break
                except Exception:
                    print('No images found for ', name)
                    time.sleep(2)






            print("hello")
        except Exception as e:
            print(e)

def split(a, n):
    k, m = divmod(len(a), n)
    return (a[i*k+min(i, m):(i+1)*k+min(i+1, m)] for i in range(n))

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

    for sheet in mapping:
        database = pd.read_csv("./data/lnc2rna_filled_data/{sheet}".format(sheet=sheet))
        names = pd.unique(database["LncRNA name"].values)
        names = [genes.extend(name.split()) for name in names]

    genes = pd.unique(genes)

    with open('./data/subcellular/gene_ids.txt', 'r') as f:
        gene_ids = f.readlines()
    genes = genes[len(gene_ids):]

    get_graphs_lncAtlas(genes)
    # from multiprocessing.pool import ThreadPool as Pool
    # pool_size = 10  # your "parallelness"
    # pool = Pool(pool_size)

    # r = pool.map_async(get_graphs_lncAtlas,  list(split(genes, pool_size)))
    # r.wait()

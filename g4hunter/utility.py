import requests as req
from bs4 import BeautifulSoup as bs
import requests


def get_fasta_and_link(NCBI_ID):
    
    for i in range(5):
        reqUrl = "https://eutils.ncbi.nlm.nih.gov/entrez/eutils/efetch.fcgi?db=nuccore&id=" + \
            NCBI_ID+"&rettype=fasta&retmode=text"
        response = requests.request("GET", reqUrl)
        if len("".join(response.text.split("\n")[1:])) > 0:
            break
        else:
            pass
            # print("Retrying...")

    return "".join(response.text.split("\n")[1:]), reqUrl


def get_QGRS_data(NCBI_ID):

    # make request to the server for an ID
    seq, url = get_fasta_and_link(NCBI_ID)
    results = {"NCBI Reference Number": NCBI_ID,
               "fasta": seq,
               "fasta_url": url}

    data = {"sequence": seq}
    options = {
        "Enabled": "true",        # set params
        "QGRSmax": "45",
        "GGroupmin": "2",
        "loop_min": "0",
        "loop_max": "36"
    }

    inputURL = "https://bioinformatics.ramapo.edu/QGRS/analyze.php"
    r = req.post(inputURL, data=data, cookies=options)

    # parse response from server, get link for "QGRS sequences without overlaps"
    # that contains the table we're interested in
    soup = bs(r.text, 'html.parser')
    # print("".join(soup.findAll('font')[1].strings))  # to confirm search parameters
    link = soup.body.find('img', {"src": "data.gif"}).parent
    baseURL = "https://bioinformatics.ramapo.edu/QGRS/dataview.php/"
    outputURL = baseURL+link['href']

    results["tableURL"] = outputURL

    # visit the link and get table
    r = req.get(outputURL)
    soup = bs(r.text, 'html.parser')
    table = soup.find('table')

    # count number of 2G,3G,4G,5G,6G sequences
    table_rows = table.find_all('tr')[1:]
    gees = [0, 0, 0, 0, 0, 0, 0]
    for tr in table_rows:
        seq = tr.find_all('td')[2]
        gees[len(seq.find_all('u')[0].text)] += 1

    results["# of 2g"] = gees[2]
    results["# of 3g"] = gees[3]
    results["# of 4g"] = gees[4]
    if gees[5] > 0:
        print(f"5g sequence found, please check manually for: {NCBI_ID}")
        # raise Exception("5g sequence found")
        results["# of 5g"] = gees[5]
    if gees[6] > 0:
        raise Exception("6g sequence found")
        results["# of 6g"] = gees[6]

    return results

if __name__ == '__main__':
    get_QGRS_data("NR_152759.1")
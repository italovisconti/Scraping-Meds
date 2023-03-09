import pandas as pd
from pandas import option_context
import requests
from bs4 import BeautifulSoup

# The first row of the table is the header
def getHeader(med):
    header = []
    for title in med.findAll('th'):
        header.append(title.text)
    
    header.pop()
    header.pop()
    header.pop()
    return header

# Convert the list to a dataframe and export it to Excel (including the header)
def toExcel(meds_list, header):

    pd.set_option('display.max_colwidth', None)

    df = pd.DataFrame(meds_list, columns=header)

    df.to_excel('meds.xlsx', index=False)
    print('Data exported to Excel!')

def main():

    # URL
    url = 'https://cnas.ro/lista-medicamente/'
    # Get the HTML
    r = requests.get(url)
    html = r.text
    # Parse the HTML
    soup = BeautifulSoup(html, 'html.parser')
    
    meds = soup.findAll('tr')
    header = getHeader(meds[0])
    # Remove the header from the list
    meds.remove(meds[0])

    meds_list = []
    # Iterate through the rows, but only the first 60 (there are about 8000 rows, but my computer can't handle that many)
    # you can remove the range(60) if you want to get all the rows
    for index, med in zip(range(60), meds):
        medInfo = []
        info = med.findAll('td')
        for x in range(14): #I only need the first 14 columns
            medInfo.append(info[x].text)

        meds_list.append(medInfo)

    print('Data scraped!')
    toExcel(meds_list, header)


if __name__ == '__main__':
    main()
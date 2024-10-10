# Imported requests, urllib3 & BeatifulSoup to successfully scrap the price of the BCV Page
import requests, urllib3, time, datetime
inicio = time.time()
urllib3.disable_warnings()
from bs4 import BeautifulSoup
from configparser import ConfigParser

# # Variables
# file = 'src\\config.ini'
# now = datetime.datetime.now()
# date = now.strftime("%d-%m-%y")

def scraping_Parallel():
    config = ConfigParser()
    # Scrap part
    page_to_scrape = requests.get('https://t.me/s/enparalelovzlatelegram', verify=False)
    #TODO Use status code for execeptions. https://github.com/terremoth/get-dollar-value-py/blob/master/dolar-value.py
    # if page_to_scrape.status_code == 200
    soup = BeautifulSoup(page_to_scrape.text, 'html.parser')
    
    # Find the div with the specific class
    div = soup.find('div', class_='tgme_widget_message_text js-message_text')

    # Extract all text from the div
    text = div.get_text()

    # Find the line containing "Bs."
    for line in text.split('\n'):
        if " Bs." in line:
            price = line.strip()  # Clean up whitespace
            print(price)  # Output: Bs. 47,53
            break
    # # Formating part
    # list_BCV = list(parent_container.find('strong').text.strip()) #  Result = ['3', '6', ',', '1', '8', '8', '3', '0', '0', '0', '0']
    # list_BCV.remove(',') # Result = ['3', '6', '1', '8', '8', '3', '0', '0', '0', '0']
    # list_BCV.insert(2, '.') #Result = ['3', '6', '.', '1', '8', '8', '3', '0', '0', '0', '0']

    # str_BCV = ''.join(list_BCV) # Formating list into a single string 36.18830000.



scraping_Parallel()
    # # Creating and Adding sections and values to the config.ini
    # config.add_section('Date')
    # config.set("Date", 'Date_Now', date)
    # config.add_section('BCV_Price')
    # config.set('BCV_Price', 'BCV_Price',str_BCV)
    # config.add_section('Language')
    # config.set('Language', 'lang', 'es') 
    
    # with open(file, 'w') as configfile:
    #     config.write(configfile)

    # price_BCV = float(str_BCV) # Casting string into a float.
    
    # Q.put(price_BCV)
    # final = time.time()
    # print('Ejecucion del scrap BCV')
    # print(final - inicio)
    # # print(price_BCV) # Result = 36.1883
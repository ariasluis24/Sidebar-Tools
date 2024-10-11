# Imported requests, urllib3 & BeatifulSoup to successfully scrap the price of the BCV Page
import requests, urllib3, time
inicio = time.time()
urllib3.disable_warnings()
from bs4 import BeautifulSoup
from configparser import ConfigParser

# # Variables
# file = 'src\\config.ini'
# now = datetime.datetime.now()


def scraping_Parallel():
    config = ConfigParser()
    # Scrap part
    page_to_scrape = requests.get('https://t.me/s/enparalelovzlatelegram', verify=False)
    #TODO Use status code for execeptions. https://github.com/terremoth/get-dollar-value-py/blob/master/dolar-value.py
    # if page_to_scrape.status_code == 200
    soup = BeautifulSoup(page_to_scrape.text, 'html.parser')

    for br in soup.find_all('br'):
        br.replace_with('\n')
    
    # Find the div with the specific class
    div = soup.find('div', class_='tgme_widget_message_text js-message_text')

    # Extract all text from the div
    info_price = div.get_text()

    # Find the line containing "Bs."
    # for line in text.split('\n'):
    #     if " Bs." in line:
    #         price = line.strip()  # Clean up whitespace
    #         print(price)  # Output: Bs. 47,53
    return info_price

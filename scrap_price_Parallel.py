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

    try:
        page_to_scrape = requests.get('https://t.me/s/enparalelovzlatelegram', verify=False)
        soup = BeautifulSoup(page_to_scrape.text, 'html.parser')
        #TODO Use status code for execeptions. https://github.com/terremoth/get-dollar-value-py/blob/master/dolar-value.py
        if page_to_scrape.status_code == 200:
            print(page_to_scrape.status_code)

            # Lista de emojis que queremos filtrar
            emojis_requeridos = {'🗓', '🕒', '💵', '🔻','🔺','🟰'}

            # Lista para almacenar los resultados que cumplen los criterios
            resultados = []

            # Recorrer los elementos <i> y filtrar por los criterios deseados
            for i_tag in soup.find_all('i', class_='emoji'):
                # Verificar si tiene la propiedad 'background-image:url'
                style = i_tag.get('style', '')
                if 'background-image:url' in style:
                    emoji = i_tag.get_text(strip=True)  # Obtener el emoji

                    # Comprobar si el emoji es uno de los requeridos
                    if emoji in emojis_requeridos:
                        # Buscar el siguiente texto relevante
                        next_text = i_tag.find_next_sibling(string=True)
                        text = next_text.strip() if next_text else 'Texto no encontrado'


                        if emoji == '🟰': # If the emojis is equal to 🟰 changed for a '='
                            
                            emoji = '\n='
                        
                        elif emoji == '🔻' : # If the emoji is equal to '🔻', add and break line next to the emoji.
                            
                            emoji = '\n🔻'
                        
                        elif emoji == '🔺': # If the emoji is equal to '🔻', add and break line next to the emoji.
                            
                            emoji = '\n🔺'   
                        
                        
                        # Almacenar el emoji y su texto en la lista de resultados
                        resultados.append([emoji, text])

            # Takes on the last 17 results.
            last_results = resultados[-17:]
            
            # # Print the last emojis and its text
            # for emoji, text in last_results:
            #     if emoji == '🗓':
            #         print(f'\n{emoji}: {text}')
            #     print(f'{emoji}: {text}')
            return list(reversed(last_results))
        
        else:
        
            return f'''Failed to load content\nHTTP code: {page_to_scrape.status_code}\n\nPlease wait\n a few minutes.\n\nOr check\n Internet Connection.'''
    
    except Exception as e:
        
        print(e)


def scraping_Parallel_Calculator():
    config = ConfigParser()
    # Scrap part
    #TODO Use status code for execeptions. https://github.com/terremoth/get-dollar-value-py/blob/master/dolar-value.py
    try:
        page_to_scrape = requests.get('https://t.me/s/enparalelovzlatelegram', verify=False)
        if page_to_scrape.status_code == 200:
            print(page_to_scrape.status_code)
            soup = BeautifulSoup(page_to_scrape.text, 'html.parser')

            # Lista de emojis que queremos filtrar
            emojis_requeridos = {'💵'}

            # Lista para almacenar los resultados que cumplen los criterios
            resultados = []

            # Recorrer los elementos <i> y filtrar por los criterios deseados
            for i_tag in soup.find_all('i', class_='emoji'):
                # Verificar si tiene la propiedad 'background-image:url'
                style = i_tag.get('style', '')
                if 'background-image:url' in style:
                    emoji = i_tag.get_text(strip=True)  # Obtener el emoji

                    # Comprobar si el emoji es uno de los requeridos
                    if emoji in emojis_requeridos:
                        # Buscar el siguiente texto relevante
                        next_text = i_tag.find_next_sibling(string=True)
                        text = next_text.strip() if next_text else 'Texto no encontrado'

                        # Almacenar el emoji y su texto en la lista de resultados
                        resultados.append([emoji, text])

            # Takes on the last result (string).
            last_result = resultados[-1:]
            
            # Takes the second item of the list which is text.
            converted = last_result[0][1]
            
            # Slice the text to have only the digits.
            cut_str:str = converted[4:]

            # Replace the , of the text with a . to be usable as a float.
            return cut_str.replace(',', '.')
        else:
            return f'''Failed to load price\nHTTP code {page_to_scrape.status_code}'''
    
    except Exception as e:
        print(e)

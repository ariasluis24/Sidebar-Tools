'''
This module is made to scrape the data from a Telegram group chat, where the parallel price is posted twice a day.
Sadly this group is also full with ads that are not needed.
With some logic behind the posts we actually need there a function that helps to get the specified values.
'''

'''
The main process of the scrap and the logic behind to get values we need:
1. Make a request get to the telegram group chat.
2. If the request returns a code of 200, proceeds if not, sends an error.
3. An list of sets emojis is declared.
4. An empty list is created.
5. A function to detected if a selected div contains the list of sets emojis is created.
6. The scraps begins getting all the <a> elements with the class 'tgme_widget_message_photo_wrap' (<a class='tgme_widget_message_photo_wrap'>...</a>).
7. Then for every <a> element looks for the next sibling that is a <div></div> with a class 'tgme_widget_message_text'.
7.1 Example of what are we getting from the scrap:
    
    <a class="tgme_widget_message_photo_wrap 5096060348783504926 1186519011_456240670" href="https://t.me/enparalelovzlatelegram/11273" style="width:800px;background-image:url('https://cdn1.cdn-telegram.org/file/thebackgroundpicurl.jpg')">
    </a>
    <div class="tgme_widget_message_text js-message_text before_footer" dir="auto">
    # ! <i class="emoji" style="background-image:url('//telegram.org/img/emoji/40/F09F9793.png')"><b>🗓</b></i> 09/12/2024<br>
    # ! <i class="emoji" style="background-image:url('//telegram.org/img/emoji/40/F09F9592.png')"><b>🕒</b></i> 01:25 PM<br>
    # ! <i class="emoji" style="background-image:url('//telegram.org/img/emoji/40/F09F92B5.png')"><b>💵</b></i> Bs. 56,77<br>
    # ! <i class="emoji" style="background-image:url('//telegram.org/img/emoji/40/F09F94BA.png')"><b>🔺</b></i> 0,21% Bs 0,12<span style="display: inline-block; width: 99px;"></span>
    </div>
    The red comments are the <i> tag elements we want to scrap the text values.

8. Once the <div> next to the <a> element is found is inspected by the function 'contains_valid_emoji_subset'
9. If the function returns True, loops the <i> elements inside the <div> and extracts the text within the <i></i>, in this case the text extracted would result in a emoji: '🗓', '🕒', '💵', '🔻'.
10. Next, finds the next sibling of the <i> element that would be plain text. Here relies all the values we need to extract.
11. Next, if the emoji scraped is one of this '🟰', '🔻' '🔺', adds a '\n' to the beginning  of the text.
12. Finally appends both 'emoji_scraped' & 'text_scraped' into a list, that will, in turn, go into another list.
13. Returns the values in a reversed list.
'''

# TODO: Make a scrap price getting it from the image. To avoid errors
# TODO: When finished the scrap, on both ways, compared and used the higher value.
 
# # Variables
# file = 'src\\config.ini'
# now = datetime.datetime.now()

def scraping_Parallel():
    
    # Scrap part
    try:
        # Imported requests, urllib3 & BeautifulSoup to successfully scrap the price of the BCV Page
        import requests, urllib3
        urllib3.disable_warnings()
        from bs4 import BeautifulSoup
        # from configparser import ConfigParser
        # config = ConfigParser()
        
        page_to_scrape = None
        soup = None
        results = None
        
        page_to_scrape = requests.get('https://t.me/s/enparalelovzlatelegram', verify=False)
        soup = BeautifulSoup(page_to_scrape.text, 'html.parser')
        #TODO Use status code for exceptions. https://github.com/terremoth/get-dollar-value-py/blob/master/dolar-value.py
        if page_to_scrape.status_code == 200:

            # List of sets to filter the div scraped.
            valid_emoji_set = [
                {'🗓', '🕒', '💵', '🔻'},
                {'🗓', '🕒', '💵', '🔺'},
                {'🗓', '🕒', '💵', '🟰'},
            ]

            # List to save the result that meet the requirements.
            results = []
            
            # Function to validate the emojis inside of a scraped div.
            def contains_valid_emoji_subset(div, valid_sets):
                # Find all emoji elements
                emojis = div.find_all('i', class_='emoji')
                # Extract emoji text
                emoji_texts = {emoji.b.text for emoji in emojis if emoji.b}
                # Check if the set matches any of the valid subsets
                return any(emoji_texts == valid_set for valid_set in valid_sets)
            
            # For loop to extract all the <a> tag elements from the webpage.
            for a_element in soup.find_all('a', class_='tgme_widget_message_photo_wrap'):
                # Get the sibling <div> next to the <a> tag.
                # <a></a>
                # <div> <-- This one is scraped.
                sibling_div = a_element.find_next_sibling('div', class_='tgme_widget_message_text')
                
                # If the sibling <div> has any of the set of lists, it returns True.
                if sibling_div and contains_valid_emoji_subset(sibling_div, valid_emoji_set):
                    
                    # Loops through the <i> elements with the class=emoji inside the sibling <div>.
                    for i_tag in sibling_div.find_all('i', class_='emoji'):
                        
                        # Gets the text inside the <i> element which is an emoji '🗓', '🕒', '💵', '🔻'
                        emoji_scraped = i_tag.get_text(strip=True)
                        
                        # Gets the text next to the <i> element. And deletes all the white spaces.
                        # <i>🗓</b></i> 09/12/2024 <-- This one is scraped
                        text_scraped = i_tag.find_next_sibling(string=True).strip()
                        

                        if emoji_scraped == '🟰': # If the emojis is equal to 🟰 changed for a '='
                            
                            emoji_scraped = '\n='
                        
                        elif emoji_scraped == '🔻' : # If the emoji is equal to '🔻', add and break line next to the emoji.
                            
                            emoji_scraped = '\n🔻'
                        
                        elif emoji_scraped == '🔺': # If the emoji is equal to '🔻', add and break line next to the emoji.
                            
                            emoji_scraped = '\n🔺' 

                        # Place the emojis and text in a list that will, in turn, go into another list.
                        results.append([emoji_scraped, text_scraped] )
            
            # Return the list of emojis and text reversed.        
            return list(reversed(results)) # [['🗓', '06/12/2024'], ['🕒', '8:55 AM'], ['💵', 'Bs. 57,29'], ['\n🔻', '0,73% Bs 0,42']

            # ! Old method to scrap the price
            '''
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

            # Takes on the last 18 results.
            last_results = resultados[-18:]
            
            # Print the last emojis and its text
            for emoji, text in last_results:
                if emoji == '🗓':
                    print(f'\n{emoji}: {text}')
                print(f'{emoji}: {text}')
            return list(reversed(last_results))
            '''
           
        
        else:
            # TODO: Test this else statement.
            return f'Failed to load content\nHTTP code: {page_to_scrape.status_code}\n\nPlease wait\n a few minutes.\n\nOr check\n Internet Connection.'
    
    except Exception as e:
        
        print(e)

def scraping_Parallel_Calculator():
    # Scrap part
    #TODO Use status code for exceptions. https://github.com/terremoth/get-dollar-value-py/blob/master/dolar-value.py
    try:
        # Imported requests, urllib3 & BeautifulSoup to successfully scrap the price of the BCV Page
        import requests, urllib3
        urllib3.disable_warnings()
        from bs4 import BeautifulSoup
        # from configparser import ConfigParser
        # config = ConfigParser()
        page_to_scrape2 = None
        soup2 = None

        page_to_scrape2 = requests.get('https://t.me/s/enparalelovzlatelegram', verify=False)
        soup2 = BeautifulSoup(page_to_scrape2.text, 'html.parser')
        if page_to_scrape2.status_code == 200:

            # Set of lists to filter the div scraped.
            valid_emoji_set = [
                {'🗓', '🕒', '💵', '🔻'},
                {'🗓', '🕒', '💵', '🔺'},
                {'🗓', '🕒', '💵', '🟰'},
            ]

            # List to save the result that meet the requirements.
            results = []
            
            # Function to validate the emojis inside of a scraped div.
            def contains_valid_emoji_subset(div, valid_sets):
                # Find all emoji elements
                emojis = div.find_all('i', class_='emoji')
                # Extract emoji text
                emoji_texts = {emoji.b.text for emoji in emojis if emoji.b}
                # Check if the set matches any of the valid subsets
                return any(emoji_texts == valid_set for valid_set in valid_sets)
            
            # For loop to extract all the <a> tag elements from the webpage.
            for a_element in soup2.find_all('a', class_='tgme_widget_message_photo_wrap'):
                # Get the sibling <div> next to the <a> tag.
                # <a></a>
                # <div> <-- This one to get.
                sibling_div = a_element.find_next_sibling('div', class_='tgme_widget_message_text')
                
                # If the sibling_div has any of the set of lists, it returns True.
                if sibling_div and contains_valid_emoji_subset(sibling_div, valid_emoji_set):
                    # Extract the background-image URL
                    
                    for i_tag in sibling_div.find_all('i', class_='emoji'):
            
                        emoji_scraped = i_tag.get_text(strip=True)
                        
                        if emoji_scraped in '💵':
                            next_text = i_tag.find_next_sibling(string=True)
                            price = next_text.strip() if next_text else 'Texto no encontrado'
                        
                            results.append(price) # ['Bs. 57,86', 'Bs. 57,71', 'Bs. 57,29', 'Bs. 56,84']

            cut_str:str = results[-1]

            # Replace the , of the text with a . to be usable as a float.
            final_str = cut_str[4:].strip() #! 'Bs. 56,84' => '56,84' Be careful in the future if the price increases, change the index of slicing.
            
            return final_str.replace(',', '.')
            
            # ! Old method to scrap the price
            '''
            # Recorrer los elementos <i> y filtrar por los criterios deseados
            for i_tag2 in soup2.find_all('i', class_='emoji'): 
                # Verificar si tiene la propiedad 'background-image:url'
                style = i_tag2.get('style', '')
               
                if "background-image:url('//telegram.org/img/emoji/40/F09F92B5.png')" in style:
                    emoji = i_tag2.get_text(strip=True)  # Obtener el emoji
                    # Comprobar si el emoji es uno de los requeridos
                    if emoji in emojis_requeridos:
                        # Buscar el siguiente texto relevante
                        # if len(next_text) < 9:
                        # print(next_text)
                        next_text = i_tag2.find_next_sibling(string=True)
                            
                        # If the length of the string next to the emoji is greater than 18 characters, replace the text with error.
                        if len(next_text) > 18:
                            next_text = 'Error.'
                        
                        # If not, strips the text and continous the extract of the price.
                        else:
                            text = next_text.strip() if next_text else 'Texto no encontrado'
                        # Almacenar el emoji y su texto en la lista de resultados
                            resultados.append([emoji, text])

            # Takes on the last result (string).
            last_result = resultados[-1:]
            
            # Takes the second item of the list which is text.
            converted = last_result[0][1]
            
            # Slice the text to have only the digits.
            cut_str:str = converted[4:]
            
            '''
        else:
            return f'''Failed to load price\nHTTP code {page_to_scrape2.status_code}'''
    
    except Exception as e:
        print(e)

def scraping_Parallel_Photo():
    try:
        # Imported requests, urllib3 & BeautifulSoup to successfully scrap the price of the BCV Page
        import requests, urllib3, shutil
        urllib3.disable_warnings()
        from bs4 import BeautifulSoup
        # from configparser import ConfigParser
        # config = ConfigParser()
        
        page_to_scrape = None
        soup = None
        
        page_to_scrape = requests.get('https://t.me/s/enparalelovzlatelegram', verify=False)
        soup = BeautifulSoup(page_to_scrape.text, 'html.parser')
        
        #TODO Use status code for exceptions. https://github.com/terremoth/get-dollar-value-py/blob/master/dolar-value.py
        
        if page_to_scrape.status_code == 200:
            '''
            
            This was a try to scrap the url of the background image of a div.
            for a_tag in soup.find_all('a', class_='tgme_widget_message_photo_wrap'):
                
                href = a_tag.get('href', '') # ! This gets the href tag value

                if 'href=https://t.me/enparalelovzlatelegram/11248': #! (11248) is the las image uploaded on 5/12/2024
                    style = a_tag.get('style', '')

            for a_tag in soup.find_all('a', class_='tgme_widget_message_photo_wrap'):
                style = a_tag.get('style', '') # ! This gets all inside of the style tag
                
                # Extract the URL using string manipulation
                import re
            

                if "width:720px" in style:
                    # url = style.get_text(strip=True)
                    # print(url)
                    pass

                
            for a_tag in soup.find_all('a', class_='tgme_widget_message_photo_wrap'):
                
                href = a_tag.get('href', '') # ! This gets the href tag value

                if 'href=https://t.me/enparalelovzlatelegram/11248': #! (11248) is the las image uploaded on 5/12/2024
                    style = a_tag.get('style', '')
            
            '''
        
            import re
            image_links = []
            dates = []
            # Define the valid subsets of emojis
            valid_emoji_sets = [
                {'🗓', '🕒', '💵', '🔻'},
                {'🗓', '🕒', '💵', '🔺'},
                {'🗓', '🕒', '💵', '🟰'},
            ]

            # Function to check if a <div> contains any of the valid emoji subsets
            def contains_valid_emoji_subset(div, valid_sets):
                # Find all emoji elements
                emojis = div.find_all('i', class_='emoji')
                # Extract emoji text
                emoji_texts = {emoji.b.text for emoji in emojis if emoji.b}
                # Check if the set matches any of the valid subsets
                return any(emoji_texts == valid_set for valid_set in valid_sets)
            
            for a_element in soup.find_all('a', class_='tgme_widget_message_photo_wrap'):
                # Get the sibling <div>
                sibling_div = a_element.find_next_sibling('div', class_='tgme_widget_message_text')
                if sibling_div and contains_valid_emoji_subset(sibling_div, valid_emoji_sets):
                    # Extract the background-image URL
                    style_attr = a_element.get('style', '')
                    match = re.search(r"background-image:url\('(.*?)'\)", style_attr)
                    if match:
                        image_links.append(match.group(1))

            for i_tag in soup.find_all('i', class_='emoji'):
                        
                emoji = i_tag.get_text(strip=True)
                        
                if emoji in {'🕒', '🗓'}:
                    next_text = i_tag.find_next_sibling(string=True)
                    text = next_text.strip() if next_text else 'Texto no encontrado'
                    dates.append(text)
                    
                    
            # This combine both text obtained from the previous scrap
            data = dates
            combined_dates = [f"{data[i]} {data[i+1]}" for i in range(0, len(data), 2)]

            for date, link in zip(combined_dates, image_links):
                # TODO: Find an use to this dates and links of parallel prices from previous days.
                # * This links would be on a combobox, when the date is selected it would show the image of the correspondent date.
                # print(f'{date}: {link}\n')
                pass

            # Send a GET request to the URL for download.
            response = requests.get(image_links[-1], stream=True)
            response.raise_for_status()  # Check for HTTP request errors
            output_path = "src\\Parallel\\downloaded_image.jpg"

            # Open a file in write-binary mode and save the content
            with open(output_path, "wb") as file:
                shutil.copyfileobj(response.raw, file)

            # print(f"Image successfully downloaded and saved as {output_path}")

    except Exception as e:
        print(e)
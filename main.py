from tkinter import *
from scrap_price_Parallel import scraping_Parallel, scraping_Parallel_Calculator
from scrap_price_BCV import scraping_BCV
from ping3 import ping
from decimal import Decimal 
from concurrent.futures import ThreadPoolExecutor
import datetime
import subprocess
import locale
import threading
import time
import gc 

locale.setlocale(locale.LC_ALL, 'es_VE')

igtf_calc_path = "C:\\Users\\l.arias\\Documents\\DOCUMENTOS CAJA LUIS ARIAS\\Nueva carpeta\\Python\\Nueva carpeta\\IGTF-Calc\\GUI.py"
explorer_exe_path = "C:\\Windows\\explorer.exe"
scanner_path = "C:\\Program Files (x86)\\epson\\Epson Scan 2\\Core\\es2launcher.exe"
web_browser_path = 'C:\\Program Files (x86)\\Microsoft\\Edge\\Application\\msedge.exe'
calculator_path = 'C:\\Windows\\System32\\calc.exe'
network_Test_path = "C:\\Windows\\System32\\cmd.exe"
profit_path = 'P:\\Profit_a\\profit_a.exe'
local_server_ip = 'server'  # Local server IP or domain.
internet_ip = '8.8.8.8'  # Ip used to do ping and check internet connection.

# // TODO Make just one function to open all programs.
# TODO Change the state of the button if the program is already open.

# // TODO Find a way to open the IGTF Calculator from python.
def open_igtf_calc():
    subprocess.Popen(["python", igtf_calc_path])

#// TODO Make this .bat apear in a new cmd window.
def open_Network_Test():
    # subprocess.Popen(f'start cmd.exe /K ping {1000}', shell=True)
    pass

# // TODO Make a way to check if there is connection to the server in order to open profit.
def open_Tool(tool_path):
    subprocess.Popen(tool_path)

def open_Pararel_Price_Window():

    # TODO Displayed Internet Error if the Internet connection failed when it tried the scrap.
    price_window = Toplevel(window)
    price_window.title('Parallel Price')
    price_window.geometry('180x415+850+70')
    price_window.iconbitmap('icon.ico')
    
    result = scraping_Parallel()
    
    if isinstance(result, list) == True:
        texto_lista = None
        # Unir los elementos de la lista en un solo string con saltos de línea
        texto_lista = ''.join([f"{emoji}: {valor}\n" for emoji, valor in result if len(valor) <=15])
    
    elif isinstance(result, str) == True:
        # 
        texto_lista = result
    
    else:
        texto_lista = 'An unexpected error occured.'
    
    price_title = Label(price_window, text='Parallel Price', font=('Arial', 12, 'bold'))
    
    scrap_price_label = Label(price_window, text=texto_lista, font=('Arial', 12), borderwidth=1, relief='groove')
   
    price_title.grid(row=0, column=0, columnspan=1,sticky='we')
    
    scrap_price_label.grid(row=1, column=0, padx=8,sticky='nswe')

    def on_closing_toplevel(price_window):
        
        # Ensure widgets are destroyed properly
        price_title.destroy() 
        scrap_price_label.destroy()

        
        # Destroy the price window itself
        price_window.destroy()

        # Force garbage collection and reset global variables
        gc.collect()
        
        price_window = None
        texto_lista = None
    
    price_window.protocol("WM_DELETE_WINDOW", lambda: on_closing_toplevel(price_window))

def delete_operation(amount, label, label2, label3, label4):
    amount.delete(0, 'end')
    label.config(text='Price BCV:')
    label2.config(text='Price Parallel:')
    label3.config(text='')
    label4.config(text='')

# To make the scraping of the BCV Price concurrent and avoid freezes on the main thread of the GUI.


class BCVCalculator:
    def __init__(self, master, executor):
        self.master = master
        self.executor = executor

        self.BCV_window = Toplevel(master)
        self.BCV_window.title('BCV Price')
        self.BCV_window.geometry('420x200+650+70')
        self.BCV_window.iconbitmap('icon.ico')
        self.BCV_window.columnconfigure(1, weight=1)

        self.create_widgets()
        self.BCV_window.protocol("WM_DELETE_WINDOW", self.on_closing_toplevel)
        self.start_scraping()

    def create_widgets(self):
        # Labels, Entry, Buttons
        self.sub_total_entry = Entry(self.BCV_window, font=('Arial', 14), width=14, bg='yellow', justify='center')
        self.dollar_button = Button(self.BCV_window, text='$', font=('Roboto', 8, 'bold'), width=2, height=1)
        self.calculate_button = Button(self.BCV_window, text='Calculate', command=self.calculation_BCV_Parallel, width=10)
        self.delete_button = Button(self.BCV_window, text='Delete', command=self.delete_operation, width=8)

        self.bcv_price = Label(self.BCV_window, text=f'BCV: Loading...', font=('Arial', 10), justify='center', height=4)
        self.parallel_price = Label(self.BCV_window, text=f'$ Parallel: Loading...', font=('Arial', 10), justify='center', height=4)

        self.result_operation_BCV = Label(self.BCV_window, text=f'Price BCV:', font=('Arial', 10), justify='right')
        self.result_operation_Parallel = Label(self.BCV_window, text=f'Price Parallel:', font=('Arial', 10), justify='right')
        self.differences_between_label = Label(self.BCV_window, font=('Arial', 10), justify='center')
        self.differences_percentage_label = Label(self.BCV_window, font=('Arial', 10), justify='right')

        # Position
        # Column 0
        self.sub_total_entry.grid(row=1, column=0, pady=5, padx=5, sticky='ns')
        self.dollar_button.grid(row=1, column=0, pady=8, padx=7, sticky='ne')
        self.delete_button.grid(row=2, column=0, padx=5, sticky='es')
        self.calculate_button.grid(row=2, column=0, padx=5, sticky='ws')
        self.bcv_price.grid(row=3, column=0, sticky='NS')
        self.parallel_price.grid(row=4, column=0, sticky='NS')

        # Column 1
        self.result_operation_BCV.grid(row=1, column=1)
        self.result_operation_Parallel.grid(row=2, column=1)
        self.differences_between_label.grid(row=3, column=1, pady=15)
        self.differences_percentage_label.grid(row=4, column=1)

    def start_scraping(self):
        future_BCV = self.executor.submit(scraping_BCV)
        future_Parallel = self.executor.submit(scraping_Parallel_Calculator)

        future_BCV.add_done_callback(lambda future: self.handle_scraping_result_BCV(future))
        future_Parallel.add_done_callback(lambda future: self.handle_scraping_result_Parallel(future))

    def handle_scraping_result_BCV(self, future):
        result_BCV = future.result()
        self.result_BCV_future = float(result_BCV)
        self.bcv_price.config(text=f'BCV: {result_BCV} Bs')

    def handle_scraping_result_Parallel(self, future):
        result_Parallel = future.result()
        self.result_Parallel_future = float(result_Parallel)
        self.parallel_price.config(text=f'Parallel: {result_Parallel} Bs')

    def calculation_BCV_Parallel(self):
        amount = self.sub_total_entry.get()
        try:
            amount_float = float(amount)
            result_calculation_BCV = round(Decimal(amount_float * self.result_BCV_future), 2)
            result_calculation_Parallel = round(Decimal(amount_float * float(self.result_Parallel_future)), 2)
            difference_between_prices = round(Decimal(result_calculation_Parallel - result_calculation_BCV), 2)

            difference_percentage = round(Decimal(((result_calculation_Parallel - result_calculation_BCV) / result_calculation_BCV) * 100), 2)

            self.result_operation_BCV.config(text=f'Price BCV: {result_calculation_BCV:n} Bs')
            self.result_operation_Parallel.config(text=f'Price Parallel: {result_calculation_Parallel:n} Bs')

            self.differences_between_label.config(text=f'Gap: {difference_between_prices:n} Bs')
            self.differences_percentage_label.config(text=f'Difference %: {difference_percentage:n}%')

        except ValueError:
            self.result_operation_BCV.config(text=f'Price BCV: Error en Valor Introducido')
            self.result_operation_Parallel.config(text=f'Price Parallel: Error en Valor Introducido')

    def delete_operation(self):
        self.sub_total_entry.delete(0, 'end')
        self.result_operation_BCV.config(text=f'Price BCV:')
        self.result_operation_Parallel.config(text=f'Price Parallel:')
        self.differences_between_label.config(text='')
        self.differences_percentage_label.config(text='')

    def on_closing_toplevel(self):
        self.BCV_window.destroy()
        gc.collect()

executor = ThreadPoolExecutor(max_workers=2)


# Windows entity  

window = Tk()

# Config of window
# icon = PhotoImage(file='icon.ico')
window.title('Sidebar Tools')
window.geometry('235x250+1120+290') # Default size of the window & Position.
window.attributes('-topmost',True) # Makes the window always on top.
window.iconbitmap('icon.ico')
# window.minsize(800, 370) # Minimun size of the window
# window.maxsize(800, 370) # Maximun size of the window
    

now = datetime.datetime.now()
date_actual = now.strftime('%a %d/%b/%y')

# Creating Labels

title = Label(window, text='Tools', font=('Roboto', 12, 'bold'), justify='center', width=10)

igtf_btn = Button(window, text='IGTF Calculator', font=('Arial', 10), width=12, height=1, justify='center', command=open_igtf_calc)
calculator_btn = Button(window, text='Calculator', font=('Arial', 10), width=12, height=1, justify='center',  command= lambda: open_Tool(calculator_path))
web_browser_btn = Button(window, text='Web Browser', font=('Arial', 10), width=12, height=1, justify='center',  command= lambda: open_Tool(web_browser_path))
profit_btn = Button(window, text='Profit', font=('Arial', 10), width=12, height=1, justify='center', command= lambda: (open_Tool(profit_path), open_Tool(profit_path)))
scanner_btn = Button(window, text='Scanner', font=('Arial', 10), width=12, height=1, justify='center',  command= lambda: open_Tool(scanner_path))
explorer_btn = Button(window, text='File Explorer', font=('Arial', 10), width=12, height=1, justify='center',  command= lambda: open_Tool(explorer_exe_path))
date_label = Label(window, text=date_actual, font=('Arial', 10,'bold'))
version_label = Label(window, text='Version: Beta 1.2', font=('Arial', 7))


server_status = Label(window, text='', font=('Arial', 10), bg='green', fg='white')
server_ping = Label(window, text='', font=('Arial', 8))
internet_status = Label(window, text='', font=('Arial', 10), height=1, bg='green', fg='white')
internet_ping = Label(window, text='', font=('Arial', 8))
bcv_parallel_btn = Button(window, text='BCV Calculator', font=('Arial', 10), width=5, height=1, justify='center',  command=lambda: BCVCalculator(window, executor))
scrap_price_btn = Button(window, text='Get Parallel Price', font=('Arial', 10), width=13, height=1, justify='center', command=open_Pararel_Price_Window)

# // TODO Make this function infinitely run in the background.     


def ping_Server():
    def ping_and_update():
        while True:
            response_server = ping(local_server_ip, unit='ms')
            
            try:
                rounded_response = round(response_server, 2) if isinstance(response_server, float) else None

                # Condition when the server responds correctly for the first time or the connection comes back.
                if isinstance(response_server, float) and server_status.cget('text') in ['', 'Host Unknown', 'Check Internet', 'Time Out', 'Check Ethernet']:
                    server_status.config(text='Server Connected', fg='white', bg='green')
                    update_status(server_ping, f'Ping: {rounded_response} ms')
                    profit_btn.config(state='normal')
                

                # Condition when the server keeps responding
                elif isinstance(response_server, float) and server_status.cget('text') == 'Server Connected':
                    update_status(server_ping, f'Ping: {rounded_response} ms')
                
                    
                # Condition when the server doesnt respond (Disconnection)
                elif response_server is False:
                    server_status.config(text='Host Unknown', fg='white', bg='red')
                    update_status(server_ping, '-')
                    profit_btn.config(state='disabled')
                

                # Condition when the server doesnt respond (Timed Out)
                elif response_server is None:
                    server_status.config(text='Timed Out', fg='white', bg='red')
                    update_status(server_ping, '-')
                    profit_btn.config(state='disabled')
                time.sleep(1)

            except TimeoutError as e:
                return f"Timeout Error: {e}"
           
            except OSError as e:
                return f"Operating system Error: {e}"

            except Exception as e:
                return f"Unexpected Error: {e}"  

    threading.Thread(target=ping_and_update, daemon=True).start()


def ping_Internet():
    
    def ping_and_update():
        while True:
            response_Internet = ping(internet_ip, unit='ms')
            
            try:
                rounded_response = round(response_Internet, 2) if isinstance(response_Internet, float) else None
                
                # Condition when the ping to the IP Address responds correctly for the first time or the connection comes back.
                if isinstance(response_Internet, float) and internet_status.cget('text') in ['', 'Host Unknown', 'Check Internet', 'Timed Out', 'Check Ethernet']:
                    internet_status.config(text='Internet Connected', fg='white', bg='green')
                    update_status(internet_ping, f'Ping: {rounded_response} ms')
                    profit_btn.config(state='normal')
                
                # Condition when the IP Address keeps responding to ping
                elif isinstance(response_Internet, float) and internet_status.cget('text') == 'Internet Connected':
                    update_status(internet_ping, f'Ping: {rounded_response} ms')
                
                # Condition when the IP Address doesnt respond (Disconnection)
                elif response_Internet is False:
                    internet_status.config(text='Host Unknown', fg='white', bg='red')
                    update_status(internet_ping, '-')
                    profit_btn.config(state='disabled')  

                # Condition when the IP Address doesnt respond (Timed Out)
                elif response_Internet is None:
                    internet_status.config(text='Timed Out', fg='white', bg='red')
                    update_status(internet_ping, '-')
                    profit_btn.config(state='disabled')
                
                time.sleep(1)
                
            except TimeoutError as e:
                return f"Timeout Error: {e}"
            
            except OSError as e:
                return f"Operating system Error: {e}"
            
            except Exception as e:
                return f"Unexpected Error: {e}" 
        
    threading.Thread(target=ping_and_update, daemon=True).start()

def update_status(label_ping, ping_text=''):
    if label_ping.cget('text') != ping_text:  # Update only if different
        label_ping.config(text=ping_text)

"""


def ping_Internet():
    # TODO Update only the label where the value of ping (ms) is displayed instead of the whole Label.
    internet_ip= '8.8.8.8' # Ip used to do ping and check internet connection.
    
    def internet_ping_and_update():

        response_internet = ping(internet_ip, unit='ms')
        
        try:
            if type(response_internet) == float and internet_status.cget('text') == '':

                rounded_response = round(response_internet, 2)
                
                internet_status.config(text='Internet Connected', fg='white', bg='green')

                if response_internet > 0 or response_internet == 0.0 and response_internet is not False:
                    # window.after(0, lambda: update_status('Server Connected', f'Ping: {rounded_response} ms', 'green', 'white'))
                    update_status(internet_ping, f'Ping: {rounded_response} ms')
                    print(f"First if Reached {internet_ip} {response_internet}")
                         
            elif type(response_internet) == float and internet_status.cget('text') == 'Internet Connected':
               
                rounded_response = round(response_internet, 2)
                
                if response_internet > 0 or response_internet == 0.0 and response_internet is not False:
                    # window.after(0, lambda: update_status('Server Connected', f'Ping: {rounded_response} ms', 'green', 'white'))
                    update_status(internet_ping, f'Ping: {rounded_response} ms')
                    print(f"Reached {internet_ip} {response_internet}")
                   
            
            elif response_internet == False:
                # window.after(0, lambda: update_status('Host Unknown', '-', 'red', 'yellow'))

                update_status(internet_ping, '-')
                internet_status.config(text='Host Unknown', fg='white', bg='red')    
                print(f"Host Unknown {internet_ip}")

            elif response_internet == None:
                # server_status.config(text='Server Timed Out')
                    
                internet_status.config(text='Timed Out', fg='white', bg='red')    
                update_status(internet_ping, '-')
                print(f"Timed Out {internet_ip}")
                
                # window.after(2000, ping_Server)
            
            else:
                internet_status.config(text='Check Ethernet', fg='white', bg='red')
                update_status(internet_ping, '-')
                print('Check Ethernet')
     
        
        except TimeoutError as e:
            print(f"Timeout error occurred: {e}")
        
        except OSError as e:
            print(f"OS error occurred: {e}")
        
        except Exception as e:
            print(f"An unexpected error occurred: {e}")
    

    window.after(1000, ping_Internet)

    threading.Thread(target=internet_ping_and_update, daemon=True).start()

    # os.system('cls')
"""

window.after(0, ping_Server)
window.after(0, ping_Internet)

# Label Position
# Column 0

# window.columnconfigure(0, weight=1)
title.grid(row=0, column=0, columnspan=2,sticky='nwse')
igtf_btn.grid(row=1, column=0, padx=3, pady=2, sticky='')
calculator_btn.grid(row=2, column=0, padx=3, pady=2,sticky='')
web_browser_btn.grid(row=3, column=0, padx=3, pady=2,sticky='')
profit_btn.grid(row=4, column=0, padx=3, pady=2, sticky='')
scanner_btn.grid(row=5, column=0, padx=3, pady=2, sticky='')
explorer_btn.grid(row=6, column=0, padx=3, pady=2)
date_label.grid(row=9, column=0, pady=5, sticky='s')


# Column 1
server_status.grid(row=1, column=1, pady=5, sticky='we')
server_ping.grid(row=2, column=1, sticky='we')
internet_status.grid(row=3, column=1, sticky='we')
internet_ping.grid(row=4, column=1, sticky='we')
bcv_parallel_btn.grid(row=5, column=1, padx=3, pady=2, sticky='nwse')
scrap_price_btn.grid(row= 6, column=1, padx=3, pady=2, sticky='nwse')
version_label.grid(row=9, column=1)


# Execute windows
window.mainloop()
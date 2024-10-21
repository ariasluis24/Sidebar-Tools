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


locale.setlocale(locale.LC_ALL, 'es_VE')

igtf_calc_path = "C:\\Users\\l.arias\\Documents\\DOCUMENTOS CAJA LUIS ARIAS\\Nueva carpeta\\Python\\Nueva carpeta\\IGTF-Calc\\GUI.py"
explorer_exe_path = "C:\\Windows\\explorer.exe"
scanner_path = "C:\\Program Files (x86)\\epson\\Epson Scan 2\\Core\\es2launcher.exe"
web_browser_path = 'C:\\Program Files (x86)\\Microsoft\\Edge\\Application\\msedge.exe'
calculator_path = 'C:\\Windows\\System32\\calc.exe'
network_Test_path = "C:\\Windows\\System32\\cmd.exe"
profit_path = 'P:\\Profit_a\\profit_a.exe'



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

    price_window = Toplevel(window)
    price_window.title('Parallel Price')
    price_window.geometry('180x415+850+70')
    price_window.iconbitmap('icon.ico')
    
    result = scraping_Parallel()
    
    # Unir los elementos de la lista en un solo string con saltos de línea
    texto_lista = ''.join([f"{emoji}: {valor}\n" for emoji, valor in result if len(valor) <=15])
    price_title = Label(price_window, text='Parallel Price', font=('Arial', 12, 'bold'))
    
    scrap_price_label = Label(price_window, text=texto_lista, font=('Arial', 12), borderwidth=1, relief='groove')
   
    price_title.grid(row=0, column=0, columnspan=1,sticky='we')
    
    scrap_price_label.grid(row=1, column=0, padx=8,sticky='nswe')

def delete_operation(amount, label, label2, label3, label4):
    amount.delete(0, 'end')
    label.config(text='Price BCV:')
    label2.config(text='Price Parallel:')
    label3.config(text='')
    label4.config(text='')

# To make the scraping of the BCV Price concurrent and avoid freezes on the main thread of the GUI.

def handle_scraping_result_BCV(future):
    global result_BCV_future
    result_BCV_future = future.result()
    bcv_price.config(text=f'BCV: {result_BCV_future} Bs')
    
def handle_scraping_result_Parallel(future):
    global result_Parallel_future
    result_Parallel_future = future.result()
    parallel_price.config(text=f'Parallel: {result_Parallel_future} Bs')

def star_scraping():
    open_BCV_Calculator()
    
    future = executor.submit(scraping_BCV)
    future2 = executor.submit(scraping_Parallel_Calculator)

    future.add_done_callback(handle_scraping_result_BCV)
    future2.add_done_callback(handle_scraping_result_Parallel)

def open_BCV_Calculator(): 
    
    global BCV_window, bcv_price, parallel_price
    
    BCV_window = Toplevel(window)
    BCV_window.title('BCV Price')
    BCV_window.geometry('420x200+650+70')
    BCV_window.iconbitmap('icon.ico')

    BCV_window.columnconfigure(1, weight=1)
    
    #Labels, Entry, Buttons
    sub_total_entry = Entry(BCV_window, font=('Arial', 14), width=14, bg='yellow', justify='center')
    dollar_button = Button(BCV_window, text='$', font=('Roboto', 8,'bold'), width=2, height=1)
    
    calculate_button = Button(BCV_window, text='Calculate', command=lambda: calculation_BCV_Parallel(sub_total_entry.get()), width=10 )
    delete_button = Button(BCV_window, text='Delete', command=lambda: delete_operation(sub_total_entry, result_operation_BCV, result_operation_Parallel, differences_between_label, differences_percentage_label), width=8)
    
    bcv_price = Label(BCV_window, text=f'BCV: Loading...', font=('Arial', 10), justify='right', height=4)
    parallel_price = Label(BCV_window, text=f'$ Parallel: Loading...', font=('Arial', 10), justify='right', height=4)
    
    result_operation_BCV = Label(BCV_window, text=f'Price BCV:', font=('Arial', 10), justify='right')
    result_operation_Parallel = Label(BCV_window, text=f'Price Parallel:', font=('Arial', 10), justify='right')

    differences_between_label = Label(BCV_window, font=('Arial', 10), justify='center')
    differences_percentage_label = Label(BCV_window, font=('Arial', 10), justify='right')
    
    # Position
    # Column 0
    sub_total_entry.grid(row=1, column=0, pady=5, padx=5, sticky='ns')
    dollar_button.grid(row=1, column=0, pady=8, padx=7, sticky='ne')

    delete_button.grid(row=2, column=0, padx=5, sticky='es')
    calculate_button.grid(row=2, column=0, padx=5, sticky='ws')
    
    bcv_price.grid(row=3, column=0, sticky='NS')
    parallel_price.grid(row=4, column=0, sticky='NS')
    
    # Column 1
    result_operation_BCV.grid(row=1, column=1)
    result_operation_Parallel.grid(row=2, column=1)
    differences_between_label.grid(row=3, column=1, pady=15)
    differences_percentage_label.grid(row=4, column=1)
    
    def calculation_BCV_Parallel(amount):
        try:    
            amount_float = float(amount)
            result_calculation_BCV = round(Decimal(amount_float * result_BCV_future),2)
            result_calculation_Parallel = round(Decimal(amount_float * float(result_Parallel_future)),2)
            difference_between_prices = round(Decimal(result_calculation_Parallel - result_calculation_BCV),2)

            difference_percentage = round(Decimal(((result_calculation_Parallel - result_calculation_BCV)/result_calculation_BCV)*100),2)
            
            difference_between_prices_to_BCV = round(Decimal(difference_between_prices / Decimal(result_Parallel_future)),2)
            difference_between_prices_to_Parallel = round(Decimal(difference_between_prices / Decimal(result_BCV_future)),2)
            
            
            result_operation_BCV.config(text=f'Price BCV: {result_calculation_BCV:n} Bs')    
            result_operation_Parallel.config(text=f'Price Parallel: {result_calculation_Parallel:n} Bs')    
            
            differences_between_label.config(text=f'Gap: {difference_between_prices:n} Bs \nBCV:({difference_between_prices_to_BCV:n}$) Parallel:({difference_between_prices_to_Parallel:n}$) ')    
            differences_percentage_label.config(text=f'Difference %: {difference_percentage:n}%')    
            
            
            result_operation_BCV.grid(row=1, column=1)
            result_operation_Parallel.grid(row=2, column=1)
            differences_between_label.grid(row=3, column=1)

        except ValueError:
            result_operation_BCV.config(text=f'Price BCV: Error en Valor Introducido')    
            result_operation_Parallel.config(text=f'Price Parallel: Error en Valor Introducido')    
            result_operation_BCV.grid(row=1, column=1)
            result_operation_Parallel.grid(row=2, column=1)
        
        except NameError:
            result_operation_BCV.config(text=f'Price BCV: Error obteniendo precio')    
            result_operation_Parallel.config(text=f'Price Parallel: Error obteniendo precio')    
            result_operation_BCV.grid(row=1, column=1)
            result_operation_Parallel.grid(row=2, column=1)


    #// TODO make the calculator of an amount with both prices BCV & Parallel
    

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
profit_btn = Button(window, text='Profit', font=('Arial', 10), width=12, height=1, justify='center', command= lambda: open_Tool(profit_path))
scanner_btn = Button(window, text='Scanner', font=('Arial', 10), width=12, height=1, justify='center',  command= lambda: open_Tool(scanner_path))
explorer_btn = Button(window, text='File Explorer', font=('Arial', 10), width=12, height=1, justify='center',  command= lambda: open_Tool(explorer_exe_path))
date_label = Label(window, text=date_actual, font=('Arial', 10,'bold'))
version_label = Label(window, text='Version: Beta 1.0', font=('Arial', 7))


server_status = Label(window, text='', font=('Arial', 10), bg='green', fg='white')
server_ping = Label(window, text='', font=('Arial', 8))
internet_status = Label(window, text='', font=('Arial', 10), height=1, bg='green', fg='white')
internet_ping = Label(window, text='', font=('Arial', 8))
bcv_parallel_btn = Button(window, text='BCV Calculator', font=('Arial', 10), width=5, height=1, justify='center',  command= star_scraping)
scrap_price_btn = Button(window, text='Get Parallel Price', font=('Arial', 10), width=13, height=1, justify='center', command=open_Pararel_Price_Window)

# // TODO Make this function infinitely run in the background.     
def ping_Server():

    local_server_ip = 'server' #Special local_server_ip used from the local server.
    
    def ping_and_update():
        response_server = ping(local_server_ip, unit='ms')
        try:
            if type(response_server) == float:
                
                rounded_response = round(response_server, 2)
                
                if response_server > 0 or response_server == 0.0:
                    # window.after(0, lambda: update_status('Server Connected', f'Ping: {rounded_response} ms', 'green', 'white'))
                    update_status(server_status, server_ping, 'Server Connected', f'Ping: {rounded_response} ms', 'green', 'white')
                    profit_btn.config(state='normal')    
                    
                    print(f"Reached {local_server_ip} {response_server}")
                    
            elif type(response_server) == False:
                # window.after(0, lambda: update_status('Host Unknown', '-', 'red', 'yellow'))

                update_status(server_status, server_ping, 'Host Unknown', '-', 'red', 'white')
                profit_btn.config(state=DISABLED)    
                print(f"Host Unknown {local_server_ip}")

            elif type(response_server) == None:
                
                update_status(server_status, server_ping, 'Timed Out', '-', 'red', 'white')
                profit_btn.config(state=DISABLED)  
                print(f"Timed Out {local_server_ip}")
                # window.after(2000, ping_Server)
            
            else:
                update_status(server_status, server_ping, 'Check Ethernet', '-', 'red', 'white')
                profit_btn.config(state=DISABLED)  
                print('Check Ethernet')
        
        except TimeoutError as e:
            print(f"Timeout error occurred: {e}")
        
        except OSError as e:
            print(f"OS error occurred: {e}")
        
        except Exception as e:
            print(f"An unexpected error occurred: {e}")   
    
    threading.Thread(target=ping_and_update, daemon=True).start()
    # os.system('cls')
    window.after(1000, ping_Server)

def ping_Internet():

    internet_ip= '8.8.8.8' # Ip used to do ping and check internet connection.
    
    def internet_ping_and_update():

        response_internet = ping(internet_ip, unit='ms')
        
        try:
            if type(response_internet) == float:

                rounded_response = round(response_internet, 2)
                
                if response_internet > 0 or response_internet == 0.0 and response_internet is not False:
                    # window.after(0, lambda: update_status('Server Connected', f'Ping: {rounded_response} ms', 'green', 'white'))
                    
                    update_status(internet_status, internet_ping, 'Internet Connected', f'Ping: {rounded_response} ms', 'green', 'white')
                    
                    print(f"Reached {internet_ip} {response_internet}")

            elif response_internet == False:
                # window.after(0, lambda: update_status('Host Unknown', '-', 'red', 'yellow'))

                update_status(internet_status, internet_ping, 'Host Unknown', '-', 'red', 'white')
                    
                print(f"Host Unknown {internet_ip}")

            elif response_internet == None:
                # server_status.config(text='Server Timed Out')
                    
                update_status(internet_status, internet_ping, 'Timed Out', '-', 'red', 'white')
                    
                print(f"Timed Out {internet_ip}")
                
                # window.after(2000, ping_Server)
            
            else:
                update_status(internet_status, internet_ping, 'Check Ethernet', '-', 'red', 'white')

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

def update_status(label_text, label_ping, status_text, ping_text='', bg_color='', fg_color=''):
    
    label_text.config(text=status_text, bg=bg_color, fg=fg_color)
    
    if ping_text:
        label_ping.config(text=ping_text)

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
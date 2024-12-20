from tkinter import *
from tkinter import messagebox
from scrap_price_Parallel import scraping_Parallel, scraping_Parallel_Calculator, scraping_Parallel_Photo
from scrap_price_BCV import scraping_BCV
from ping3 import ping
from decimal import Decimal 
from concurrent.futures import ThreadPoolExecutor
from PIL import ImageTk, Image
import datetime
import subprocess
import locale
import threading
import time
import gc 
import pyautogui
import pygetwindow as gw


# * Functions to automate most of the process of the programs open.
def start_User_Profit_EPS(window_title, text):
    
    width = 1366
    height = 210

    x = (width) // 2
    y = (height) // 2
    
    password = '0000'
    companies = ['NE', 'EPS2']

    pyautogui.FAILSAFE = True

    # Find the window with the specified title
    # Activate the first window with the matching title
    windows = gw.getWindowsWithTitle(window_title)
    if not windows:
        print("Window not found!")
    try:

        profit_window = windows[1]
        profit_window.activate()

    except IndexError:

        open_Tool(profit_path)


    # Wait a moment for the window to come to focus
    time.sleep(3)
    
    # Type the specified text
    pyautogui.PAUSE = 0.4
    pyautogui.write(text, 0.1)
    pyautogui.press('Enter')
    pyautogui.write(password, 0.1)
    pyautogui.press('Enter')
    
    time.sleep(8)
    
    pyautogui.PAUSE = 1.5
    pyautogui.write(companies[1], 0.1)
    
    pyautogui.PAUSE = 0.7
    pyautogui.press('Enter')
    pyautogui.press('Enter')
    pyautogui.press('Enter')
    

    pyautogui.PAUSE = 1.3
    pyautogui.press('down')
    pyautogui.press('Enter')
    pyautogui.press('Enter')

    pyautogui.write('EOL', 0.1)

    pyautogui.press('Enter')

    # Change window size
    time.sleep(4)

    pyautogui.moveTo(x, y)
    pyautogui.click(clicks=2, button='left')

    stop_auto_thread_event.set()

def start_User_Profit_NE(window_title, text):
        
    width = 1366
    height = 210

    x = (width) // 2
    y = (height) // 2
    
    password = '0000'
    companies = ['NE', 'EPS2']

    def auto_NE():
        
        pyautogui.FAILSAFE = True
        time.sleep(2)
        # Find the window with the specified title
        
        windows = gw.getWindowsWithTitle(window_title)
        
        if not windows:
            print("Window not found!")
            return
        
        # Activate the first window with the matching title
        profit_window = windows[0]
        profit_window.activate()

        # Wait a moment for the window to come to focus
        time.sleep(3)
        
        # Type the specified text
        pyautogui.PAUSE = 0.4
        pyautogui.write(text, 0.1)
        pyautogui.press('Enter')
        pyautogui.write(password, 0.1)
        pyautogui.press('Enter')
        
        time.sleep(8)
        
        pyautogui.PAUSE = 1.5
        pyautogui.write(companies[0], 0.1)

        pyautogui.PAUSE = 0.7
        pyautogui.press('Enter')
        pyautogui.press('Enter')
        pyautogui.press('Enter')
        

        pyautogui.PAUSE = 1.3
        pyautogui.press('down')
        pyautogui.press('Enter')
        pyautogui.PAUSE = 1.5
        pyautogui.press('Enter')
        
        pyautogui.PAUSE = 0.1
        pyautogui.press('esc')

        
        pyautogui.PAUSE = 1.3
        # Change window size
        time.sleep(3)
        pyautogui.moveTo(x, y)
        pyautogui.click(clicks=2, button='left')
        
        pyautogui.moveTo(1300, 10)
        pyautogui.click(clicks=1, button='left')

        # Note this drag only works when the program is open for the first time
        pyautogui.moveTo(640, 400)
        pyautogui.dragTo(1360, 400)


        time.sleep(2)

        start_User_Profit_EPS("Profit Plus Administrativo", "Luis Arias")


    auto_thread = threading.Thread(target=auto_NE, daemon=True)
    auto_thread.start()

def start_Scan_Bill():
        
    def auto_epson_scan():
        
        time.sleep(5)
        
        pyautogui.FAILSAFE = True
        
        windows = gw.getWindowsWithTitle('Epson Scan 2')
        if not windows:
            print("Window not found!")
            messagebox.showinfo(title=None, message=f'Epson Scan 2, no esta abierto!')
            
        # Activate the first window with the matching title
        profit_window = windows[0]
        profit_window.activate()

        #############################
        pyautogui.PAUSE = 0
        repeat_Tab(17)
        pyautogui.press('enter')
        
        time.sleep(10)
        repeat_Tab(6)
        pyautogui.press('enter')

        stop_auto_thread_event.set()

    auto_Scan = threading.Thread(target=auto_epson_scan, daemon=True)
    auto_Scan.start()

def start_Print_Report():
    # TODO: Use check marks to decide which report is going to be printed.
    
    windows = gw.getWindowsWithTitle('Facturas de Venta - Profit Plus Administrativo ( Ventas y Cuentas x Cobrar ) Usuario: Luis Arias Empresa: COMPUGATE CENTER VALENCIA,CA Suc: NOTA DE ENTREGA')
    windows_2 = gw.getWindowsWithTitle('Cobros a Clientes - Profit Plus Administrativo ( Ventas y Cuentas x Cobrar ) Usuario: Luis Arias Empresa: COMPUGATE CENTER VALENCIA,CA Suc: NOTA DE ENTREGA')
    pyautogui.FAILSAFE = True
    
    def auto_Print_Report():
        condition_Tabs = 5
        # This condition check on what module the Profit Window and activates the one being used.
        # Activate the first window with the matching title
        if not windows:
            # Facturas de Venta
            profit_window = windows_2[0]
            profit_window.activate()
        
        else:
            # Cobros a Clientes
            profit_window = windows[0]
            profit_window.activate()
            
        # Wait a moment for the window to come to focus
        time.sleep(2)
        pyautogui.PAUSE = 0.7

        pyautogui.press('alt')
        pyautogui.press('r')


        pyautogui.PAUSE = 1
        pyautogui.press('b')

        time.sleep(1)
        try:
            # This Try and except code verify if on the print report window there is a button that changes how many times the tab needs to be pressed.
            printers = pyautogui.locateCenterOnScreen('src/printers.png')
            condition_Tabs = 6
        except pyautogui.ImageNotFoundException:
            pass


        time.sleep(2)
        ###########################################
        # EPS2

        pyautogui.PAUSE = 1

        pyautogui.press('num1')

        pyautogui.press('tab')

        pyautogui.PAUSE = 1

        pyautogui.press('e')
        pyautogui.press('e')
        pyautogui.press('down')

        pyautogui.PAUSE = 0.01

        repeat_Tab(condition_Tabs)
        
        pyautogui.write(date_For_Automation, interval=0.03)

        repeat_Tab(28)

        pyautogui.PAUSE = 0.4
        pyautogui.press('i')
        pyautogui.press('tab')    
        
        pyautogui.press('enter') # ! Critical step, starts the printer


        # Here would be the function to detect the window error of there is not info to print.
        time.sleep(1)
        try:
            no_info = pyautogui.locateCenterOnScreen('src/no_info_2.png')
            pyautogui.moveTo((no_info[0] + 160 ), (no_info[1] + 55), 0.02)
            pyautogui.leftClick() # ! If there is no info to print accepts the alert window
        
        except pyautogui.ImageNotFoundException:
            pass

        ##########################################
        # NE
        pyautogui.PAUSE = 0
        repeat_Tab(5)

        pyautogui.PAUSE = 1

        pyautogui.press('num2')
        
        pyautogui.press('tab')
        pyautogui.press('n')

        pyautogui.PAUSE = 0.01

        repeat_Tab(condition_Tabs)

        pyautogui.write(date_For_Automation, interval=0.03)

        repeat_Tab(28)

        pyautogui.PAUSE = 0.4
        pyautogui.press('i')
        pyautogui.press('tab')
        pyautogui.press('enter') # ! Critical step, starts the printer
        pyautogui.press('esc')

        stop_auto_print_report_thread_event.set()

    auto_Print = threading.Thread(target=auto_Print_Report, daemon=True)
    auto_Print.start()

def repeat_Tab(times):

    for x in range(times):
        pyautogui.press('tab')

locale.setlocale(locale.LC_ALL, 'es_VE')

# Variables to use.
igtf_calc_path = "src\\GUI.exe"
explorer_exe_path = "C:\\Windows\\explorer.exe"
scanner_path = "C:\\Program Files (x86)\\epson\\Epson Scan 2\\Core\\es2launcher.exe"
web_browser_path = 'C:\\Program Files (x86)\\Microsoft\\Edge\\Application\\msedge.exe'
calculator_path = 'C:\\Windows\\System32\\calc.exe'
network_Test_path = "C:\\Windows\\System32\\cmd.exe"
profit_path = 'P:\\Profit_a\\profit_a.exe'
local_server_ip = 'server'  # Local server IP or domain.
internet_ip = 'www.youtube.com'  # Ip used to do ping and check internet connection.
hide_event = threading.Event()
stop_auto_thread_event = threading.Event()
stop_auto_scan_thread_event = threading.Event()
stop_auto_print_report_thread_event = threading.Event()
stop_auto_open_parallel_window_thread_event = threading.Event()
ping_thread = None
ping_thread_two = None
version = 'Beta 2.0'
now = datetime.datetime.now()
date_actual = now.strftime('%a %d/%b/%y')
date_For_Automation = now.strftime('%d%m20%y')
name_file = f'src\\logs\\log-{date_For_Automation}.txt'
network_response = ['Server Connected', 'Internet Connected', 'Host Unknown',  'Timed Out', 'Check Internet', 'Check Ethernet']

def saving_logs(server, ping, network_response):
    update_Log_Time = datetime.datetime.now()
    date_For_Logs = update_Log_Time.strftime('%d/%m/%Y %I:%M:%S')
    # date_For_Logs = update_Log_Time.strftime('%T')
    with open(name_file, 'a') as file:
        # Write method to write file in an external txt file.
        # Put a if statement when the ping returned is a blank space.
        file.write(f'[{server}] Time:[{date_For_Logs}] - Ping:[{ping} - {network_response}]\n')

# TODO Change the state of the button if the program is already open.

def open_Tool(tool_path):
    subprocess.Popen(tool_path)

def open_Parallel_Price_Window():

    def auto_Parallel():
        # TODO: Redo this whole window into a Class window.
        # TODO Displayed Internet Error if the Internet connection failed when it tried the scrap.
        # TODO: Make a refresh button.
        # TODO: Make a combobox with the different dates and links obtained from the scrap.
        # TODO: Make a little scrap on the background every now and then, check time and price, if the script detects new content display a button to updated image and values.
        
        price_window = Toplevel(window)
        price_window.title('Parallel Price')
        # TODO: Make the window one size or another if the more that 4 set of results.
        price_window.geometry('600x515+450+70')
        price_window.iconbitmap('icon.ico')
        
        scraping_Parallel_Photo()
        result = scraping_Parallel()
        
        if isinstance(result, list) == True:
            texto_lista = None
            # Joins all the elements from a list, into a single string with jump spaces.
            texto_lista = ''.join([f"{emoji}: {valor}\n" for emoji, valor in result if len(valor) <=15])
        
        elif isinstance(result, str) == True:
            # 
            texto_lista = result
        
        else:
            texto_lista = 'An unexpected error occurred.'
        
        img = ImageTk.PhotoImage(Image.open('src\\Parallel\\downloaded_image.jpg').resize((345,345)))
        price_title = Label(price_window, text='Parallel Price', font=('Arial', 12, 'bold'))
        scrap_price_label = Label(price_window, text=texto_lista, font=('Arial', 12), width=25, borderwidth=1, relief='groove')
        price_photo_label = Label(price_window, image=img)
        price_photo_label.image = img

        # Position of Widgets
        price_title.grid(row=0, column=0, sticky='we', columnspan=2)
        scrap_price_label.grid(row=1, column=0, padx=8,sticky='we')
        
        price_photo_label.grid(row=0, column=1, rowspan=2)

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
        stop_auto_print_report_thread_event.set()

    scraping_Parallel_Window = threading.Thread(target=auto_Parallel, daemon=True)
    scraping_Parallel_Window.start()

def delete_operation(amount, label, label2, label3, label4):
    amount.delete(0, 'end')
    label.config(text='Price BCV:')
    label2.config(text='Price Parallel:')
    label3.config(text='')
    label4.config(text='')

def open_about_me():
    messagebox.showinfo(title=None, message=f'Sidebar Tools {version}\nMade by Luis Arias\n2024 ©')

# To make the scraping of the BCV Price concurrent and avoid freezes on the main thread of the GUI.
class BCVCalculator:
    def __init__(self, master, executor):
        self.master = master
        self.executor = executor

        self.BCV_window = Toplevel(master)
        self.BCV_window.title('BCV Price')
        self.BCV_window.geometry('420x150+650+270')
        self.BCV_window.iconbitmap('icon.ico')
        self.BCV_window.columnconfigure(1, weight=1)

        self.converted = False
        self.currency = 'Dollars'
        self.add_Text_Result_Shown = False

        self.create_widgets()
        self.BCV_window.protocol("WM_DELETE_WINDOW", self.on_closing_toplevel)
        self.shown_scraping()

    def create_widgets(self):
        # Labels, Entry, Buttons
        self.sub_total_entry = Entry(self.BCV_window, font=('Arial', 14), width=14, bg='yellow', justify='center')
        self.convert_currency_button = Button(self.BCV_window, text='$', font=('Roboto', 8, 'bold'), command=self.convert_value, width=2, height=1)
        self.calculate_button = Button(self.BCV_window, text='Calculate', command=self.calculation_BCV_Parallel, width=10)
        self.delete_button = Button(self.BCV_window, text='Delete', command=self.delete_operation, width=8)
        self.refresh_button = Button(self.BCV_window, text='Refresh', command=self.refresh, width=6)

        self.bcv_price_label = Label(self.BCV_window, text=f'BCV: Loading...', font=('Arial', 10), justify='center')
        self.parallel_price_label = Label(self.BCV_window, text=f'$ Parallel: Loading...', font=('Arial', 10), justify='center')
        
        self.bcv_price = Text(self.BCV_window, height=1, width=14, borderwidth=0, highlightthickness=0, bg='#f1f1f0')
        self.parallel_price = Text(self.BCV_window, height=1, width=16, borderwidth=0, highlightthickness=0, bg='#f1f1f0')

        self.result_operation_BCV_Text = Text(self.BCV_window, height=1, width=30, borderwidth=0, highlightthickness=0, bg='#f1f1f0')
        self.result_operation_Parallel_Text = Text(self.BCV_window, height=1, width=30, borderwidth=0, highlightthickness=0, bg='#f1f1f0')
        self.differences_between_Text = Text(self.BCV_window, height=1, width=30, borderwidth=0, highlightthickness=0, bg='#f1f1f0')
        self.differences_percentage_Text = Text(self.BCV_window, height=1, width=30, borderwidth=0, highlightthickness=0, bg='#f1f1f0')

        # Position
        # Column 0
        self.sub_total_entry.grid(row=1, column=0, pady=5, padx=5, sticky='ns')
        self.convert_currency_button.grid(row=1, column=0, pady=8, padx=7, sticky='ne')
        self.delete_button.grid(row=2, column=0, padx=5, sticky='es')
        self.calculate_button.grid(row=2, column=0, padx=5, sticky='ws')
        self.bcv_price_label.grid(row=3, column=0)
        self.parallel_price_label.grid(row=4, column=0)

        # Column 1
        self.result_operation_BCV_Text.grid(row=1, column=1)
        self.result_operation_Parallel_Text.grid(row=2, column=1)
        
        self.BCV_window.rowconfigure(3, minsize=50)
        self.differences_between_Text.grid(row=3, column=1)
        self.differences_percentage_Text.grid(row=4, column=1)

        self.refresh_button.grid(row=4, column=1, padx=3, sticky='e')
        self.refresh_button.lift()

    def shown_scraping(self):
        
        future_BCV = self.executor.submit(scraping_BCV)
        future_Parallel = self.executor.submit(scraping_Parallel_Calculator)

        future_BCV.add_done_callback(lambda future: self.handle_scraping_result_BCV(future))
        future_Parallel.add_done_callback(lambda future: self.handle_scraping_result_Parallel(future))

    def handle_scraping_result_BCV(self, future):
        
        result_BCV = future.result()
        self.result_BCV_future = float(result_BCV)     
        
        self.bcv_price_label.grid_forget()
        
        # Create a Text widget
        
        self.bcv_price.insert("1.0", "BCV: ", 'initial')  # Insert the static text
        self.bcv_price.insert("2.0", f"{self.result_BCV_future:n} Bs", "bold")  # Insert the result with a tag

        self.bcv_price.tag_configure('initial', font=('Arial', 10), justify='center')
        self.bcv_price.tag_configure("bold", font=("Arial", 10, "bold"), justify='center')  # Configure the bold tag
        self.bcv_price.configure(state="disabled")
        
        self.bcv_price.grid(row=3, column=0)    

    def handle_scraping_result_Parallel(self, future):
        
        result_Parallel = future.result()
        self.result_Parallel_future = float(result_Parallel)

        self.parallel_price_label.grid_forget()

        # Create a Text widget
        
        self.parallel_price.insert("1.0", "$ Parallel: ", 'initial_parallel')  # Insert the static text
        self.parallel_price.insert("end", f"{self.result_Parallel_future:n} Bs", "bold_parallel")  # Insert the result with a tag
        self.parallel_price.tag_configure('initial_parallel', font=('Arial', 10), justify='center')
        self.parallel_price.tag_configure("bold_parallel", font=("Arial", 10, "bold"), justify='center')  # Configure the bold tag
        self.parallel_price.configure(state="disabled")

        self.parallel_price.grid(row=4, column=0)    

    def calculation_BCV_Parallel(self):
        amount = self.sub_total_entry.get()

        def add_Result_Text(Text_widget:Text, result_Description:str, result_operation):

            Text_widget.configure(state='normal')    
            Text_widget.delete('1.0', END)
            Text_widget.insert('1.0', f'{result_Description} ', 'initial')

            if self.converted == False:
            
                if Text_widget == self.differences_percentage_Text:

                    Text_widget.insert('2.0', f'{result_operation:n} %', 'last')
            
                else:
                    Text_widget.insert('2.0', f'{result_operation:n} Bs', 'last')
            
            if self.converted == True:
            
                if Text_widget == self.differences_percentage_Text:

                    Text_widget.insert('2.0', f'{result_operation:n} %', 'last')
            
                else:
                    Text_widget.insert('2.0', f'{result_operation:n} $', 'last')

            Text_widget.tag_configure('initial', font=('Arial', 10), justify='center')
            Text_widget.tag_configure('last', font=('Arial', 10, 'bold'),justify='center')

            Text_widget.configure(state='disabled')
        
        def add_Error_Text(Text_widget_one:Text, Text_widget_two:Text):
            
            Text_widget_one.configure(state='normal')    
            Text_widget_two.configure(state='normal')    
            Text_widget_one.delete('1.0', END)
            Text_widget_two.delete('1.0', END)

            Text_widget_one.insert('1.0', 'Price BCV: Error en Valor Introducido', 'initial')
            Text_widget_two.insert('1.0', 'Price Parallel: Error en Valor Introducido', 'initial')


            Text_widget_one.tag_configure('initial', font=('Arial', 8, 'bold'), justify='center')
            Text_widget_two.tag_configure('initial', font=('Arial', 8, 'bold'), justify='center')

            Text_widget_one.configure(state='disabled')
            Text_widget_two.configure(state='disabled')

        try:

            if self.converted == False:
                amount_float = float(amount)
                result_calculation_BCV = round(Decimal(amount_float * self.result_BCV_future), 2)
                result_calculation_Parallel = round(Decimal(amount_float * float(self.result_Parallel_future)), 2)
                difference_between_prices = round(Decimal(result_calculation_Parallel - result_calculation_BCV), 2)
                difference_percentage = round(Decimal(((result_calculation_Parallel - result_calculation_BCV) / result_calculation_BCV) * 100), 2)
                
                self.add_Text_Result_Shown = True
                
                add_Result_Text(self.result_operation_BCV_Text, 'Price BCV:', result_calculation_BCV)
                add_Result_Text(self.result_operation_Parallel_Text, 'Price Parallel:', result_calculation_Parallel)
                add_Result_Text(self.differences_between_Text, 'Gap:', difference_between_prices)
                add_Result_Text(self.differences_percentage_Text, 'Difference:', difference_percentage)
            
            elif self.converted == True:
                amount_float = float(amount)
                result_calculation_BCV = round(Decimal(amount_float / self.result_BCV_future ), 2)
                result_calculation_Parallel = round(Decimal(amount_float / float(self.result_Parallel_future)), 2)
                difference_between_prices = round(Decimal(result_calculation_BCV - result_calculation_Parallel), 2)
                difference_percentage = round(Decimal(((result_calculation_BCV - result_calculation_Parallel) / result_calculation_BCV) * 100), 2)

                self.add_Text_Result_Shown = True

                add_Result_Text(self.result_operation_BCV_Text, 'Price BCV:', result_calculation_BCV)
                add_Result_Text(self.result_operation_Parallel_Text, 'Price Parallel:', result_calculation_Parallel)
                add_Result_Text(self.differences_between_Text, 'Gap:', difference_between_prices)
                add_Result_Text(self.differences_percentage_Text, 'Difference:', difference_percentage)
        
        except ValueError:

            add_Error_Text(self.result_operation_BCV_Text, self.result_operation_Parallel_Text)

        except AttributeError:

            messagebox.showinfo(title=None, message=f'Precios aun no actualizados!')

    def delete_operation(self):

        self.sub_total_entry.delete(0, 'end')
        # Change the state of the Text widget to accept changes.
        self.result_operation_BCV_Text.configure(state='normal')
        self.result_operation_Parallel_Text.configure(state='normal')
        self.differences_between_Text.configure(state='normal')
        self.differences_percentage_Text.configure(state='normal')
        
        self.result_operation_BCV_Text.delete('1.0', END)
        self.result_operation_Parallel_Text.delete('1.0', END)
        self.differences_between_Text.delete('1.0', END)
        self.differences_percentage_Text.delete('1.0', END)

    def on_closing_toplevel(self):
       
        self.BCV_window.destroy()
        gc.collect()

    def convert_value(self):

        def add_Result_Text(Text_widget:Text, result_Description:str, result_operation):

            Text_widget.configure(state='normal')    
            Text_widget.delete('1.0', END)
            Text_widget.insert('1.0', f'{result_Description} ', 'initial')

            if self.converted == False:
            
                if Text_widget == self.differences_percentage_Text:

                    Text_widget.insert('2.0', f'{result_operation:n} %', 'last')
            
                else:
                    Text_widget.insert('2.0', f'{result_operation:n} Bs', 'last')
            
            if self.converted == True:
            
                if Text_widget == self.differences_percentage_Text:

                    Text_widget.insert('2.0', f'{result_operation:n} %', 'last')
            
                else:
                    Text_widget.insert('2.0', f'{result_operation:n} $', 'last')

            Text_widget.tag_configure('initial', font=('Arial', 10), justify='center')
            Text_widget.tag_configure('last', font=('Arial', 10, 'bold'),justify='center')

            Text_widget.configure(state='disabled')

        if self.convert_currency_button.cget('text') == '$':
            print(self.convert_currency_button.cget('text'))
            self.converted = True
        
        elif self.convert_currency_button.cget('text') == 'Bs':
            print(self.convert_currency_button.cget('text'))
            self.converted = False

        value = float(self.sub_total_entry.get())

        if self.currency == 'Dollars':
            result_To_Bolivars = round(value * self.result_Parallel_future, 2)
            self.currency = 'Bolivars'

            self.convert_currency_button.config(text='Bs')
            
            self.sub_total_entry.delete(0, 'end')
            self.sub_total_entry.insert(0, result_To_Bolivars)


        elif self.currency == 'Bolivars':
            result_To_Dollars = round(value / self.result_Parallel_future, 2)
            self.currency = 'Dollars'

            result_calculation_BCV = round(Decimal(value / self.result_BCV_future ), 2)
            result_calculation_Parallel = round(Decimal(value / float(self.result_Parallel_future)), 2)
            difference_between_prices = round(Decimal(result_calculation_BCV - result_calculation_Parallel), 2)
            difference_percentage = round(Decimal(((result_calculation_BCV - result_calculation_Parallel) / result_calculation_BCV) * 100), 2)

            self.convert_currency_button.config(text='$')
            
            self.sub_total_entry.delete(0, 'end')
            self.sub_total_entry.insert(0, result_To_Dollars)

            if self.add_Text_Result_Shown == False:
                add_Result_Text(self.result_operation_BCV_Text, 'Price BCV:', result_calculation_BCV)
                add_Result_Text(self.result_operation_Parallel_Text, 'Price Parallel:', result_calculation_Parallel)
                add_Result_Text(self.differences_between_Text, 'Gap:', difference_between_prices)
                add_Result_Text(self.differences_percentage_Text, 'Difference:', difference_percentage)
                pass

            elif self.add_Text_Result_Shown == True:
                pass

    
    def refresh(self):
        
        #TODO: Fix no complete refresh, when a new value is posted on the telegram chat, it does not scrap the new value and works with the previous one when the window is opened.
        self.converted = False
        self.currency = 'Dollars'

        self.convert_currency_button.config(text='$')

        self.delete_operation()
        self.bcv_price.grid_forget()
        self.bcv_price_label.grid(row=3, column=0)
        
        self.parallel_price.grid_forget()
        self.parallel_price_label.grid(row=4, column=0)
        self.shown_scraping()

class AutoWindow:

    # TODO: Investigate what other task can be automated.
    def __init__(self, master, executor):
        
        self.master = master
        self.executor = executor

        self.Auto_window = Toplevel(master)
        self.Auto_window.title('Autowork')
        self.Auto_window.geometry('200x200+650+70')
        self.Auto_window.iconbitmap('icon.ico')
        self.Auto_window.columnconfigure(1, weight=1)

        self.create_widgets()
        self.Auto_window.protocol("WM_DELETE_WINDOW", self.on_closing_toplevel)

    def create_widgets(self):
        
        self.print_reports_btn = Button(self.Auto_window, text='Print Reports', font=('Roboto', 8, 'bold'), width=10, height=1, command=start_Print_Report)
        self.print_NE = Button(self.Auto_window, text='Print NE', font=('Roboto', 8, 'bold'), width=10, height=1)

        # Position
        self.Auto_window.rowconfigure(0, minsize=20)
        self.Auto_window.columnconfigure(0, minsize=5)
        self.Auto_window.rowconfigure(1, minsize=50)
        self.Auto_window.columnconfigure(1, minsize=50)
        
        self.print_reports_btn.grid(row=0, column=0, padx=2, pady=2)
        self.print_NE.grid(row=1, column=0, padx=2, pady=2)

    def on_closing_toplevel(self):
        
        self.Auto_window.destroy()
        gc.collect()
   
executor = ThreadPoolExecutor(max_workers=4)

# Windows entity  

window = Tk()

# Config of window
window.title('Sidebar Tools')
window.geometry('340x80+100+648') # Default size of the window & Position.
window.attributes('-topmost',True) # Makes the window always on top.
window.iconbitmap('icon.ico')
window.config(bg='#121212') # Change the background color of the main window.
window.overrideredirect(True) # Takes out the title window

# window.minsize(800, 370) # Minimun size of the window
# window.maxsize(800, 370) # Maximun size of the window
    
#Images for the buttons.
IGTF_icon = PhotoImage(file='src\\IGTF30.png')
calculator_icon = PhotoImage(file='src\\calculator30.png')
web_browser_icon = PhotoImage(file='src\\web30.png')
profit_icon = PhotoImage(file='src\\profit30.png')
scanner_icon = PhotoImage(file='src\\scanner30.png')
explorer_icon = PhotoImage(file='src\\file_explorer30.png')
bcv_icon = PhotoImage(file='src\\BCV30.png')
parallel_icon = PhotoImage(file='src\\parallel30.png')
script_icon = PhotoImage(file='src\\script30.png')

# Creating Labels

close_btn = Button(window, text='Close', font=('Arial', 7), bg='#121212', fg='white', command=window.destroy)

igtf_btn = Button(window, image=IGTF_icon, font=('Arial', 8), width=30, height=27, justify='center', bg='#121212', command= lambda: open_Tool(igtf_calc_path))
calculator_btn = Button(window, image=calculator_icon, font=('Arial', 8), width=25, height=27, justify='center', bg='#121212', command= lambda: open_Tool(calculator_path))
web_browser_btn = Button(window, image=web_browser_icon, font=('Arial', 8), width=30, height=27, justify='center', bg='#121212', command= lambda: open_Tool(web_browser_path))
profit_btn = Button(window, image=profit_icon, font=('Arial', 8), width=30, height=27, justify='center', bg='#121212', command= lambda: (open_Tool(profit_path), open_Tool(profit_path), start_User_Profit_NE("Profit Plus Administrativo", "Luis Arias")))
scanner_btn = Button(window, image=scanner_icon, font=('Arial', 8), width=25, height=27, justify='center', bg='#121212', command= lambda: (open_Tool(scanner_path), start_Scan_Bill()))
explorer_btn = Button(window, image=explorer_icon, font=('Arial', 8), width=25, height=27, justify='center', bg='#121212', fg='white', command= lambda: open_Tool(explorer_exe_path))
bcv_parallel_calc_btn = Button(window, image=bcv_icon, font=('Arial', 8), width=30, height=27, justify='center', command=lambda: BCVCalculator(window, executor))
parallel_price_btn = Button(window, image=parallel_icon, font=('Arial', 8), width=30, height=27, justify='center', bg='#121212', command=open_Parallel_Price_Window)
script_btn = Button(window, image=script_icon, font=('Arial', 8), width=30, height=27, justify='center', fg='white', bg='#121212', command=lambda: AutoWindow(window, executor))


date_label = Label(window, text=date_actual, font=('Arial', 8,'bold'), bg='#121212', fg='white')
version_label = Button(window, text=f'Version: {version}', font=('Arial', 7), width=12, bg='#121212', fg='white', relief=FLAT, justify='center', command=open_about_me)


server_status = Label(window, text='', font=('Arial', 7), width=15, height=1, bg='green', fg='white')
server_ping = Label(window, text='', font=('Arial', 7), bg='#121212', fg='white')
internet_status = Label(window, text='', font=('Arial', 7), width=15, height=1, bg='green', fg='white')
internet_ping = Label(window, text='', font=('Arial', 7), bg='#121212', fg='white')


def ping_Server():
    global ping_thread
    def ping_and_update():
        while not hide_event.is_set():
            response_server = ping(local_server_ip, unit='ms')
            
            try:
                rounded_response = round(response_server, 2) if isinstance(response_server, float) else None

                # Condition when the server responds correctly for the first time or the connection comes back.
                if isinstance(response_server, float) and server_status.cget('text') in ['', 'Host Unknown', 'Check Internet', 'Time Out', 'Check Ethernet']:
                    server_status.config(text=network_response[0], fg='white', bg='green')
                    update_status(server_ping, f'Ping: {rounded_response} ms')
                    profit_btn.config(state='normal')
                    saving_logs('Server', rounded_response, network_response[10])

                # Condition when the server keeps responding
                elif isinstance(response_server, float) and server_status.cget('text') == 'Server Connected':
                    update_status(server_ping, f'Ping: {rounded_response} ms')
                    saving_logs('Server', rounded_response, network_response[0])
                    
                # Condition when the server doesn't respond (Disconnection)
                elif response_server is False:
                    server_status.config(text=network_response[2], fg='white', bg='red')
                    update_status(server_ping, '-')
                    profit_btn.config(state='disabled')
                    saving_logs('Server', rounded_response, network_response[2])

                # Condition when the server doesn't respond (Timed Out)
                elif response_server is None:
                    server_status.config(text=network_response[3], fg='white', bg='red')
                    update_status(server_ping, '-')
                    profit_btn.config(state='disabled')
                    saving_logs('Server', rounded_response, network_response[3])
                
                time.sleep(1)

            except TimeoutError:
                ping_and_update()
           
            except OSError:
                ping_and_update()

            except Exception:
                ping_and_update()

    if ping_thread is None or not ping_thread.is_alive():
        hide_event.clear()  # Reset the hide event
        ping_thread = threading.Thread(target=ping_and_update, daemon=True)
        ping_thread.start()

def ping_Internet():
    global ping_thread_two
    def ping_and_update_Internet():
        while not hide_event.is_set():
            
            response_Internet = ping(internet_ip, unit='ms')
            
            try:
                rounded_response = round(response_Internet, 2) if isinstance(response_Internet, float) else None
                
                # Condition when the ping to the IP Address responds correctly for the first time or the connection comes back.
                if isinstance(response_Internet, float) and internet_status.cget('text') in ['', 'Host Unknown', 'Check Internet', 'Timed Out', 'Check Ethernet']:
                    internet_status.config(text=network_response[1], fg='white', bg='green')
                    update_status(internet_ping, f'Ping: {rounded_response} ms')
                    saving_logs('Internet', rounded_response, network_response[1])
                
                # Condition when the IP Address keeps responding to ping
                elif isinstance(response_Internet, float) and internet_status.cget('text') == network_response[1]:
                    update_status(internet_ping, f'Ping: {rounded_response} ms')
                    saving_logs('Internet', rounded_response, network_response[1])
                
                # Condition when the IP Address doesn't respond (Disconnection)
                elif response_Internet is False:
                    internet_status.config(text=network_response[2], fg='white', bg='red')
                    update_status(internet_ping, '-')
                    saving_logs('Internet', rounded_response, network_response[2])

                # Condition when the IP Address doesn't respond (Timed Out)
                elif response_Internet is None:
                    internet_status.config(text=network_response[3], fg='white', bg='red')
                    update_status(internet_ping, '-')
                    saving_logs('Internet', rounded_response, network_response[3])
                
                time.sleep(1)
                
            except TimeoutError:
                ping_and_update_Internet()
            
            except OSError:
                ping_and_update_Internet()
            
            except Exception:
                ping_and_update_Internet() 
        
    if ping_thread_two is None or not ping_thread_two.is_alive():
        hide_event.clear()  # Reset the hide event
        ping_thread_two = threading.Thread(target=ping_and_update_Internet, daemon=True)
        ping_thread_two.start()

def update_status(label_ping, ping_text=''):
    if label_ping.cget('text') != ping_text:  # Update only if different
        label_ping.config(text=ping_text)

def start_drag(event):
    # Store the initial mouse position
    window.x_offset = event.x
    window.y_offset = event.y

def on_drag(event):
    # Calculate the new position of the window
    x = event.x_root - window.x_offset
    y = event.y_root - window.y_offset
    window.geometry(f"+{x}+{y}")

def hide():
    # Stops the threads of the functions ping_Internet & ping_Server
    hide_event.set()

    # Change the size of the window
    window.geometry('375x43+100+685')

    # Unmap all the buttons of the first 2 rows
    hide_btn.grid_forget()

    server_status.grid_forget()
    server_ping.grid_forget()

    internet_status.grid_forget()
    internet_ping.grid_forget()

    date_label.grid_forget()
    version_label.grid_forget()

    # Change the position of the tools buttons to be displayed on a new windows size
    shown_btn.grid(row=0, column=0, pady=2, sticky='n')
    close_btn.grid(row=0, column=0, padx=2, pady=0, sticky='s')

    igtf_btn.grid(row=0, column=1)

    calculator_btn.grid(row=0, column=2, padx=2, pady=5, sticky='w')
    web_browser_btn.grid(row=0, column=3, padx=2, pady=5, sticky='w')
    profit_btn.grid(row=0, column=4, padx=2, pady=5, sticky='w')

    scanner_btn.grid(row=0, column=5, padx=2, pady=5, sticky='w')
    explorer_btn.grid(row=0, column=6, padx=2, pady=5, sticky='w')
    bcv_parallel_calc_btn.grid(row=0, column=7, padx=2, pady=5, sticky='w')

    parallel_price_btn.grid(row=0, column=8, padx=2, pady=5, sticky='w')
    script_btn.grid(row=0, column=9, padx=0, sticky='w')

def shown():
    # Start both functions creating 2 new threads.
    ping_Internet()
    ping_Server()

    # Change the size of the window.
    window.geometry('340x80+100+648')
    
    # Unmap button.
    hide_btn.grid_forget()

    server_status.grid_forget()
    server_ping.grid_forget()

    internet_status.grid_forget()
    internet_ping.grid_forget()

    date_label.grid_forget()
    version_label.grid_forget()
    shown_btn.grid_forget()

    igtf_btn.grid_forget()

    calculator_btn.grid_forget()
    web_browser_btn.grid_forget()
    profit_btn.grid_forget()

    scanner_btn.grid_forget()
    explorer_btn.grid_forget()
    bcv_parallel_calc_btn.grid_forget()

    parallel_price_btn.grid_forget()
    script_btn.grid_forget()
    
    # Label Position
    # Row 2
    igtf_btn.grid(row=2, column=0)

    calculator_btn.grid(row=2, column=1 ,sticky='w')
    web_browser_btn.grid(row=2, column=1, padx=5)
    profit_btn.grid(row=2, column=1, sticky='e')

    scanner_btn.grid(row=2, column=2, sticky='w')
    explorer_btn.grid(row=2, column=2, padx=3, sticky='')
    bcv_parallel_calc_btn.grid(row=2, column=2, sticky='e')

    parallel_price_btn.grid(row=2, column=3, sticky='w')
    script_btn.grid(row=2, column=3, padx=37, sticky='w')


    # Row 0, 1
    hide_btn.grid(row=0, column=0, pady=0, ipadx=0, ipady=0)
    close_btn.grid(row=1, column=0, padx= 5, pady=0, sticky='n')

    server_status.grid(row=0, column=1, padx=3,  pady=1, sticky='')
    server_ping.grid(row=1, column=1, padx=0,  pady=1, sticky='n')

    internet_status.grid(row=0, column=2, padx=5, pady=1, sticky='')
    internet_ping.grid(row=1, column=2, padx=0, pady=1, sticky='n')

    version_label.grid(row=1, column=3, padx=2, pady=1, sticky='wn')
    date_label.grid(row=0, column=3, pady=1, sticky='w')

hide_btn = Button(window, text='▼', font=('Arial', 6), width=2, bg='#121212', fg='white', command=hide)
shown_btn = Button(window, text='▲', font=('Arial', 6), width=2, bg='#121212', fg='white', command=shown)

window.after(0, ping_Server) # Start function at the beginning of the program.
window.after(0, ping_Internet) # Start function at the beginning of the program.

window.bind("<Button-1>", start_drag) # Bind to make the window movable
window.bind("<B1-Motion>", on_drag) # Bind to make the window movable

# Label Position
# Row 2
igtf_btn.grid(row=2, column=0)

calculator_btn.grid(row=2, column=1 ,sticky='w')
web_browser_btn.grid(row=2, column=1)
profit_btn.grid(row=2, column=1, sticky='e')


scanner_btn.grid(row=2, column=2, padx=3, sticky='w')
explorer_btn.grid(row=2, column=2, padx=3, sticky='')
bcv_parallel_calc_btn.grid(row=2, column=2, sticky='e')

parallel_price_btn.grid(row=2, column=3, sticky='w')
script_btn.grid(row=2, column=3, padx=37, sticky='w')


# Row 0, 1
hide_btn.grid(row=0, column=0, pady=0, ipadx=0, ipady=0)
close_btn.grid(row=1, column=0, padx= 5, pady=0, sticky='n')

server_status.grid(row=0, column=1, padx=3,  pady=1, sticky='')
server_ping.grid(row=1, column=1, padx=0,  pady=1, sticky='n')

internet_status.grid(row=0, column=2, padx=5, pady=1, sticky='')
internet_ping.grid(row=1, column=2, padx=0, pady=1, sticky='n')

version_label.grid(row=1, column=3, padx=2, pady=1, sticky='wn')
date_label.grid(row=0, column=3, pady=1, sticky='w')

# Execute windows
window.mainloop()
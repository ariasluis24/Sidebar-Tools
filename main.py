from tkinter import *
import datetime
import subprocess
import locale
# import psutil
# import time


locale.setlocale(locale.LC_ALL, 'es_VE')

igtf_calc_path = "C:\\Users\\l.arias\\Documents\\DOCUMENTOS CAJA LUIS ARIAS\\Nueva carpeta\\Python\\Nueva carpeta\\IGTF-Calc\\GUI.py"
explorer_path = 'C:\\Windows\\explorer.exe'
scanner_path = "C:\\Program Files (x86)\\epson\\Epson Scan 2\\Core\\es2launcher.exe"
web_browser_path = 'C:\\Program Files (x86)\\Microsoft\\Edge\\Application\\msedge.exe'
calculator_path = 'C:\\Windows\\System32\\calc.exe'
network_Test_path = "C:\\Windows\\System32\\cmd.exe"
profit_path = 'P:\\Profit_a\\profit_a.exe'

ip_address = '8.8.8.8'


# // TODO Make just one function to open all programs.
# TODO Change the state of the button if the program is already open.

# // TODO Find a way to open the IGTF Calculator from python.
def open_igtf_calc():
    # subprocess.Popen([igtf_calc_path])
    subprocess.Popen(["python", igtf_calc_path])
    # igtf_btn.config(state=DISABLED)
    # Replace 'your_script.py' with the name of your Python script
    # script_name = 'GUI.py'  # Change this to your actual script name
    # try:
    #     while True:
    #         if is_script_running(script_name):
    #             print(f"{script_name} is running.")
    #         else:
    #             print(f"{script_name} is not running.")
            
    #         # Wait for a specific interval before checking again (e.g., 5 seconds)
    #         time.sleep(5)  # Change the interval as needed
    # except KeyboardInterrupt:
    #     print("Stopped checking.")

def is_script_running(script_name):
#     # Normalize the script name to avoid issues with case sensitivity
#     script_name = script_name.lower()
#     # Iterate through all running processes
#     for proc in psutil.process_iter(['pid', 'name', 'cmdline']):
#         try:
#             # Check if the process is a Python process
#             if proc.info['name'] == 'python.exe' or proc.info['name'] == 'pythonw.exe':
#                 # Check if the script name is in the command line arguments
#                 if any(script_name in arg.lower() for arg in proc.info['cmdline']):
#                     return True
#         except (psutil.NoSuchProcess, psutil.AccessDenied, psutil.ZombieProcess):
#             pass
                
#     return False
    pass

#// TODO Make this .bat apear in a new cmd window.
def open_Network_Test():
    subprocess.Popen(f'start cmd.exe /K ping {ip_address}', shell=True)

# TODO Make a way to check if there is connection to the server in order to open profit.
def open_Tool(tool_path):
    subprocess.Popen([tool_path])

# Windows entity  
window = Tk()
window.attributes('-topmost',True) # Makes the window always on top.

# Config of window
# icon = PhotoImage(file='src\\icon.png')
window.title('Sidebar Tools')
# window.iconphoto(True, icon)
window.geometry('230x370+1120+70') # Default size of the window & Position.
# window.minsize(800, 370) # Minimun size of the window
# window.maxsize(800, 370) # Maximun size of the window
    

now = datetime.datetime.now()
date_actual = now.strftime('%a %d/%b/%y')

# Creating Labels

title = Label(window, text='Tools', font=('Roboto', 12, 'bold'), justify='center', width=10)

igtf_btn = Button(window, text='IGTF Calculator', font=('Arial', 10), width=5, height=1, justify='center', command=open_igtf_calc)
calculator_btn = Button(window, text='Calculator', font=('Arial', 10), width=5, height=1, justify='center',  command= lambda: open_Tool(calculator_path))
web_browser_btn = Button(window, text='Web Browser', font=('Arial', 10), width=5, height=1, justify='center',  command= lambda: open_Tool(web_browser_path))
profit_btn = Button(window, text='Profit', font=('Arial', 10), width=5, height=1, justify='center', command= lambda: open_Tool(profit_path))
scanner_btn = Button(window, text='Scanner', font=('Arial', 10), width=5, height=1, justify='center',  command= lambda: open_Tool(scanner_path))
explorer_btn = Button(window, text='File Explorer', font=('Arial', 10), width=5, height=1, justify='center',  command= lambda: open_Tool(explorer_path))
network_btn = Button(window, text='Network Test', font=('Arial', 10), width=5, height=1, justify='center', command=open_Network_Test)

date_label = Label(window, text=date_actual, font=('Arial', 10,'bold'))

# Label Position
title.grid(row=0, column=0, sticky='nwse')
igtf_btn.grid(row=1, column=0, padx=3, pady=2, sticky='nwse')
calculator_btn.grid(row=2, column=0, padx=3, pady=2,sticky='nwse')
web_browser_btn.grid(row=3, column=0, padx=3, pady=2,sticky='nwse')
profit_btn.grid(row=4, column=0, padx=3, pady=2, sticky='nwse')
scanner_btn.grid(row=5, column=0, padx=3, pady=2, sticky='nwse')
explorer_btn.grid(row=6, column=0, padx=3, pady=2, sticky='nwse')
network_btn.grid(row=7, column=0, padx=3, pady=2, sticky='nwse')
date_label.grid(row=8, column=0, pady=100, sticky='s')



# Execute windows
window.mainloop()
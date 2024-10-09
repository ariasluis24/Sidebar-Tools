from tkinter import *
import datetime
import subprocess

igtf_calc_path = "C:\\Users\\l.arias\Documents\\DOCUMENTOS CAJA LUIS ARIAS\\Nueva carpeta\\Python\\Nueva carpeta\\IGTF-Calc\\GUI.py"
explorer_path = 'C:\\Windows\\explorer.exe'
scanner_path = "C:\\Program Files (x86)\\epson\\Epson Scan 2\\Core\\es2launcher.exe"
web_browser_path = 'C:\\Program Files (x86)\\Microsoft\\Edge\\Application\\msedge_proxy.exe'
calculator_path = 'C:\\Windows\\System32\\calc.exe'
network_Test_path = r"C:\\Windows\\System32\\cmd.exe"

ip_address = '8.8.8.8'

web_arg = '--profile-directory=Default'
web_arg_2 = '--app-id=hnpfjngllnobngcgfapefoaidbinmjnm'
web_arg_3 = '--app-url=https://web.whatsapp.com/'
web_arg_4 = '--app-launch-source=4'


# TODO Make just one function to open all programs.
# TODO Change the state of the button if the program is already open.

def open_Calculator():
    subprocess.Popen([calculator_path])

def open_Web_Browser():
    subprocess.Popen([web_browser_path, web_arg, web_arg_2, web_arg_3, web_arg_4])

def open_Explorer():
    subprocess.Popen([explorer_path])

#// TODO Make this .bat apear in a new cmd window.
def open_Network_Test():
    subprocess.Popen(f'start cmd.exe /K ping {ip_address}', shell=True)

def open_Scanner():
    subprocess.Popen([scanner_path])

#TODO Find a way to open the IGTF Calculator from python.
def open_igtf_calc():
    # subprocess.Popen([igtf_calc_path])
    subprocess.run(["python", igtf_calc_path])
    
# Windows entity  
window = Tk()

# Config of window
# icon = PhotoImage(file='src\\icon.png')
window.title('Sidebar Tools')
# window.iconphoto(True, icon)
window.geometry('230x370') # Default size of the window
# window.minsize(800, 370) # Minimun size of the window
# window.maxsize(800, 370) # Maximun size of the window
    

now = datetime.datetime.now()
date_actual = now.strftime('%d-%m-%y')

# Creating Labels

title = Label(window, text='Title', font=('Roboto', 12, 'bold'), justify='center', width=10)

igtf_btn = Button(window, text='IGTF Calculator', font=('Arial', 10), width=5, height=1, justify='center', command=open_igtf_calc)
calculator_btn = Button(window, text='Calculator', font=('Arial', 10), width=5, height=1, justify='center', command=open_Calculator)
web_browser_btn = Button(window, text='Web Browser', font=('Arial', 10), width=5, height=1, justify='center', command=open_Web_Browser)
profit_btn = Button(window, text='Profit', font=('Arial', 10), width=5, height=1, justify='center')
scanner_btn = Button(window, text='Scanner', font=('Arial', 10), width=5, height=1, justify='center', command=open_Scanner)
explorer_btn = Button(window, text='File Explorer', font=('Arial', 10), width=5, height=1, justify='center', command=open_Explorer)
network_btn = Button(window, text='Network Test', font=('Arial', 10), width=5, height=1, justify='center', command=open_Network_Test)

date_label = Label(window, text=date_actual, font=('Arial', 8,'bold'))

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
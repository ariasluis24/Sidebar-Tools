from tkinter import *
import datetime
import subprocess


def open_Network_Test():
    subprocess.run([r"C:\\Users\\l.arias\\Documents\\DOCUMENTOS CAJA LUIS ARIAS\\Nueva carpeta\\Python\\Nueva carpeta\\Sidebar Tools\\src\\test.bat"])


#TODO Find a way to open the IGTF Calculator from python.
def open_igtf_calc():
    #  subprocess.run([r"C:\\Users\\l.arias\Documents\\DOCUMENTOS CAJA LUIS ARIAS\\Nueva carpeta\\Python\\Nueva carpeta\\IGTF-Calc\\GUI.py"])
    pass

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

#TODO C:\Windows\explorer.exe

# Creating Labels

title = Label(window, text='Title', font=('Roboto', 12, 'bold'), justify='center', width=10)

igtf_btn = Button(window, text='IGTF Calculator', font=('Arial', 10), width=5, height=1, justify='center', command=open_igtf_calc)
calculator_btn = Button(window, text='Calculator', font=('Arial', 10), width=5, height=1, justify='center')
web_browser_btn = Button(window, text='Web Browser', font=('Arial', 10), width=5, height=1, justify='center')
profit_btn = Button(window, text='Profit', font=('Arial', 10), width=5, height=1, justify='center')
scanner_btn = Button(window, text='Scanner', font=('Arial', 10), width=5, height=1, justify='center')
explorer_btn = Button(window, text='File Explorer', font=('Arial', 10), width=5, height=1, justify='center')
network_btn = Button(window, text='Network Test', font=('Arial', 10), width=5, height=1, justify='center', command=open_Network_Test)

date_label = Label(window, text=date_actual, font=('Arial', 8,'bold'))

# Label Position
title.grid(row=0, column=0, sticky='nwse')
igtf_btn.grid(row=1, column=0, sticky='nwse')
calculator_btn.grid(row=2, column=0, pady=2,sticky='nwse')
web_browser_btn.grid(row=3, column=0, pady=2,sticky='nwse')
profit_btn.grid(row=4, column=0, pady=2, sticky='nwse')
scanner_btn.grid(row=5, column=0, pady=2, sticky='nwse')
explorer_btn.grid(row=6, column=0, pady=2, sticky='nwse')
network_btn.grid(row=7, column=0, pady=2, sticky='nwse')
date_label.grid(row=8, column=1, pady=2, sticky='nwse')
window.mainloop()
import typing
from tkinter.ttk import Frame, Notebook, Treeview
from tkinter import *

from gui.controls_tab import controls_tab
from gui.connection_config_tab import connection_config_tab


def init_gui():
    window = Tk()
    window.title("Robot service app")
    window.geometry('1500x450')
    
    tab_control = Notebook(window)  
    tab1 = Frame(tab_control)  
    tab2 = Frame(tab_control)

    
    tab_control.add(tab1, text='controls_tab')  
    tab_control.add(tab2, text='connection_config')

    tab_control.pack(expand=1, fill='both')  

    
    controls_tab(tab1)
    connection_config_tab(tab2)

    
    window.mainloop()

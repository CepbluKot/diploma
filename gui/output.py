import typing
from tkinter.ttk import Frame, Notebook, Treeview
from tkinter import *

from gui.controls_tab import controls_tab
from gui.connection_config_tab import connection_config_tab



import tkinter, threading, json
import tkintermapview
import paho.mqtt.client as mqtt


def open_secondary_window():
    # Create secondary (or popup) window.
    secondary_window = Toplevel()
    secondary_window.title("Secondary Window")
    secondary_window.config(width=500, height=500)
    
    old_marker = None


    map_widget = tkintermapview.TkinterMapView(secondary_window, width=500, height=500, corner_radius=0)
    map_widget.pack(fill="both", expand=True)
    map_widget.set_tile_server("https://mt0.google.com/vt/lyrs=s&hl=en&x={x}&y={y}&z={z}&s=Ga", max_zoom=22)  # google satellite
    map_widget.set_position(56.255518, 38.467219)


    

def init_gui():
    window = Tk()
    window.title("Robot service app")
    window.geometry('1500x450')
    
    tab_control = Notebook(window)  
    tab1 = Frame(tab_control)  
    tab2 = Frame(tab_control)
    tab3 = Frame(tab_control)
    
    tab_control.add(tab1, text='controls_tab')  
    tab_control.add(tab2, text='connection_config')
    tab_control.add(tab3, text='map')

    tab_control.pack(expand=1, fill='both')  

    rofl=controls_tab(tab1)
    
    lora_ports_selector, \
    server_address_entry,\
    conn_state_label_lora,\
    conn_state_label_internet,\
    btn_connect,\
    connection_method_lora_radiobtn,\
    connection_method_server_radiobtn,\
    connection_type_auto_radiobtn,\
    connection_type_manual_radiobtn = connection_config_tab(tab2)
    open_secondary_window()

    def pp():
        while 1 :
            import time
            time.sleep(1)
            rofl.config(text=str(time.time()))

    import threading
    t1 = threading.Thread(target=pp)
    t1.start()
    window.mainloop()
    t1.join()
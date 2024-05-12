import typing, time
import threading
from tkinter.ttk import Frame, Notebook, Treeview
from tkinter import *

from gui.controls_tab import controls_tab
from gui.connection_config_tab import connection_config_tab


from transceiver_modules.global_transceiver import GlobalTransceiver, ManualConnectionMethod
import tkintermapview
import paho.mqtt.client as mqtt


def open_map_window():
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
    
    tab_control.add(tab1, text='controls_tab')  
    tab_control.add(tab2, text='connection_config')

    tab_control.pack(expand=1, fill='both')  

    conn_status_indicator = controls_tab(tab1)
    
    connection_status_internet_param_label,\
    connection_status_lora_param_label,\
    connection_method_param,\
    connection_type_auto_radiobtn,\
    connection_method_lora_radiobtn,\
    connection_method_server_radiobtn = connection_config_tab(tab2)


    def nothin(non=None, ):
        pass
    
    def gui_socket_connect_callback():
        connection_status_internet_param_label.configure(text='connected',
                                                         background='green')

    def gui_socket_disconnect_callback():
        connection_status_internet_param_label.configure(text='no connection',
                                                         background='red')
    
    def gui_socket_reconnect_callback():
        connection_status_internet_param_label.configure(text='connected',
                                                         background='green')
            
    def gui_lora_disconnect_callback():
        connection_status_lora_param_label.configure(text='no connection',
                                                    background='red')
    
    def gui_lora_reconnect_callback():
        connection_status_lora_param_label.configure(text='connected',
                                                    background='green')

    def gui_lora_connect_callback():
        connection_status_lora_param_label.configure(text='connected',
                                                    background='green')


    trans = GlobalTransceiver(nothin,
                              nothin, 
                              nothin, 
                              nothin,  
                              nothin,
                              gui_socket_connect_callback,
                              gui_socket_disconnect_callback,
                              gui_socket_reconnect_callback,
                              gui_lora_connect_callback,
                              gui_lora_disconnect_callback,
                              gui_lora_reconnect_callback)
    
    def change_connection_type_to_auto_action():
        nonlocal trans
        trans.set_connection_mode(True)

    def change_connection_type_to_manual_action():
        nonlocal trans
        new_conn_type = connection_method_param.get()

        if new_conn_type == "LoRa":
            trans.set_connection_mode(False, ManualConnectionMethod.LoRa)
        elif new_conn_type == "socket":
            trans.set_connection_mode(False, ManualConnectionMethod.internet)


    connection_type_auto_radiobtn.config(command=change_connection_type_to_auto_action)

    connection_method_lora_radiobtn.config(command=change_connection_type_to_manual_action)
    connection_method_server_radiobtn.config(command=change_connection_type_to_manual_action)
    
    open_map_window()
    
    def conn_type_updater():
        while 1 :
            time.sleep(1)
            curr_conn_type = trans.get_curr_connection_type()
            
            if curr_conn_type.value == 'LoRa':
                conn_status_indicator.config(background='green')
                conn_status_indicator.config(text='LoRa')

            elif curr_conn_type.value == 'socket':
                conn_status_indicator.config(background='green')
                conn_status_indicator.config(text='internet')

            else:
                conn_status_indicator.config(background='red')
                conn_status_indicator.config(text='no connection')

    def test_sender(): 
        while 1:
            if trans:
                time.sleep(1)
                trans.send('elloy')

 
    conn_type_upd_thr = threading.Thread(target=conn_type_updater)
    conn_type_upd_thr.daemon = True
    conn_type_upd_thr.start()

    test_send_thr = threading.Thread(target=test_sender)
    test_send_thr.daemon = True
    test_send_thr.start()

    window.mainloop()
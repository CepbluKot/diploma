import tkintermapview
import typing, time
import threading
from tkinter.ttk import Frame, Notebook
from tkinter import *

from operator_modules.gui.controls_tab import controls_tab
from operator_modules.gui.connection_config_tab import connection_config_tab
from operator_modules.transceiver_modules.global_transceiver import global_transceiver, ManualConnectionMethod
from operator_modules.ds3_control.controller import run as ds3_run
from operator_modules.gui.buttons_control import ButtonsController, EngineSide
from data_formats.temp_hum_data import TempHumData
from data_formats.gnss_data import GNSSData
from data_formats.encoder_data import EngineEncoderData


global_lat = None
global_lon = None


def open_map_window():
    secondary_window = Toplevel()
    secondary_window.title("GNSS")
    secondary_window.config(width=500, height=500)
    
    map_widget = tkintermapview.TkinterMapView(secondary_window, width=500, height=500, corner_radius=0)
    map_widget.pack(fill="both", expand=True)
    map_widget.set_tile_server("https://mt0.google.com/vt/lyrs=s&hl=en&x={x}&y={y}&z={z}&s=Ga", max_zoom=22)  # google satellite
    map_widget.set_position(56.255518, 38.467219, marker=True)

    def pos_updater():
        global global_lat
        global global_lon
        
        while True:
            if global_lat is not None and global_lon is not None:
                map_widget.set_position(global_lat, global_lon, marker=True)
            time.sleep(1)

    update_thr = threading.Thread(target=pos_updater)
    update_thr.daemon = True
    update_thr.start()

def init_gui():
    window = Tk()
    window.title("Robot control app")
    window.geometry("1500x500")
    
    tab_control = Notebook(window)  
    tab1 = Frame(tab_control)  
    tab2 = Frame(tab_control)
    
    tab_control.add(tab1, text="Управление")  
    tab_control.add(tab2, text="Подключение")

    tab_control.pack(expand=1, fill="both")  

    open_map_window()

    (btn_move_forward_left_eng,
     btn_stop_left_eng,
     btn_move_backward_left_eng,
     btn_move_forward_right_eng,
     btn_stop_right_eng,
     btn_move_backward_right_eng,
     btn_stop_full,
     lat_value_field,
     lon_value_field,
     speed_value_field,
     track_value_field,
     temp_value_field,
     hum_value_field,
     left_eng_encoder_value_field,
     right_eng_encoder_value_field,
     conn_status_indicator) = controls_tab(tab1)
    
    (connection_status_internet_param_label,
     connection_status_lora_param_label,
     connection_method_param,
     connection_type_auto_radiobtn,
     connection_method_lora_radiobtn,
     connection_method_server_radiobtn) = connection_config_tab(tab2)


    def gui_socket_connect_callback():
        connection_status_internet_param_label.configure(text="подключено",
                                                         background="green")

    def gui_socket_disconnect_callback():
        connection_status_internet_param_label.configure(text="нет подключения",
                                                         background="red")
    
    def gui_socket_reconnect_callback():
        connection_status_internet_param_label.configure(text="подключено",
                                                         background="green")
            
    def gui_lora_disconnect_callback():
        connection_status_lora_param_label.configure(text="нет подключения",
                                                    background="red")
    
    def gui_lora_reconnect_callback():
        connection_status_lora_param_label.configure(text="подключено",
                                                    background="green")

    def gui_lora_connect_callback():
        connection_status_lora_param_label.configure(text="подключено",
                                                    background="green")

    def encoder_data_callback(data: dict):
        parsed_data = EngineEncoderData.parse_obj(data)
        left_eng_encoder_value_field.configure(text=str(parsed_data.left))
        right_eng_encoder_value_field.configure(text=str(parsed_data.right))

    def gnss_data_callback(data: dict):
        global global_lat
        global global_lon
        
        parsed_data = GNSSData.parse_obj(data)
        lat_value_field.configure(text=str(parsed_data.lat))
        lon_value_field.configure(text=str(parsed_data.lon))
        speed_value_field.configure(text=str(parsed_data.spd_over_grnd_kmph))
        track_value_field.configure(text=str(parsed_data.true_track))

        global_lat=parsed_data.lat
        global_lon=parsed_data.lon

    def temp_hum_data_callback(data: dict):
        parsed_data = TempHumData.parse_obj(data)
        temp_value_field.configure(text=str(parsed_data.temperature))
        hum_value_field.configure(text=str(parsed_data.humidity))

    global_transceiver.gui_lora_reconnect_callback = gui_lora_reconnect_callback
    global_transceiver.gui_socket_disconnect_callback = gui_socket_disconnect_callback
    global_transceiver.gui_socket_reconnect_callback = gui_socket_reconnect_callback
    global_transceiver.gui_lora_disconnect_callback = gui_lora_disconnect_callback
    global_transceiver.gui_socket_connect_callback = gui_socket_connect_callback
    global_transceiver.gui_lora_connect_callback = gui_lora_connect_callback

    global_transceiver.encoder_data_callback = encoder_data_callback
    global_transceiver.gnss_data_callback = gnss_data_callback
    global_transceiver.temp_hum_data_callback = temp_hum_data_callback


    def change_connection_type_to_auto_action():
        global_transceiver.set_connection_mode(True)

    def change_connection_type_to_manual_action():
        new_conn_type = connection_method_param.get()

        if new_conn_type == "LoRa":
            global_transceiver.set_connection_mode(False, ManualConnectionMethod.LoRa)
        
        elif new_conn_type == "socket":
            global_transceiver.set_connection_mode(False, ManualConnectionMethod.internet)


    connection_type_auto_radiobtn.config(command=change_connection_type_to_auto_action)

    connection_method_lora_radiobtn.config(command=change_connection_type_to_manual_action)
    connection_method_server_radiobtn.config(command=change_connection_type_to_manual_action)
    

    buttons_controller = ButtonsController(global_transceiver.send)
    
    def btn_move_forward_left_eng_act():
        buttons_controller.fwd_button_press(EngineSide.left)

    def btn_move_backward_left_eng_act():
        buttons_controller.bwd_button_press(EngineSide.left)

    def btn_stop_left_eng_act():
        buttons_controller.stop_button_press(EngineSide.left)

    def btn_move_forward_right_eng_act():
        buttons_controller.fwd_button_press(EngineSide.right)

    def btn_move_backward_right_eng_act():
        buttons_controller.bwd_button_press(EngineSide.right)

    def btn_stop_right_eng_act():
        buttons_controller.stop_button_press(EngineSide.right)

    def btn_stop_full_act():
        buttons_controller.stop_button_press()

    btn_move_forward_left_eng.configure(command=btn_move_forward_left_eng_act)
    btn_move_backward_left_eng.configure(command=btn_move_backward_left_eng_act)
    btn_stop_left_eng.configure(command=btn_stop_left_eng_act)
    
    btn_move_forward_right_eng.configure(command=btn_move_forward_right_eng_act)
    btn_move_backward_right_eng.configure(command=btn_move_backward_right_eng_act)
    btn_stop_right_eng.configure(command=btn_stop_right_eng_act)

    btn_stop_full.configure(command=btn_stop_full_act)


    
    def conn_type_updater():
        while True:
            time.sleep(1)
            curr_conn_type = global_transceiver.get_curr_connection_type()
            
            if curr_conn_type.value == "LoRa":
                conn_status_indicator.config(background="green")
                conn_status_indicator.config(text="LoRa")

            elif curr_conn_type.value == "socket":
                conn_status_indicator.config(background="green")
                conn_status_indicator.config(text="internet/LAN")

            else:
                conn_status_indicator.config(background="red")
                conn_status_indicator.config(text="нет подключения")

    ds3_run(global_transceiver.send)
 
    conn_type_upd_thr = threading.Thread(target=conn_type_updater)
    conn_type_upd_thr.daemon = True
    conn_type_upd_thr.start()

    window.mainloop()

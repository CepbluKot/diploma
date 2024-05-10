import serial.tools.list_ports
import typing
from tkinter import *
from tkinter.ttk import Combobox
# from gui.controls_tab import conn_type_indicator


def connection_config_tab(frame):
    
    # --- LoRa port selector ---
    def get_ports():
        ports = serial.tools.list_ports.comports()
        names = [""]

        for name, desc, hwid in sorted(ports):
            names.append(name)

        lora_ports_selector.config(values=names)

    lora_ports_label = Label(master=frame, text='LoRa transmitter port', background='white')
    lora_ports_label.grid(row=1, column=1, padx=(100, 10), pady=(100,10))

    lora_ports_selector = Combobox(master=frame, state="readonly", postcommand=get_ports)
    lora_ports_selector.grid(row=2, column=1, padx=(100, 10) )


    btn_stop_full = Button(master=frame, text="connect",)
    btn_stop_full.grid(row=3, column=1,  pady=15,padx=(100, 10))

    conn_type_label = Label(master=frame, text='Not connected', background='white')
    conn_type_label.grid(row=3, column=2, )

    # --- Server address selector ---

    server_address_label = Label(master=frame, text='Server Address', background='white')
    server_address_label.grid(row=1, column=2+1, padx=(100, 10), pady=(100,10))

    server_address_entry = Entry(master=frame, text='Server address', )
    server_address_entry.grid(row=2, column=2+1, padx=(100, 10))

    # --- conn available mqtt http

    btn_stop_full = Button(master=frame, text="connect",)
    btn_stop_full.grid(row=3, column=2+1,  pady=15,padx=(100, 10))

    conn_type_label = Label(master=frame, text='Not connected', background='white')
    conn_type_label.grid(row=3, column=3+1, )


    # --- connection type selector ---

    connection_type_label = Label(master=frame, text='Connection Type', background='white')
    connection_type_label.grid(row=1, column=3+1+1, padx=(100, 10), pady=(100,10))

    connection_type_param = StringVar()

    def change_conn_type_btn():
        
        print('wtf',connection_type_param.get() )

    connection_type_lora_radiobtn = Radiobutton(master=frame,  text="LoRa", variable=connection_type_param, anchor=W, value="LoRa", command=change_conn_type_btn)
    connection_type_lora_radiobtn.grid(row=2, column=3+1+1, padx=(100, 10), sticky=W)

    conn_type_indicator = Label(master=frame, text=str(None), background='white')
    conn_type_indicator.grid(row=2, column=5+1)

    connection_type_server_radiobtn = Radiobutton(master=frame, text="Server", variable=connection_type_param, anchor=W, value="Server", command=change_conn_type_btn)
    connection_type_server_radiobtn.grid(row=3, column=3+1+1, padx=(100, 10), sticky=W)

    conn_type_indicator = Label(master=frame, text=str(None), background='white')
    conn_type_indicator.grid(row=3, column=5+1)

    connection_type_mqtt_radiobtn = Radiobutton(master=frame, text="MQTT", variable=connection_type_param, anchor=W, value="MQTT", command=change_conn_type_btn)
    connection_type_mqtt_radiobtn.grid(row=4, column=3+1+1, padx=(100, 10), sticky=W)


    conn_type_indicator = Label(master=frame, text=str(None), background='white')
    conn_type_indicator.grid(row=4, column=5+1)

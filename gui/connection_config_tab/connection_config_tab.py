import serial.tools.list_ports
import typing
from tkinter import *
from tkinter.ttk import Combobox



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


    # --- Server address selector ---

    server_address_label = Label(master=frame, text='Server Address', background='white')
    server_address_label.grid(row=1, column=2, padx=(100, 10), pady=(100,10))

    server_address_entry = Entry(master=frame, text='Server address', )
    server_address_entry.grid(row=2, column=2, padx=(100, 10))

    # --- connection type selector ---

    use_http_param = BooleanVar()

    connection_type_label = Label(master=frame, text='Connection Type', background='white')
    connection_type_label.grid(row=1, column=3, padx=(100, 10), pady=(100,10))

    connection_type_lora_radiobtn = Radiobutton(master=frame,  text="LoRa", variable=use_http_param, anchor=W, value=False)
    connection_type_lora_radiobtn.grid(row=2, column=3, padx=(100, 10), sticky=W)

    connection_type_http_radiobtn = Radiobutton(master=frame, text="Server", variable=use_http_param, anchor=W, value=True)
    connection_type_http_radiobtn.grid(row=3, column=3, padx=(100, 10), sticky=W)

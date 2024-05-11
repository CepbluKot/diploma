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


    # man/auto connection


    connection_type_label = Label(master=frame, text='Connection Type', background='white')
    connection_type_label.grid(row=1, column=3+1+1, padx=(100, 10), pady=(100,10))

    connection_type_param = StringVar()

    def change_conn_type_btn():
        if connection_type_param.get() == "Auto":
            connection_method_lora_radiobtn.configure(state = DISABLED)
            connection_method_server_radiobtn.configure(state = DISABLED)

        elif connection_type_param.get() == "Manual":
            connection_method_lora_radiobtn.configure(state = NORMAL)
            connection_method_server_radiobtn.configure(state = NORMAL)

    
    connection_type_auto_radiobtn = Radiobutton(master=frame,  text="Auto", variable=connection_type_param, anchor=W, value="Auto", command=change_conn_type_btn)
    connection_type_auto_radiobtn.grid(row=2, column=3+1+1, padx=(100, 10), sticky=W)


    connection_type_manual_radiobtn = Radiobutton(master=frame, text="Manual", variable=connection_type_param, anchor=W, value="Manual", command=change_conn_type_btn)
    connection_type_manual_radiobtn.grid(row=3, column=3+1+1, padx=(100, 10), sticky=W)


    # --- connection method selector ---

    connection_method_label = Label(master=frame, text='Connection Method', background='white')
    connection_method_label.grid(row=1, column=3+1+1+1, padx=(100, 10), pady=(100,10))

    connection_method_param = StringVar()

    def change_conn_method_btn():
        print('method',connection_method_param.get() )

    connection_method_lora_radiobtn = Radiobutton(master=frame,  text="LoRa", variable=connection_method_param, anchor=W, value="LoRa", command=change_conn_method_btn)
    connection_method_lora_radiobtn.grid(row=2, column=3+1+1+1, padx=(100, 10), sticky=W)


    connection_method_server_radiobtn = Radiobutton(master=frame, text="Internet", variable=connection_method_param, anchor=W, value="Internet", command=change_conn_method_btn)
    connection_method_server_radiobtn.grid(row=3, column=3+1+1+1, padx=(100, 10), sticky=W)


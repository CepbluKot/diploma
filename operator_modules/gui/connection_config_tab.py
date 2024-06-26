from tkinter import *
# from gui.controls_tab import conn_type_indicator
from operator_modules.transceiver_modules.global_transceiver import ManualConnectionMethod


def connection_config_tab(frame):
    # man/auto connection

    data_check_label_internet = Label(master=frame, text="Тип подключения", background="white")
    data_check_label_internet.grid(row=1, column=3+1+1, padx=(100, 10), pady=(100,10))

    connection_type_param = StringVar()

    # --- connection method selector ---
    
    connection_type_auto_radiobtn = Radiobutton(master=frame,  text="Автоматически", variable=connection_type_param, anchor=W, value="Auto", )
    connection_type_auto_radiobtn.grid(row=2, column=3+1+1, padx=(100, 10), sticky=W)

    connection_method_lora_radiobtn = Radiobutton(master=frame,  text=ManualConnectionMethod.LoRa.value, variable=connection_type_param, anchor=W, value="LoRa", )
    connection_method_lora_radiobtn.grid(row=3, column=3+1+1, padx=(100, 10), sticky=W)
    
    connection_method_server_radiobtn = Radiobutton(master=frame, text=ManualConnectionMethod.internet.value, variable=connection_type_param, anchor=W, value="socket", )
    connection_method_server_radiobtn.grid(row=4, column=3+1+1, padx=(100, 10), sticky=W)
    
    # conn status

    connection_status_label = Label(master=frame, text="Состояние подключения", background="white")
    connection_status_label.grid(row=1, column=3+1+1+1+1, padx=(100, 10), pady=(100,10))

    connection_status_internet_label = Label(master=frame, text="Internet/LAN", background="white")
    connection_status_internet_label.grid(row=2, column=3+1+1+1+1,  padx=(100,10), pady=10)

    connection_status_internet_param_label = Label(master=frame, text="не подключено", background="white")
    connection_status_internet_param_label.grid(row=2, column=3+1+1+1+1+1,  padx=10, pady=10)

    connection_status_lora_label = Label(master=frame, text="LoRa", background="white")
    connection_status_lora_label.grid(row=3, column=3+1+1+1+1,  padx=(100,10), pady=10)

    connection_status_lora_param_label = Label(master=frame, text="не подключено", background="white")
    connection_status_lora_param_label.grid(row=3, column=3+1+1+1+1+1, padx=10, pady=10)


    return  connection_status_internet_param_label,\
            connection_status_lora_param_label,\
            connection_type_param,\
            connection_type_auto_radiobtn,\
            connection_method_lora_radiobtn,\
            connection_method_server_radiobtn

from tkinter.ttk import Button, Scale, Label
from tkinter import *
from random import randint


def controls_tab(frame):
    # --- left engine controls ---

    btn_move_forward_left_eng = Button(master=frame, text="↑")
    btn_move_forward_left_eng.grid(row=2, column=1, padx=(100, 10), pady=10)


    btn_stop_left_eng = Button(master=frame, text="СТОП",)
    btn_stop_left_eng.grid(row=3, column=1, padx=(100, 10), pady=10)


    btn_move_backward_left_eng = Button(master=frame, text="↓")
    btn_move_backward_left_eng.grid(row=4, column=1, padx=(100, 10), pady=10)


    # --- right engine controls ---


    btn_move_forward_right_eng = Button(master=frame, text="↑")
    btn_move_forward_right_eng.grid(row=2, column=3, padx=10, pady=10)


    btn_stop_right_eng = Button(master=frame, text="СТОП",)
    btn_stop_right_eng.grid(row=3, column=3, padx=10, pady=10)


    btn_move_backward_right_eng = Button(master=frame, text="↓")
    btn_move_backward_right_eng.grid(row=4, column=3, padx=10, pady=10)
    

    # --- full stop button ---


    btn_stop_full = Button(master=frame, text="ПОЛНАЯ ОСТАНОВКА",)
    btn_stop_full.grid(row=3, column=2, padx=10, pady=10)


    # --- gnss data fields ---

    gnss_label = Label(master=frame, text="GNSS", background="white")
    gnss_label.grid(row=1, column=4, padx=(100, 10), pady=(100,10))


    lat_label = Label(master=frame, text="Широта", background="white")
    lat_label.grid(row=2, column=4, padx=(100, 10), pady=10)
    
    lat_value_field = Label(master=frame, text=str(None), background="white")
    lat_value_field.grid(row=2, column=4+1, padx=5, pady=5)


    lon_label = Label(master=frame, text="Долгота", background="white")
    lon_label.grid(row=3, column=4, padx=(100, 10), pady=10)


    lon_value_field = Label(master=frame, text=str(None), background="white")
    lon_value_field.grid(row=3, column=4+1, padx=5, pady=5)

    
    speed_label = Label(master=frame, text="Скорость (км/ч)", background="white")
    speed_label.grid(row=4, column=4, padx=(100, 10), pady=10)

    speed_value_field = Label(master=frame, text=str(None), background="white")
    speed_value_field.grid(row=4, column=4+1, padx=5, pady=5)


    track_label = Label(master=frame, text="Курс", background="white")
    track_label.grid(row=5, column=4, padx=(100, 10), pady=10)

    track_value_field = Label(master=frame, text=str(None), background="white")
    track_value_field.grid(row=5, column=4+1, padx=5, pady=5)


    # --- temp and hum data fields ---

    dht11_label = Label(master=frame, text="DHT11", background="white")
    dht11_label.grid(row=1, column=6, padx=(100, 10), pady=(100,10))
    
    temp_label = Label(master=frame, text="Температура", background="white")
    temp_label.grid(row=2, column=6, padx=(100, 10), pady=10)
    

    temp_value_field = Label(master=frame, text=str(None), background="white")
    temp_value_field.grid(row=2, column=6+1, padx=10, pady=5)


    hum_label = Label(master=frame, text="Влага", background="white")
    hum_label.grid(row=3, column=6, padx=(100, 10), pady=10)
    
    hum_value_field = Label(master=frame, text=str(None), background="white")
    hum_value_field.grid(row=3, column=6+1, padx=10, pady=5)

    

    # --- encoders fields ---

    encoder_label = Label(master=frame, text="Энкодеры", background="white")
    encoder_label.grid(row=1, column=8, padx=(100, 10), pady=(100,10))
    
    left_eng_encoder_label = Label(master=frame, text="Левый двигатель", background="white")
    left_eng_encoder_label.grid(row=2, column=8, padx=(100, 10), pady=10)
    
    left_eng_encoder_value_field = Label(master=frame, text=str(None), background="white")
    left_eng_encoder_value_field.grid(row=2, column=8+1, padx=10, pady=5)



    right_eng_label = Label(master=frame, text="Правый двигатель", background="white")
    right_eng_label.grid(row=3, column=8, padx=(100, 10), pady=10)
    
    right_eng_encoder_value_field = Label(master=frame, text=str(None), background="white")
    right_eng_encoder_value_field.grid(row=3, column=8+1, padx=10, pady=5)
    

    # --- connection type indicator ---

    conn_status_label = Label(master=frame, text="Тип подключения", background="white")
    conn_status_label.grid(row=6, column=8, padx=(100, 10))

    conn_status_indicator = Label(master=frame, text=str(None), background="white")
    conn_status_indicator.grid(row=6, column=9, )

    return (btn_move_forward_left_eng,
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
            conn_status_indicator)
import json, pickle, threading, time, requests
import paho.mqtt.client as mqtt
import socket, json, serial
import serial.serialutil


class LoRaTransceiver:
    def __init__(self,
                 encoder_data_callback,
                 gnss_data_callback,
                 on_lora_connect_action,
                 on_lora_disconnect_action,
                 on_lora_reconnect_action,
                 ) -> None:
 
        
        self.config = json.load(open("config.json"))

        self.sender_port = self.config["LoRa_robot_sender_port"]
        self.receiver_port = self.config["LoRa_robot_receiver_port"]

        self.on_encoder_data = encoder_data_callback
        self.on_gnss_data = gnss_data_callback
        
        self.on_lora_connect_action = on_lora_connect_action
        self.on_lora_disconnect_action = on_lora_disconnect_action
        self.on_lora_reconnect_action = on_lora_reconnect_action

        self.is_lora_connected = True
        self.baudrate = 9600
        self.serial_interaction_lock = threading.Lock()

        self.serial_sender_conn = None
        self.serial_sender_conn = serial.Serial(self.sender_port, self.baudrate)
        
        self.serial_receiver_conn = None
        self.serial_receiver_conn = serial.Serial(self.receiver_port, self.baudrate)
        
        self.read_thr = threading.Thread(target=self.recv_thread, args=(10, ))
        self.read_thr.daemon = True
        self.read_thr.start()


    def send(self, data: str):
        with self.serial_interaction_lock:
            if self.serial_sender_conn:
                while self.serial_sender_conn.in_waiting:
                    self.serial_sender_conn.read_until(b"\r\n")
                
                self.serial_sender_conn.write(data.encode()+b"\r")


    def on_connect(self,):
        if not self.is_lora_connected:
            self.on_lora_reconnect_action()

        else:
            self.on_lora_connect_action()

        self.is_lora_connected = True

    def on_recv(self, data:str):
        try:
            parsed_data = json.loads(data)

            if "encoder_data" in parsed_data:
                self.on_encoder_data(parsed_data["encoder_data"])
            
            if "gnss_data" in parsed_data:
                self.on_gnss_data(parsed_data["gnss_data"])

        except Exception as e:
            print(f"error during receiving data:{e}")

    def recv_thread(self, conn_timeout: int):
        start_wait_time = time.time()
        while self.serial_receiver_conn.is_open:
            with self.serial_interaction_lock:
                if self.serial_receiver_conn.in_waiting:
                    read_data = self.serial_receiver_conn.read_until(b"\r\n")
                    read_data = read_data[:-2].decode()
                    
                    # while self.serial_receiver_conn.in_waiting:
                    #     pass
                    
                    start_wait_time = time.time()
                    self.on_recv(read_data)
                    self.on_connect()
                   
                else:
                    if self.is_lora_connected and abs(time.time() - start_wait_time) >= conn_timeout:
                       
                        self.is_lora_connected = False
                        self.on_lora_disconnect_action()
                        
                        while not self.is_lora_connected:
                            try:
                                if self.serial_receiver_conn.in_waiting:
                                    self.on_connect()

                            except Exception as e:
                                pass
                            

                        start_wait_time = time.time()

    def on_lora_disconnected(self):
        self.is_lora_connected = False
        self.on_lora_disconnect_action()
        
        def reconnect_procedure():
            while not self.is_lora_connected:
                try:
                    time.sleep(0.1)
                    while not self.serial_receiver_conn.is_open:
                        self.serial_receiver_conn.close()
                        self.serial_receiver_conn = serial.Serial(self.port, self.baudrate)

                    if self.serial_receiver_conn.in_waiting:
                        self.on_connect()

                except Exception as e:
                    pass
 
        reconnect_thr = threading.Thread(target=reconnect_procedure)
        reconnect_thr.daemon = True
        reconnect_thr.start()

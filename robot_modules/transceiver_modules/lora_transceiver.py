import json, pickle, threading, time, requests
import paho.mqtt.client as mqtt
import socket, json, serial
import serial.serialutil


class LoRaTransceiver:
    def __init__(self,
                 command_data_callback
                 ) -> None:
 
        
        self.config = json.load(open("config.json"))

        self.sender_port = self.config["LoRa_operator_sender_port"]
        self.receiver_port = self.config["LoRa_operator_receiver_port"]

        self.on_command_data = command_data_callback

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

    def on_recv(self, data:str):
        try:
            parsed_data = json.loads(data)

            if "command" in parsed_data:
                self.on_command_data(parsed_data["command"])
            
        except Exception as e:
            print(f"error during receiving data:{e}")

    def recv_thread(self):
        while self.serial_receiver_conn.is_open:
            with self.serial_interaction_lock:
                if self.serial_receiver_conn.in_waiting:
                    read_data = self.serial_receiver_conn.read_until(b"\r\n")
                    read_data = read_data[:-2].decode()
                    
                    # while self.serial_receiver_conn.in_waiting:
                    #     pass
                    
                    self.on_recv(read_data)
        
if __name__=="__main__":
    def nothin(rofl=None):
        pass
    n = LoRaTransceiver(nothin,nothin)


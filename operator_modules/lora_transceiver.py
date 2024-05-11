import json, pickle, threading, time, requests
import paho.mqtt.client as mqtt
import socket, json, serial


class LoRaTransceiver:
    def __init__(self, 
                 encoder_data_callback,
                 gnss_data_callback,
                 on_lora_disconnect_action,
                 on_lora_reconnect_action) -> None:
 
        
        self.config = json.load(open("config.json"))

        self.port = self.config['LoRa_operator_transceiver_port']

        self.on_encoder_data = encoder_data_callback
        self.on_gnss_data = gnss_data_callback
        
        self.on_lora_disconnect_action = on_lora_disconnect_action
        self.on_lora_reconnect_action = on_lora_reconnect_action

        self.is_lora_connected = True
        self.baudrate = 9600
        self.serial_conn = serial.Serial(self.port, self.baudrate)

        read_thr = threading.Thread(target=self.recv_thread, args=(10, ))
        read_thr.daemon = True
        read_thr.start()
        # read_thr.join()

    def send(self, data: str):
        self.serial_conn.write(data.encode()+b'\r')

    def on_connect(self,):
        if not self.is_lora_connected:
            print('lora connected')
            self.on_lora_reconnect_action()
        
        self.is_lora_connected = True

    def on_recv(self, data:str):
        parsed_data = data
        # parsed_data = json.loads(data)
        self.on_encoder_data(parsed_data)
        self.on_gnss_data(parsed_data)

    def recv_thread(self, conn_timeout: int):
        start_wait_time = time.time()
        while self.serial_conn.is_open:
            if self.serial_conn.in_waiting:
                read_data = self.serial_conn.read_until(b'\r\n')
                read_data = read_data[:-2].decode()
                self.on_recv(read_data)
                self.on_connect()
                start_wait_time = time.time()
            
            else:
                if self.is_lora_connected and time.time() - start_wait_time >= conn_timeout:
                    
                    self.on_lora_disconnected()
                    start_wait_time = time.time()

    def on_lora_disconnected(self):
        if self.is_lora_connected:
            print('lora disconnected')
        
        self.is_lora_connected = False
        self.on_lora_disconnect_action()
        def reconnect_procedure():
            while not self.is_lora_connected:
                try:
                    time.sleep(5)
                    while not self.serial_conn.is_open:
                        self.serial_conn.close()
                        self.serial_conn = serial.Serial(self.port, self.baudrate)

                    if self.serial_conn.in_waiting:
                        self.on_connect()

                except Exception:
                    pass

        reconnect_thr = threading.Thread(target=reconnect_procedure)
        reconnect_thr.daemon = True
        reconnect_thr.start()
        
if __name__=='__main__':
    def nothin(rofl=None):
        pass
    n = LoRaTransceiver(nothin,nothin)


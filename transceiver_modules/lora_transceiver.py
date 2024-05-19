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

        self.port = self.config['LoRa_operator_transceiver_port']

        self.on_encoder_data = encoder_data_callback
        self.on_gnss_data = gnss_data_callback
        
        self.on_lora_connect_action = on_lora_connect_action
        self.on_lora_disconnect_action = on_lora_disconnect_action
        self.on_lora_reconnect_action = on_lora_reconnect_action

        self.is_lora_connected = True
        self.baudrate = 9600
        self.serial_interaction_lock = threading.Lock()

        self.serial_conn = None
        self.serial_conn = serial.Serial(self.port, self.baudrate)
        
        self.read_thr = threading.Thread(target=self.recv_thread, args=(10, ))
        self.read_thr.daemon = True
        self.read_thr.start()
        # read_thr.join()



    def send(self, data: str):
        # with self.serial_interaction_lock:
        #     if self.serial_conn:
        #         self.serial_conn.write(data.encode()+b'\r')
        #         print(time.time(),'send', data)
        pass
        # print('lora sent')

        # try this
        with self.serial_interaction_lock:
            if self.serial_conn:
                while self.serial_conn.in_waiting:
                    self.serial_conn.read_until(b'\r\n')
                
                self.serial_conn.write(data.encode()+b'\r')
    

    def on_connect(self,):
        if not self.is_lora_connected:
            # print(time.time(), 'lora connected')
            self.on_lora_reconnect_action()
            
            # self.read_thr = threading.Thread(target=self.recv_thread, args=(10, ))
            # self.read_thr.daemon = True
            # self.read_thr.start()

        else:
            self.on_lora_connect_action()

        self.is_lora_connected = True

    def on_recv(self, data:str):
        parsed_data = data
        # parsed_data = json.loads(data)
        self.on_encoder_data(parsed_data)
        self.on_gnss_data(parsed_data)

    def recv_thread(self, conn_timeout: int):
        start_wait_time = time.time()
        while self.serial_conn.is_open:
            # try:
            with self.serial_interaction_lock:
                if self.serial_conn.in_waiting:
                    read_data = self.serial_conn.read_until(b'\r\n')
                    read_data = read_data[:-2].decode()
                    
                    while self.serial_conn.in_waiting:
                        pass
                    
                    start_wait_time = time.time()
                    self.on_recv(read_data)
                    self.on_connect()
                    # print(abs(time.time() - start_wait_time),'lora recv',read_data)
            
                else:
                    if self.is_lora_connected and abs(time.time() - start_wait_time) >= conn_timeout:
                        print('discon stuff')
                        # self.on_lora_disconnected()

                        self.is_lora_connected = False
                        self.on_lora_disconnect_action()
                        
                        while not self.is_lora_connected:
                            try:
                                # time.sleep(0.1)
                                if self.serial_conn.in_waiting:
                                    self.on_connect()

                            except Exception as e:
                                pass
                            

                        start_wait_time = time.time()
            
            
            # except Exception:
            #     self.on_lora_disconnected()
            #     start_wait_time = time.time()
        print('recv thread ended')

    def on_lora_disconnected(self):
        # if self.is_lora_connected:
            # print(time.time(), 'lora disconnected')
        
        self.is_lora_connected = False
        self.on_lora_disconnect_action()
        
        def reconnect_procedure():
            while not self.is_lora_connected:
                try:
                    time.sleep(0.1)
                    # while not self.serial_conn.is_open:
                    #     self.serial_conn.close()
                    #     self.serial_conn = serial.Serial(self.port, self.baudrate)

                    if self.serial_conn.in_waiting:
                        self.on_connect()

                except Exception as e:
                    pass
 
        # reconnect_thr = threading.Thread(target=reconnect_procedure)
        # reconnect_thr.daemon = True
        # reconnect_thr.start()
        
if __name__=='__main__':
    def nothin(rofl=None):
        pass
    n = LoRaTransceiver(nothin,nothin)


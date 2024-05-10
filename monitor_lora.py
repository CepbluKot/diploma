import json, pickle, threading, time, requests
import paho.mqtt.client as mqtt
import socket, json, serial


class Networking:
    def __init__(self, port) -> None:
        self.is_lora_connected = False
        baudrate = 9600
        self.serial_conn = serial.Serial(port, baudrate)

        read_thr = threading.Thread(target=self.recv_thread, args=(10, ))
        read_thr.start()
        read_thr.join()

    def send(self, data: str):
        self.serial_conn.write(data.encode()+b'\r')

    def on_connect(self,):
            self.is_lora_connected = True
            print('connected 4 real')

    def on_recv(self,data):
        self.is_lora_connected = True
        print('data',data,time.time())

    def recv_thread(self, conn_timeout: int):
        start_wait_time = time.time()
        while self.serial_conn.is_open:
            if self.serial_conn.in_waiting:
                read_data = self.serial_conn.read_until(b'\r\n')
                read_data = read_data[:-2].decode()
                self.on_recv(read_data)
                
                start_wait_time = time.time()
            
            else:
                if time.time() - start_wait_time >= conn_timeout:
                    self.on_lora_dead()
                    start_wait_time = time.time()

    def on_lora_dead(self):
        print('lora dead')
        self.is_lora_connected = False

        while not self.is_lora_connected:
            try:
                time.sleep(5)
                if self.serial_conn.in_waiting:
                    self.on_connect()
            
            except Exception:
                print('conn err')


n = Networking('/dev/ttyUSB0')


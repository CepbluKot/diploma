import json, pickle, threading, time, requests
import paho.mqtt.client as mqtt
import socket, json


class HTTPTransceiver:
    def __init__(self) -> None:
        self.is_http_connected = False
        
    def get_data(self):
        try:
            r = requests.get('http://localhost:5000')

        except requests.exceptions.ConnectionError:
            self.on_http_dead()

    def send_data(self):
        try:
            r = requests.post('http://localhost:5000')

        except requests.exceptions.ConnectionError:
            self.on_http_dead()

    def on_connect(self,):
            self.is_http_connected = True
            print('http connected')

    def on_http_dead(self):
        print('http dead')
        self.is_http_connected = False

        def reconnect_procedure():
            while not self.is_http_connected:
                try:
                    time.sleep(5)
                    r = requests.get('http://localhost:5000')
                    self.on_connect()
                
                except requests.exceptions.ConnectionError:
                    pass
        
        reconnect_thr = threading.Thread(target=reconnect_procedure)
        reconnect_thr.start()
        reconnect_thr.join()

n = HTTPTransceiver()
while 1:
    time.sleep(2)
    n.get_data()

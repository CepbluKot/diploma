import json, pickle, threading, time, requests
import paho.mqtt.client as mqtt
import socket, json


# class Networking:
#     def __init__(self) -> None:
#         self.is_http_connected = False
        

#     def send(self):
#         try:
#             self.is_http_connected = False
#             r = requests.get('http://localhost:5000')

#         except requests.exceptions.ConnectionError:
#             self.on_http_dead()

#     def on_connect(self,):
#             self.is_http_connected = True
#             print('connected 4 real')

#     def on_http_dead(self):
#         print('http dead')
#         self.is_http_connected = False

#         while not self.is_http_connected:
#             try:
#                 time.sleep(5)
#                 r = requests.get('http://localhost:5000')
#                 self.on_connect()
            
#             except requests.exceptions.ConnectionError:
#                 print('conn err')


n = Networking()
while 1:
    time.sleep(2)
    n.send()

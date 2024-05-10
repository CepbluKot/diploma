import json, pickle, threading, time
import paho.mqtt.client as mqtt
import socket, json


class Networking:
    def __init__(self) -> None:
        self.ADDRESS = 'localhost'
        self.port = 8005

        self.is_socket_connected = False
        self.s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        
        try:
            self.s.connect((self.ADDRESS, self.port))
            self.on_connect()
        except:
            self.on_socket_dead()

    def send(self, msgInBytes):
        try:
            self.s.sendall(msgInBytes)
        except:
            self.on_socket_dead()

    def on_connect(self,):
            self.is_socket_connected = True
            print('connected 4 real')

    def on_socket_dead(self):
        print('socket dead')
        self.is_socket_connected = False

        while not self.is_socket_connected:
            try:
                time.sleep(5)
                self.s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
                self.s.connect((self.ADDRESS, self.port))
                self.on_connect()
            
            except Exception as e:
                print('err',e)
    


n = Networking()
while 1:
    time.sleep(2)
    n.send('wewreg'.encode())

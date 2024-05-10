import json, pickle, threading, time
import paho.mqtt.client as mqtt
import socket, json


class SocketSender:
    def __init__(self) -> None:
        def do_nothing():
            pass

        self.config = json.load(open("config.json"))

        self.address = self.config['robot_address']
        self.port = self.config['socket_port']
        
        self.on_socket_disconnect_action = do_nothing
        self.on_socket_reconnect_action = do_nothing

        self.is_socket_connected = False
        self.s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        
        try:
            self.s.connect((self.address, self.port))
            self.on_connect()
        
        except Exception:
            self.on_socket_dead()

    def send(self, data: str):
        try:
            self.s.sendall(data.encode())
        except Exception:
            self.on_socket_dead()

    def on_connect(self,):
            self.is_socket_connected = True
            print('socket connected')

    def on_socket_dead(self):
        print('socket dead')
        self.is_socket_connected = False

        def reconnect_procedure():
            while not self.is_socket_connected:
                try:
                    time.sleep(5)
                    self.s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
                    self.s.connect((self.address, self.port))
                    self.on_connect()
                
                except Exception:
                    pass
        
        reconnect_thr = threading.Thread(target=reconnect_procedure)
        reconnect_thr.start()
        reconnect_thr.join()


n = SocketSender('localhost',8005)
while 1:
    time.sleep(2)
    n.send('wewreg')

import json, pickle, threading, time
import paho.mqtt.client as mqtt
import socket, json


class SocketSender:
    def __init__(self, on_socket_connect_action,on_socket_disconnect_action,on_socket_reconnect_action) -> None:
        
        self.config = json.load(open("config.json"))

        self.address = self.config['robot_address']
        self.port = self.config['socket_port']
        
        self.on_socket_connect_action = on_socket_connect_action
        self.on_socket_disconnect_action = on_socket_disconnect_action
        self.on_socket_reconnect_action = on_socket_reconnect_action

        self.is_socket_connected = False
        self.s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        
        try:
            self.s.connect((self.address, self.port))
            self.on_connect()
        
        except Exception:
            self.on_socket_disconnected()

    def send(self, data: str):
        if self.is_socket_connected:
            def send_action():
                try:
                    self.s.sendall(data.encode())
                except Exception:
                    self.on_socket_disconnected()
            
            send_thr = threading.Thread(target=send_action)
            send_thr.daemon = True
            send_thr.start()

    def on_connect(self,):
            self.is_socket_connected = True
            self.on_socket_connect_action()
            print('socket connected')

    def on_socket_disconnected(self):
        print('socket disconnected')
        self.is_socket_connected = False
        self.on_socket_disconnect_action()
        print('sok on discon action done')

        def reconnect_procedure():
            while not self.is_socket_connected:
                try:
                    time.sleep(0.1)
                    self.s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
                    self.s.connect((self.address, self.port))
                    self.on_connect()
                    self.on_socket_reconnect_action()
                except Exception:
                    pass
        
        reconnect_thr = threading.Thread(target=reconnect_procedure)
        reconnect_thr.daemon = True
        reconnect_thr.start()

if __name__=='__main__':
    n = SocketSender()
    while 1:
        time.sleep(2)
        n.send('wewreg')
        # print('riidn high')

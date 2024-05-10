import socket, json


class Client:
    def __init__(self) -> None:
        f = open('/home/oleg/Documents/ipc_interfaces/config.json')
        config = json.load(f)
        port = 12312
        ip = '127.0.0.1'
        
        self.s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.s.connect((ip, port))
        

    def send(self, msgInBytes):
        self.s.sendall(msgInBytes)

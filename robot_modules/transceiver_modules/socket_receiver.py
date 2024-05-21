import json, threading, time
import socket, json


class SocketReceiver:
    def __init__(self, on_command_recv, config: dict) -> None:
        self.on_command_recv = on_command_recv
        self.config = config
        
        self.s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

        port = self.config["socket_port"]
        address = self.config["robot_address"]
        self.nSymbols = self.config["nSymbols"]

        self.s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.s.bind((address, port))

        self.connect()
        self.server_job()
        

    def connect(self):
        self.s.listen()
        self.conn, addr = self.s.accept()


    def server_job(self):
        try:
            while True:
                received = self.conn.recv(self.nSymbols)
                if received and len(received):
                    self.on_command_recv(received)
                else:
                    self.conn.close()
        except:
            self.connect()
            self.server_job()


if __name__=="__main__":
    def donothing(msg):
        print("lol",msg)
    n = SocketReceiver(donothing)

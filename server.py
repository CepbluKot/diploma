import json, typing, socket


class Server:
    def __init__(self) -> None:
        f = open('/home/oleg/Documents/ipc_interfaces/config.json')
        config = json.load(f)
        port = 12312
        ip = '127.0.0.1'
        self.nSymbols = config['nSymbols']

        self.s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.s.bind((ip, port))

    def connect(self):
        self.s.listen()
        self.conn, addr = self.s.accept()
        print('!!! new conn created')


    def serverJob(self, onReceive: typing.Callable[[], str]):
        try:
            while True:
                received = self.conn.recv(self.nSymbols)
                if received and len(received):
                    onReceive(received)
                else:
                    self.conn.close()
        except:
            print('errorka')
            self.connect()
            self.serverJob(onReceive)

import json, threading
import json, serial
import serial.serialutil


class LoRaTransceiver:
    def __init__(self, command_data_callback, config: dict) -> None:
 
        self.config = config

        self.sender_port = self.config["LoRa_operator_sender_port"]
        self.receiver_port = self.config["LoRa_operator_receiver_port"]

        self.on_command_data = command_data_callback

        self.is_lora_connected = True
        self.baudrate = 9600

        self.serial_sender_conn = None
        
        try:
            self.serial_sender_conn = serial.Serial(self.sender_port, self.baudrate)
        except Exception:
            pass


        self.serial_receiver_conn = None
        
        try:
            self.serial_receiver_conn = serial.Serial(self.receiver_port, self.baudrate)
        except Exception:
            pass

        self.read_thr = threading.Thread(target=self.recv_thread)
        self.read_thr.daemon = True
        self.read_thr.start()

    def send(self, data: str):
        if self.serial_sender_conn:
            while self.serial_sender_conn.in_waiting:
                self.serial_sender_conn.read_until(b"\r\n")
            
            self.serial_sender_conn.write(data.encode()+b"\r")

    def on_recv(self, data:str):
        try:
            parsed_data = json.loads(data)

            if "command" in parsed_data:
                self.on_command_data(parsed_data["command"])     

        except Exception as e:
            print(f"error during receiving data:{e}")

    def recv_thread(self):
        while self.serial_receiver_conn and self.serial_receiver_conn.is_open:
            if self.serial_receiver_conn.in_waiting:
                read_data = self.serial_receiver_conn.read_until(b"\r\n")
                read_data = read_data[:-2].decode()
                
                # while self.serial_receiver_conn.in_waiting:
                #     pass
                
                self.on_recv(read_data)
        
if __name__=="__main__":
    def nothin(rofl=None):
        pass
    n = LoRaTransceiver(nothin,nothin)


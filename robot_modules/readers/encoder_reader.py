from time import sleep
import serial, json, threading
import serial.tools.list_ports


class EncoderReader:
    def __init__(self, on_encoder_data, config: dict) -> None:
        self.on_encoder_data = on_encoder_data

        self.config = config
        self.encoder_port = self.config["encoder_serial_port"]
        self.baudrate = 9600

        self.serial_encoder_conn = None
        
        try:
            self.serial_encoder_conn = serial.Serial(self.encoder_port, self.baudrate)
        except Exception:
            pass

        self.read_thr = threading.Thread(target=self.recv_thr, )
        self.read_thr.daemon = True
        self.read_thr.start()

    def recv_thr(self):
        while self.serial_encoder_conn and self.serial_encoder_conn.is_open:
            if self.serial_encoder_conn.in_waiting:
                read_data = self.serial_encoder_conn.read_until(b"\r\n")
                read_data = read_data[:-2].decode()

                self.on_encoder_data(read_data)


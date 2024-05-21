from time import sleep
import serial, json, threading
import serial.tools.list_ports


class TempHumReader:
    def __init__(self, on_temp_hum_data) -> None:
        self.on_temp_hum_data = on_temp_hum_data

        self.config = json.load(open("config.json"))
        self.temp_hum_port = self.config["temp_hum_serial_port"]
        self.baudrate = 9600

        self.serial_temp_hum_conn = None
        self.serial_temp_hum_conn = serial.Serial(self.temp_hum_port, self.baudrate)

        self.read_thr = threading.Thread(target=self.recv_thr, args=(10, ))
        self.read_thr.daemon = True
        self.read_thr.start()

    def recv_thr(self):
        while self.serial_temp_hum_conn.is_open:
            if self.serial_temp_hum_conn.in_waiting:
                read_data = self.serial_temp_hum_conn.read_until(b"\r\n")
                read_data = read_data[:-2].decode()

                self.on_temp_hum_data(read_data)


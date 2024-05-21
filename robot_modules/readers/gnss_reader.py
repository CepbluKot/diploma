import serial, json, threading
import serial.tools.list_ports
import serial, threading
import serial.tools.list_ports
import pynmea2
from data_formats.gnss_data import GNSSData


class GNSSReader:
    def __init__(self, on_gnss_data, config: dict) -> None:
        self.on_gnss_data = on_gnss_data

        self.config = config
        self.gnss_port = self.config["gnss_serial_port"]
        self.baudrate = 9600

        self.serial_gnss_conn = None

        try:
            self.serial_gnss_conn = serial.Serial(self.gnss_port, self.baudrate)
        except Exception:
            pass

        self.global_gnss_data = GNSSData()

        self.read_thr = threading.Thread(target=self.recv_job, args=(10, ))
        self.read_thr.daemon = True
        self.read_thr.start()

    def recv_job(self):
        while self.serial_gnss_conn and self.serial_gnss_conn.is_open and self.read_thr.is_alive():
            parsed = pynmea2.parse(self.serial_gnss_conn.readline().decode("utf-8"))
            
            if isinstance(parsed, pynmea2.types.talker.VTG):
                self.global_gnss_data.true_track = parsed.true_track
                self.global_gnss_data.spd_over_grnd_kmph = (parsed.spd_over_grnd_kmph)

            if isinstance(parsed, pynmea2.types.talker.GLL):
                self.global_gnss_data.lat = float(parsed.lat) / 100
                self.global_gnss_data.lat_dir = parsed.lat_dir
                self.global_gnss_data.lon = float(parsed.lon) / 100
                self.global_gnss_data.lon_dir = parsed.lon_dir

            if self.global_gnss_data.lat > 0 and self.global_gnss_data.lon > 0:
                self.on_gnss_data(self.global_gnss_data.json())

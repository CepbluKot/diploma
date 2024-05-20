import serial, json, threading
import serial.tools.list_ports
from time import sleep
import pydantic
import serial, threading
import serial.tools.list_ports
import pynmea2


class GPSData(pydantic.BaseModel):
    lat: float = -1
    lat_dir: str = None
    lon: float = -1
    lon_dir: str = None
    spd_over_grnd_kmph: float = -1
    true_track: float = -1
    altitude: float = -1


class GNSSReader:
    def __init__(self, on_new_data) -> None:
        self.on_new_data = on_new_data

        self.global_gps_data = GPSData()

        self.config = json.load(open('config.json'))
        self.gnss_port = self.config['gnss_serial_port']
        self.baudrate = 9600

        self.serial_gnss_conn = None
        self.serial_gnss_conn = serial.Serial(self.gnss_port, self.baudrate)

        self.read_thr = threading.Thread(target=self.recv_thr, args=(10, ))
        self.read_thr.daemon = True
        self.read_thr.start()

    def recv_thr(self):
        while self.serial_gnss_conn.is_open:
            parsed = pynmea2.parse(self.serial_gnss_conn.readline().decode('utf-8'))

            if isinstance(parsed, pynmea2.types.talker.VTG):
                self.global_gps_data.true_track = parsed.true_track
                self.global_gps_data.spd_over_grnd_kmph = (parsed.spd_over_grnd_kmph)

            if isinstance(parsed, pynmea2.types.talker.GLL):
                self.global_gps_data.lat = float(parsed.lat) / 100
                self.global_gps_data.lat_dir = parsed.lat_dir
                self.global_gps_data.lon = float(parsed.lon) / 100
                self.global_gps_data.lon_dir = parsed.lon_dir

            if self.global_gps_data.lat > 0 and self.global_gps_data.lon > 0:
                self.on_new_data(self.global_gps_data)

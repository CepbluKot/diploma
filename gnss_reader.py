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


global_gps_data = GPSData()


def search_for_ports():
    ports = list(serial.tools.list_ports.comports())
    return ports

def run(gui_upd_callback):
    # print('available ports')
    # for index, port in enumerate(search_for_ports()):
    #     print('[{}] {}'.format(index, port.description))

    # port = search_for_ports()[0].device
    port = "/dev/ttyUSB0"
    baudrate = 9600
    serial_conn = serial.Serial(port, baudrate)


    while True:
        try:
            parsed = pynmea2.parse(serial_conn.readline().decode("utf-8"))

            # if isinstance(parsed, pynmea2.types.talker.RMC):
            #     global_gps_data.lat = parsed.lat
            #     global_gps_data.lon = parsed.lon
            #     # global_gps_data.spd_over_grnd_kmph = parsed.spd_over_grnd
            #     # global_gps_data.true_track = parsed.true_course
            #     global_gps_data.lat_dir = parsed.lat_dir
            #     global_gps_data.lon_dir = parsed.lon_dir


            # if isinstance(parsed, pynmea2.types.talker.GGA):
            #     global_gps_data.lat = parsed.lat
            #     global_gps_data.lon = parsed.lon
            #     global_gps_data.lat_dir = parsed.lat_dir
            #     global_gps_data.lon_dir = parsed.lon_dir
            #     global_gps_data.altitude = parsed.altitude


            if isinstance(parsed, pynmea2.types.talker.VTG):
                global_gps_data.true_track = parsed.true_track
                global_gps_data.spd_over_grnd_kmph = (parsed.spd_over_grnd_kmph)

            if isinstance(parsed, pynmea2.types.talker.GLL):
                global_gps_data.lat = float(parsed.lat) / 100
                global_gps_data.lat_dir = parsed.lat_dir
                global_gps_data.lon = float(parsed.lon) / 100
                global_gps_data.lon_dir = parsed.lon_dir
   
            # if global_gps_data.lat:
            #     global_gps_data.lat = global_gps_data.lat / 100
            
            # if global_gps_data.lon:
            #     global_gps_data.lon = global_gps_data.lon / 100
            
            if global_gps_data.lat > 0 and global_gps_data.lon > 0:
                gui_upd_callback(global_gps_data.lat, global_gps_data.lon)

        except Exception as e:
            print(e)


if __name__ == "__main__":
    def nothin():
        pass
    
    run(nothin)

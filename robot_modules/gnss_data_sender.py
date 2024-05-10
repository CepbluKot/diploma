import pydantic
import serial
import json
import time
import serial.tools.list_ports
import pynmea2
import paho.mqtt.client as mqtt


config = json.load(open("config.json"))
GNSS_PORT_NAME = config["gnss_serial_port"]
ADDRESS = config["robot_address"]
MQTT_PORT = config["MQTT_port"]
MQTT_TOPIC_STR = config["gnss_topic_str_format"]


def on_connect(client, userdata, flags, rc):
    print("Connected with result code " + str(rc))

send_status = False
def on_publish(client, userdata, mid):
    global send_status
    if not send_status:
        print("gnss data being sended")
        send_status = True

client = mqtt.Client()
client.on_connect = on_connect
client.on_publish = on_publish
client.connect(ADDRESS, MQTT_PORT, 60)
client.loop_start()


class GPSData(pydantic.BaseModel):
    lat: float = -1
    lat_dir: str = None
    lon: float = -1
    lon_dir: str = None
    spd_over_grnd_kmph: float = -1
    true_track: float = -1
    altitude: float = -1


global_gnss_data = GPSData()


def search_for_ports():
    ports = list(serial.tools.list_ports.comports())
    return ports

def run():
    port = GNSS_PORT_NAME
    baudrate = 9600
    serial_conn = serial.Serial(port, baudrate)


    while serial_conn.is_open:
        try:
            parsed = pynmea2.parse(serial_conn.readline().decode("utf-8"))

            if isinstance(parsed, pynmea2.types.talker.VTG):
                global_gnss_data.true_track = parsed.true_track
                global_gnss_data.spd_over_grnd_kmph = parsed.spd_over_grnd_kmph

            if isinstance(parsed, pynmea2.types.talker.GLL):
                global_gnss_data.lat = parsed.lat
                global_gnss_data.lat_dir = parsed.lat_dir
                global_gnss_data.lon = parsed.lon
                global_gnss_data.lon_dir = parsed.lon_dir
   
            client.publish(payload=global_gnss_data.model_dump_json(), topic=MQTT_TOPIC_STR)
            time.sleep(1)
            
        except Exception:
            break


def test_run():
    try:
        import random
        while 1:
            global_gnss_data.lat = 56.256340
            global_gnss_data.lon = 38.466686
            global_gnss_data.spd_over_grnd_kmph = random.randint(1,6)

            client.publish(payload=global_gnss_data.model_dump_json(), topic=MQTT_TOPIC_STR)
            time.sleep(1)

    except Exception:
        pass

if __name__ == "__main__":
    # run()
    test_run()

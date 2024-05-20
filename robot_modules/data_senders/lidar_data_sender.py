from rplidar import RPLidar
import paho.mqtt.client as mqtt
import pickle
import json


config = json.load(open('config.json'))
LIDAR_PORT_NAME = config['lidar_serial_port']
ADDRESS = config['robot_address']
MQTT_PORT = config['MQTT_port']
MQTT_TOPIC_PICKLE = config['lidar_topic_pickle_format']
MQTT_TOPIC_STR = config['lidar_topic_str_format']


def on_connect(client, userdata, flags, rc):
    print('Connected with result code ' + str(rc))

send_status = False
def on_publish(client, userdata, mid):
    global send_status
    if not send_status:
        print('lidar data being sended')
        send_status = True

client = mqtt.Client()
client.on_connect = on_connect
client.on_publish = on_publish
client.connect(ADDRESS, MQTT_PORT, 60)
client.loop_start()


def run():
    '''Main function'''
    lidar = RPLidar(LIDAR_PORT_NAME)

    try:
        for scan in lidar.iter_scans():
            client.publish(payload=pickle.dumps(scan), topic=MQTT_TOPIC_PICKLE)
    except Exception:
        run()

if __name__ == '__main__':
    run()

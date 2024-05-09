import freenect
import paho.mqtt.client as mqtt
import pickle
import json


config = json.load(open("config.json"))
ADDRESS = config["robot_address"]
MQTT_PORT = config["MQTT_port"]

MQTT_DEPTH_CAM_TOPIC_PICKLE = config["depth_cam_topic_pickle_format"]
MQTT_DEPTH_CAM_TOPIC_STR = config["depth_cam_topic_str_format"]
MQTT_RGB_CAM_TOPIC_PICKLE = config["rgb_cam_topic_pickle_format"]
MQTT_RGB_CAM_TOPIC_STR = config["rgb_cam_topic_str_format"]

DEPTH_CAM_IND = 0


def on_connect(client, userdata, flags, rc):
    print("Connected with result code " + str(rc))


send_status = False
def on_publish(client, userdata, mid):
    global send_status
    if not send_status:
        print("depth cam data being sended")
        send_status = True

client = mqtt.Client()
client.on_connect = on_connect
client.on_publish = on_publish
client.connect(ADDRESS, MQTT_PORT, 60)
client.loop_start()



def run():
    while True:
        if freenect.sync_get_depth(DEPTH_CAM_IND) and freenect.sync_get_video(DEPTH_CAM_IND):
            depth_mat = freenect.sync_get_depth(DEPTH_CAM_IND)[0]
            video = freenect.sync_get_video(DEPTH_CAM_IND)[0]

            if depth_mat.size and video.size:
                client.publish(payload=pickle.dumps(depth_mat), topic=MQTT_DEPTH_CAM_TOPIC_PICKLE)
                client.publish(payload=pickle.dumps(video), topic=MQTT_RGB_CAM_TOPIC_PICKLE)


if __name__=='__main__':
    run()

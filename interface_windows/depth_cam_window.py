import numpy as np
import paho.mqtt.client as mqtt
import json
import numpy as np
import threading
import cv2
import frame_convert2
import pickle


config = json.load(open("config.json"))
ADDRESS = config["robot_address"]
MQTT_PORT = config["MQTT_port"]

MQTT_DEPTH_CAM_TOPIC_PICKLE = config["depth_cam_topic_pickle_format"]
# MQTT_DEPTH_CAM_TOPIC_STR = config["depth_cam_topic_str_format"]
MQTT_RGB_CAM_TOPIC_PICKLE = config["rgb_cam_topic_pickle_format"]
# MQTT_RGB_CAM_TOPIC_STR = config["rgb_cam_topic_str_format"]


depth_msg = []
rgb_msg = []


def on_connect_depth(client: mqtt.Client, userdata, flags, rc):
    print("Connected with result code " + str(rc))
    client.subscribe(topic=MQTT_DEPTH_CAM_TOPIC_PICKLE)
    client.subscribe(topic=MQTT_RGB_CAM_TOPIC_PICKLE)


def on_message(client, userdata, msg: mqtt.MQTTMessage):
    global depth_msg
    global rgb_msg

    if msg.topic == MQTT_DEPTH_CAM_TOPIC_PICKLE:
        if msg.payload:
            depth_msg =  pickle.loads(msg.payload)

    if msg.topic == MQTT_RGB_CAM_TOPIC_PICKLE:
        if msg.payload:
            rgb_msg =  pickle.loads(msg.payload)



client = mqtt.Client()
client.on_connect = on_connect_depth
client.on_message = on_message
client.connect(ADDRESS, MQTT_PORT, 60)


def run():
    depth=np.zeros((480,640))
    rgb = np.zeros((480,640,3))
    while 1:
        if len(depth_msg) and len(rgb_msg):
            try:
                depth = frame_convert2.pretty_depth_cv(depth_msg)
                rgb = frame_convert2.video_cv(rgb_msg)

            except:
                pass
            
        cv2.imshow('Depth', depth)
        cv2.imshow('rgb', rgb)

        cv2.waitKey(70)



def launch():
    t1 = threading.Thread(target=client.loop_forever)
    t1.start()
    run()
    t1.join()

if __name__=='__main__':
    launch()

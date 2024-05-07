import freenect
import paho.mqtt.client as mqtt
import time, random
import json
import numpy as np
import pickle


PORT_NAME = '/dev/ttyUSB0'


def on_connect(client, userdata, flags, rc):
    print("Connected with result code " + str(rc))


i=0
def on_publish(client, userdata, mid):
    global i
    print("sent data",i)
    i+=1


client = mqtt.Client()
client.on_connect = on_connect
client.on_publish = on_publish
client.connect("localhost", 1883, 60)
client.loop_start()
ind = 0


def run():
    while 1:
        if freenect.sync_get_depth(ind) and freenect.sync_get_video(ind):
            depth_mat = freenect.sync_get_depth(ind)[0]
            video = freenect.sync_get_video(ind)[0]

            if depth_mat.size:
                client.publish(payload=pickle.dumps(depth_mat), topic="data/depth_cam")
                client.publish(payload=pickle.dumps(video), topic="data/rgb_cam")

if __name__=='__main__':
    run()

import matplotlib.pyplot as plt
import numpy as np
import matplotlib.animation as animation
import paho.mqtt.client as mqtt
import json
import matplotlib.pyplot as plt
import numpy as np
import matplotlib.animation as animation
import threading
import cv2
import frame_convert2
import pickle




class LastMsgContainer:
    def __init__(self) -> None:
        self.lock = threading.Lock()
        self.value = []

    def set(self, new_val):
        self.lock.acquire()
        self.value = new_val
        self.lock.release()


    def get(self):
        self.lock.acquire()
        val_to_return = self.value
        self.lock.release()

        return val_to_return


depth_msg = LastMsgContainer()
rgb_msg = LastMsgContainer()

def on_connect_depth(client: mqtt.Client, userdata, flags, rc):
    print("Connected with result code " + str(rc))
    client.subscribe(topic="data/depth_cam")
    client.subscribe(topic="data/rgb_cam")


def on_message(client, userdata, msg: mqtt.MQTTMessage):
    global depth_msg
    global rgb_msg

    if msg.topic == 'data/depth_cam':
        if msg.payload:
            print('gotcha')
            depth_msg.set( pickle.loads(msg.payload))

    if msg.topic == 'data/rgb_cam':
        if msg.payload:
            print('gotcha')
            rgb_msg.set( pickle.loads(msg.payload))



client = mqtt.Client()
client.on_connect = on_connect_depth
client.on_message = on_message
client.connect("localhost", 1883, 60)


def run():
    while 1:
        if len(depth_msg.get()):
            depth = frame_convert2.pretty_depth_cv(depth_msg.get())
            rgb=frame_convert2.video_cv(rgb_msg.get())
            cv2.imshow('Depth', depth)
            cv2.imshow('rgb', rgb)

        if cv2.waitKey(10) == 27:
            break


def launch():
    t1 = threading.Thread(target=client.loop_forever)
    t1.start()
    run()
    t1.join()

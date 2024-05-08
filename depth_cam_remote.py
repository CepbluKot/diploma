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




# class LastMsgContainer:
#     def __init__(self) -> None:
#         self.lock = threading.Lock()
#         self.value = []

#     def set(self, new_val):
#         self.lock.acquire()
#         self.value = new_val
#         self.lock.release()


#     def get(self):
#         self.lock.acquire()
#         val_to_return = self.value
#         self.lock.release()

#         return val_to_return


depth_msg = []
rgb_msg = []

def on_connect_depth(client: mqtt.Client, userdata, flags, rc):
    print("Connected with result code " + str(rc))
    client.subscribe(topic="data/depth_cam")
    client.subscribe(topic="data/rgb_cam")


def on_message(client, userdata, msg: mqtt.MQTTMessage):
    global depth_msg
    global rgb_msg

    if msg.topic == 'data/depth_cam':
        if msg.payload:
            depth_msg =  pickle.loads(msg.payload)

    if msg.topic == 'data/rgb_cam':
        if msg.payload:
            rgb_msg =  pickle.loads(msg.payload)



client = mqtt.Client()
client.on_connect = on_connect_depth
client.on_message = on_message
client.connect("localhost", 1883, 60)


def run():
    depth=np.zeros((480,640))
    rgb = np.zeros((480,640,3))
    while 1:
        if len(depth_msg):
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

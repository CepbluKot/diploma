#!/usr/bin/env python3
'''Records scans to a given file in the form of numpy array.
Usage example:

$ ./record_scans.py out.npy'''
import sys
import numpy as np
from rplidar import RPLidar
import paho.mqtt.client as mqtt
import time, random
import json

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


def run():
    '''Main function'''
    lidar = RPLidar(PORT_NAME)

    
    try:
        for scan in lidar.iter_scans():
            client.publish(payload=json.dumps(scan), topic="/")
            
        
    except KeyboardInterrupt:
        print('Stoping.')

    lidar.stop()
    lidar.disconnect()

if __name__ == '__main__':
    run()

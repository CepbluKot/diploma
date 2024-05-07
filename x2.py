#!/usr/bin/env python3
'''Animates distances and measurment quality'''

import matplotlib.pyplot as plt
import numpy as np
import matplotlib.animation as animation
import paho.mqtt.client as mqtt
import json





def on_connect(client: mqtt.Client, userdata, flags, rc):
    print("Connected with result code " + str(rc))
    client.subscribe(topic="#")


def on_message(client, userdata, msg: mqtt.MQTTMessage):
    if msg.topic == '/':
        if msg.payload:
            res = json.loads(msg.payload)
            print(res  , '\n\n')
    




client = mqtt.Client()
client.on_connect = on_connect
client.on_message = on_message
client.connect("localhost", 1883, 60)
client.loop_start()


DMAX = 4000
IMIN = 0
IMAX = 50

# def update_line(num, iterator, line):

#     # scan = next(iterator)
#     # offsets = np.array([(np.radians(meas[1]), meas[2]) for meas in scan])
#     # line.set_offsets(offsets)
#     # intens = np.array([meas[0] for meas in scan])
#     # line.set_array(intens)
#     return line,

# def run():
#     fig = plt.figure()
#     ax = plt.subplot(111, projection='polar')
#     line = ax.scatter([0, 0], [0, 0], s=5, c=[IMIN, IMAX],
#                            cmap=plt.cm.Greys_r, lw=0)
#     ax.set_rmax(DMAX)
#     ax.grid(True)

#     ani = animation.FuncAnimation(fig, update_line,
#         fargs=(line), interval=50)
#     plt.show()

# if __name__ == '__main__':
#     run()
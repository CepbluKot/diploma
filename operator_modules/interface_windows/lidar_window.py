import matplotlib.pyplot as plt
import numpy as np
import matplotlib.animation as animation
import paho.mqtt.client as mqtt
import json
import matplotlib.pyplot as plt
import numpy as np
import matplotlib.animation as animation
import threading
import pickle


config = json.load(open("config.json"))
ADDRESS = config["robot_address"]
MQTT_PORT = config["MQTT_port"]

MQTT_LIDAR_TOPIC_PICKLE = config["lidar_topic_pickle_format"]
# MQTT_LIDAR_TOPIC_STR = config["lidar_topic_str_format"]


last_msg = []

def on_connect(client: mqtt.Client, userdata, flags, rc):
    print("Connected with result code " + str(rc))
    client.subscribe(topic=MQTT_LIDAR_TOPIC_PICKLE)


def on_message(client, userdata, msg: mqtt.MQTTMessage):
    global last_msg

    if msg.topic == MQTT_LIDAR_TOPIC_PICKLE:
        if msg.payload:
            # print("gotcha")
            last_msg = pickle.loads(msg.payload)

client = mqtt.Client()
client.on_connect = on_connect
client.on_message = on_message
client.connect(ADDRESS, MQTT_PORT, 60)



def update_line(num, iterator, line):
    scan = last_msg

    if scan:
        offsets = np.array([(np.radians(meas[1]), meas[2]) for meas in scan])
        line.set_offsets(offsets)
        intens = np.array([meas[0] for meas in scan])
        line.set_array(intens)
    return line

DMAX = 4000
IMIN = 0
IMAX = 50

def run():
    fig = plt.figure()
    fig.canvas.manager.set_window_title("LiDar")
    ax = plt.subplot(111, projection="polar")
    line = ax.scatter([0, 0], [0, 0], s=5, c=[IMIN, IMAX],
                           cmap=plt.cm.Greys_r, lw=0)
    ax.set_rmax(DMAX)
    ax.grid(True)
    iterator=None
    ani = animation.FuncAnimation(fig, update_line,
        fargs=( iterator, line), interval=50)
    
    plt.show()

def launch():
    t1 = threading.Thread(target=client.loop_forever)
    t1.start()
    run()
    t1.join()

if __name__=="__main__":
    launch()

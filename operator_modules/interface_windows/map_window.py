import tkinter, threading, json
import tkintermapview
import paho.mqtt.client as mqtt


config = json.load(open("config.json"))
ADDRESS = config["robot_address"]
MQTT_PORT = config["MQTT_port"]
MQTT_GNSS_TOPIC_STR = config["gnss_topic_str_format"]


map_widget = None
old_marker = None

def on_connect(client: mqtt.Client, userdata, flags, rc):
    print("Connected with result code " + str(rc))
    client.subscribe(topic=MQTT_GNSS_TOPIC_STR)


def on_message(client, userdata, msg: mqtt.MQTTMessage):
    global old_marker
    global map_widget
    if msg.topic == MQTT_GNSS_TOPIC_STR:
        if msg.payload:
            if old_marker:
                old_marker.delete()
            parsed = json.loads(msg.payload)

            if "lat" in parsed and "lon" in parsed:
                if map_widget:
                    old_marker = map_widget.set_position(parsed["lat"],parsed["lon"],marker=True)


def launch():
    global map_widget

    client = mqtt.Client()
    client.on_connect = on_connect
    client.on_message = on_message
    client.connect(ADDRESS, MQTT_PORT, 60)


    root_tk = tkinter.Tk()
    root_tk.geometry(f"{500}x{500}")
    root_tk.title("map")
    old_marker = None


    map_widget = tkintermapview.TkinterMapView(root_tk, width=500, height=50, corner_radius=0)
    map_widget.pack(fill="both", expand=True)
    map_widget.set_tile_server("https://mt0.google.com/vt/lyrs=s&hl=en&x={x}&y={y}&z={z}&s=Ga", max_zoom=22)  # google satellite
    map_widget.set_position(56.255518, 38.467219)

    point_upd_thr = threading.Thread(target=client.loop_forever)
    point_upd_thr.start()  
    # root_tk.mainloop()
    point_upd_thr.join()


if __name__=="__main__":
    launch()

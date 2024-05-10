import json, pickle, threading, time
import paho.mqtt.client as mqtt


class Networking:
    def __init__(self) -> None:
        config = json.load(open("config.json"))
        self.ADDRESS = 'localhost'
        self.MQTT_PORT = 1883
        self.MQTT_LIDAR_TOPIC_PICKLE = 'data/gnss_str'

        
        
        self.is_mqtt_connected = False
        self.mqtt_client = mqtt.Client()
        self.mqtt_client.on_connect = self.on_connect
        self.mqtt_client.on_disconnect = self.on_mqtt_dead
        self.mqtt_client.connect(self.ADDRESS, self.MQTT_PORT, 60)

        self.mqtt_thread = threading.Thread(target=self.mqtt_client.loop_forever)
        self.mqtt_thread.start()
        self.mqtt_thread.join()


    def on_connect(self, client: mqtt.Client, userdata, flags, rc):
            print("Connected with result code " + str(rc))
            # client.subscribe(topic=self.MQTT_LIDAR_TOPIC_PICKLE)
            self.is_mqtt_connected = True
            print('connected 4 real')

    def on_mqtt_dead(self,client: mqtt.Client, userdata,  rc):
        print('mqtt dead')
        self.is_mqtt_connected = False

        while not self.is_mqtt_connected:
            try:
                time.sleep(5)

                client.on_connect = self.on_connect
                client.on_disconnect = self.on_mqtt_dead
                res= client.connect(self.ADDRESS, self.MQTT_PORT, 60)
                if res == mqtt.MQTT_ERR_SUCCESS:
                    self.is_mqtt_connected = True
                
                print('tryin to reconn')
                
                print('res',res)
            except:
                pass


n = Networking()

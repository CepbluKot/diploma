import json, pickle, threading, time
import paho.mqtt.client as mqtt


class MQTTReceiver:
    def __init__(self, address, port) -> None:
        self.address = address
        self.port = port

        
        self.is_mqtt_connected = False

        self.mqtt_client = mqtt.Client()
        self.mqtt_client.on_connect = self.on_connect
        self.mqtt_client.on_disconnect = self.on_mqtt_dead
        self.mqtt_client.connect(self.address, self.port, 60)

        self.mqtt_thread = threading.Thread(target=self.mqtt_client.loop_forever)
        self.mqtt_thread.start()
        self.mqtt_thread.join()


    def on_connect(self, client: mqtt.Client, userdata, flags, rc):
            # client.subscribe(topic=self.MQTT_LIDAR_TOPIC_PICKLE)
            self.is_mqtt_connected = True
            print('mqtt connected')

    def on_mqtt_dead(self,client: mqtt.Client, userdata,  rc): # этой шняги достаточно
        print('mqtt dead') # проста добавим сюда гуи логики
        self.is_mqtt_connected = False

        def reconnect_procedure():
            while not self.is_mqtt_connected:
                try:
                    time.sleep(5)

                    client.on_connect = self.on_connect
                    client.on_disconnect = self.on_mqtt_dead
                    res= client.connect(self.address, self.port, 60)
                    if res == mqtt.MQTT_ERR_SUCCESS:
                        self.is_mqtt_connected = True
                    
                    print('tryin to reconn')
                    
                    print('res',res)
                except:
                    pass
        
        reconnect_thr = threading.Thread(target=reconnect_procedure)
        reconnect_thr.start()
        reconnect_thr.join()

n = MQTTReceiver()

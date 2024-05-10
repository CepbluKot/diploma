import json, pickle, threading, time
import paho.mqtt.client as mqtt


class MQTTReceiver:
    def __init__(self,\
                 lidar_topic_callback,\
                 depth_cam_topic_callback,\
                 rgb_cam_topic_callback,\
                 encoder_topic_callback,\
                 gnss_topic_callback) -> None:
        def do_nothing():
            pass

        self.on_lidar_msg = lidar_topic_callback
        self.on_depth_cam_msg = depth_cam_topic_callback
        self.on_rgb_cam_msg = rgb_cam_topic_callback
        self.on_encoder_msg = encoder_topic_callback
        self.on_gnss_msg = gnss_topic_callback

        self.on_mqtt_disconnect_action = do_nothing
        self.on_mqtt_reconnect_action = do_nothing

        self.config = json.load(open("config.json"))

        self.address = self.config['robot_address']
        self.port = self.config['MQTT_port']


        self.is_mqtt_connected = False

        self.mqtt_client = mqtt.Client()
        self.mqtt_client.on_connect = self.on_connect
        self.mqtt_client.on_message = self.on_message
        self.mqtt_client.on_disconnect = self.on_disconnect
        
        try:
            self.mqtt_client.connect(self.address, self.port, 60)
        except ConnectionRefusedError:
            self.on_disconnect(self.mqtt_client)
    
        self.mqtt_thread = threading.Thread(target=self.mqtt_client.loop_forever)
        # self.mqtt_thread.daemon = True
        self.mqtt_thread.start()
        self.mqtt_thread.join()
        
    def on_connect(self, client: mqtt.Client, userdata, flags, rc):
        client.subscribe(topic=self.config['lidar_topic_pickle_format'])
        client.subscribe(topic=self.config['depth_cam_topic_pickle_format'])
        client.subscribe(topic=self.config['rgb_cam_topic_pickle_format'])
        client.subscribe(topic=self.config['encoder_topic_str_format'])
        client.subscribe(topic=self.config['gnss_topic_str_format'])
        
        self.is_mqtt_connected = True
        print('mqtt connected')

    def on_message(self, client, userdata, msg: mqtt.MQTTMessage):
        if msg.topic == self.config['lidar_topic_pickle_format']:
            if msg.payload:
                lidar_msg =  pickle.loads(msg.payload)
                self.on_lidar_msg(lidar_msg)

        if msg.topic == self.config['depth_cam_topic_pickle_format']:
            if msg.payload:
                depth_cam_msg =  pickle.loads(msg.payload)
                self.on_depth_cam_msg(depth_cam_msg)

        if msg.topic == self.config['rgb_cam_topic_pickle_format']:
            if msg.payload:
                rgb_cam_msg =  pickle.loads(msg.payload)
                self.on_rgb_cam_msg(rgb_cam_msg)

        if msg.topic == self.config['encoder_topic_str_format']:
            if msg.payload:
                encoder_msg =  json.loads(msg.payload)
                self.on_encoder_msg(encoder_msg)

        if msg.topic == self.config['gnss_topic_str_format']:
            if msg.payload:
                gnss_msg =  json.loads(msg.payload)
                self.on_gnss_msg(gnss_msg)

    def on_disconnect(self,client: mqtt.Client, userdata=None,  rc=None):
        print('mqtt disconnected')
        self.is_mqtt_connected = False

        self.on_mqtt_disconnect_action()

        def reconnect_procedure():
            while not self.is_mqtt_connected:
                try:
                    time.sleep(1)

                    client.on_connect = self.on_connect
                    client.on_disconnect = self.on_disconnect
                    res= client.connect(self.address, self.port, 60)
                    if res == mqtt.MQTT_ERR_SUCCESS:
                        self.is_mqtt_connected = True
                        self.on_mqtt_reconnect_action()

                except Exception:
                    pass
        
        reconnect_thr = threading.Thread(target=reconnect_procedure)
        reconnect_thr.daemon = True
        reconnect_thr.start()


# def do_nothing():
#     pass

# n = MQTTReceiver(do_nothing,do_nothing,do_nothing,do_nothing,do_nothing)

import json, pickle, threading, time
import paho.mqtt.client as mqtt


class MQTTSender:
    def __init__(self, config: dict) -> None:

        self.config = config
                
        address = self.config["robot_address"]
        port = self.config["MQTT_port"]

        self.lidar_topic_pickle = self.config["lidar_topic_pickle_format"]
        self.depth_cam_topic_pickle = self.config["depth_cam_topic_pickle_format"]
        self.rgb_cam_topic_pickle = self.config["rgb_cam_topic_pickle_format"]
        self.gnss_topic_str = self.config["gnss_topic_str_format"]
        self.encoder_topic_str = self.config["encoder_topic_str_format"]
        self.temp_hum_topic_str = self.config["temp_hum_topic_str_format"]

        self.mqtt_client = mqtt.Client()
        self.mqtt_client.connect(address, port, 60)

        self.mqtt_thread = threading.Thread(target=self.mqtt_client.loop_start)
        self.mqtt_thread.daemon  = True
        self.mqtt_thread.start()


    def send_lidar_data(self, data):
        self.mqtt_client.publish(payload=pickle.dumps(data), topic=self.lidar_topic_pickle)
        
    def send_depth_cam_data(self, data):
        self.mqtt_client.publish(payload=pickle.dumps(data), topic=self.depth_cam_topic_pickle)

    def send_rgb_cam_data(self, data):
        self.mqtt_client.publish(payload=pickle.dumps(data), topic=self.rgb_cam_topic_pickle)

    def send_gnss_data(self, data: str):
        self.mqtt_client.publish(payload=data, topic=self.gnss_topic_str)

    def send_encoder_data(self, data: str):
        self.mqtt_client.publish(payload=data, topic=self.encoder_topic_str)

    def send_temp_hum_data(self, data: str):
        self.mqtt_client.publish(payload=data, topic=self.temp_hum_topic_str)

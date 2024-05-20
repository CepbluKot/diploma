import json, pickle, threading, time
import paho.mqtt.client as mqtt


class MQTTSender:
    def __init__(self) -> None:
        self.config = json.load(open('config.json'))
                
        address = self.config['robot_address']
        port = self.config['MQTT_port']

        self.lidar_topic_pickle = self.config['lidar_topic_pickle_format']
        self.depth_cam_topic_pickle = self.config['depth_cam_topic_pickle_format']
        self.rgb_cam_topic_pickle = self.config['rgb_cam_topic_pickle_format']
        self.gnss_topic_str = self.config['gnss_topic_str_format']
        self.encoder_topic_str = self.config['encoder_topic_str_format']
        
        self.client = mqtt.Client()
        self.client.connect(address, port, 60)
        self.client.loop_start()


    def send_lidar_data(self, data):
        self.client.publish(payload=pickle.dumps(data), topic=self.lidar_topic_pickle)
        
    def send_depth_cam_data(self, data):
        self.client.publish(payload=pickle.dumps(data), topic=self.depth_cam_topic_pickle)

    def send_rgb_cam_data(self, data):
        self.client.publish(payload=pickle.dumps(data), topic=self.rgb_cam_topic_pickle)

    def send_gnss_data(self, data: str):
        self.client.publish(payload=data, topic=self.gnss_topic_str)

    def send_encoder_data(self, data: str):
        self.client.publish(payload=data, topic=self.encoder_topic_str)

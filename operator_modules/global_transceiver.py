from socket_sender import SocketSender
import paho.mqtt.client as mqtt
import threading
import json
from lora_transceiver import LoRaTransceiver
from mqtt_receiver import MQTTReceiver


class GlobalTransceiver:
    def __init__(self,
                 socket_sender: SocketSender,\
                 lora_transceiver: LoRaTransceiver,\
                 mqtt_transceiver: MQTTReceiver,\
                 encoder_data_callback,\
                 gnss_data_callback
                 ) -> None:
        
        self.socket_sender = socket_sender
        self.lora_transceiver = lora_transceiver
        self.mqtt_transceiver = mqtt_transceiver

        self.encoder_data_callback = encoder_data_callback
        self.gnss_data_callback = gnss_data_callback
       

        self.lora_transceiver.on_lora_disconnect_action = self.lora_disconnect_action
        self.lora_transceiver.on_lora_reconnect_action = self.lora_reconnect_action
        
        self.mqtt_transceiver.on_mqtt_disconnect_action = self.mqtt_disconnect_action
        self.mqtt_transceiver.on_mqtt_reconnect_action = self.mqtt_reconnect_action
        
        self.socket_sender.on_socket_disconnect_action = self.socket_disconnect_action
        self.socket_sender.on_socket_reconnect_action = self.socket_reconnect_action
        
        self.sender = socket_sender

    def set_transceiver_config(self, internet_available: bool):
        def do_nothing():
            pass

        if internet_available:
            self.lora_transceiver.on_encoder_data = do_nothing
            self.lora_transceiver.on_gnss_data = do_nothing

            self.mqtt_transceiver.on_encoder_msg = self.encoder_data_callback
            self.mqtt_transceiver.on_gnss_msg = self.gnss_data_callback

        else:
            self.lora_transceiver.on_encoder_data = self.encoder_data_callback
            self.lora_transceiver.on_gnss_data = self.gnss_data_callback

            self.mqtt_transceiver.on_encoder_msg = do_nothing
            self.mqtt_transceiver.on_gnss_msg = do_nothing

    def send(self, data: str):
        self.sender.send(data)
    
    def mqtt_disconnect_action(self,):
        self.set_transceiver_config(internet_available=False)
        self.sender = self.lora_transceiver

    def mqtt_reconnect_action(self,):
        self.set_transceiver_config(internet_available=True)
        self.sender = self.socket_sender

    def lora_disconnect_action(self,):
        class NoSender:
            def send():
                pass
        
        self.sender = NoSender()

    def lora_reconnect_action(self,):
        self.sender = self.lora_transceiver

    def socket_disconnect_action(self,):
        self.set_transceiver_config(internet_available=False)
        self.sender = self.lora_transceiver

    def socket_reconnect_action(self,):
        self.set_transceiver_config(internet_available=True)
        self.sender = self.socket_sender

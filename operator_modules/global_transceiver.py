from socket_sender import SocketSender
import paho.mqtt.client as mqtt
import threading
import json, time
from lora_transceiver import LoRaTransceiver
from mqtt_receiver import MQTTReceiver
from enum import Enum


class ManualConnectionMethod(Enum):
    LoRa = 'LoRa'
    internet = 'socket'

class ConnectionMode(Enum):
    auto = 'auto'
    manual = 'manual'


class GlobalTransceiver:
    def __init__(self,
                 lidar_data_callback,
                 depth_cam_data_callback,
                 rgb_cam_data_callback,
                 encoder_data_callback,
                 gnss_data_callback
                 ) -> None:
        
        self.sender_internet_available = True
        self.receiver_internet_available = True
        self.lora_available = True

        self.connection_mode = ConnectionMode.auto
        self.manual_connection_method = ManualConnectionMethod.LoRa

        self.change_receiver_config_lock = threading.Lock()
        self.change_sender_config_lock = threading.Lock()
        
        self.change_sender_internet_state_lock = threading.Lock()
        self.change_receiver_internet_state_lock = threading.Lock()
        self.change_lora_state_lock = threading.Lock()

        self.encoder_data_callback = encoder_data_callback
        self.gnss_data_callback = gnss_data_callback

        self.socket_sender = None
        self.lora_transceiver = None
        self.mqtt_receiver = None

        self.socket_sender = SocketSender(self.socket_sender_disconnect_action, 
                                          self.socket_sender_reconnect_action)
        
        self.lora_transceiver = LoRaTransceiver(encoder_data_callback,gnss_data_callback, 
                                                self.lora_transceiver_disconnect_action, 
                                                self.lora_transceiver_reconnect_action)
        
        self.mqtt_receiver = MQTTReceiver(lidar_data_callback,
                                         depth_cam_data_callback,
                                         rgb_cam_data_callback,
                                         encoder_data_callback,
                                         gnss_data_callback,
                                         self.mqtt_receiver_disconnect_action,
                                         self.mqtt_receiver_reconnect_action)

        
        # self.lora_transceiver.on_lora_disconnect_action = self.lora_transceiver_disconnect_action
        # self.lora_transceiver.on_lora_reconnect_action = self.lora_transceiver_reconnect_action
        
        # self.mqtt_transceiver.on_mqtt_disconnect_action = self.mqtt_receiver_disconnect_action
        # self.mqtt_transceiver.on_mqtt_reconnect_action = self.mqtt_receiver_reconnect_action
        
        # self.socket_sender.on_socket_disconnect_action = self.socket_sender_disconnect_action
        # self.socket_sender.on_socket_reconnect_action = self.socket_sender_reconnect_action
        
        self.sender = self.socket_sender
        self.__set_sender_config()
        self.__set_receiver_config()

    def __change_sender_internet_state(self, internet_available):
        with self.change_sender_internet_state_lock:
            self.sender_internet_available = internet_available
            print('chaneg SENDER inet state to', self.sender_internet_available)

    def __change_receiver_internet_state(self, internet_available):
        with self.change_receiver_internet_state_lock:
            self.receiver_internet_available = internet_available
            print('chaneg RECEIVER inet state to', self.receiver_internet_available)


    def __change_lora_state(self, lora_available):
        with self.change_lora_state_lock:
            self.lora_available = lora_available
            print('chaneg lora state to', self.lora_available)
            
    def __set_receiver_config(self, use_lora=None):
        if self.mqtt_receiver:
            with self.change_receiver_config_lock:
                def do_nothing(smth=None):
                    pass
                
                if use_lora is None:
                    if self.receiver_internet_available:
                        self.lora_transceiver.on_encoder_data = do_nothing
                        self.lora_transceiver.on_gnss_data = do_nothing

                        self.mqtt_receiver.on_encoder_msg = self.encoder_data_callback
                        self.mqtt_receiver.on_gnss_msg = self.gnss_data_callback

                    else:
                        self.lora_transceiver.on_encoder_data = self.encoder_data_callback
                        self.lora_transceiver.on_gnss_data = self.gnss_data_callback

                        self.mqtt_receiver.on_encoder_msg = do_nothing
                        self.mqtt_receiver.on_gnss_msg = do_nothing
                else:
                    if use_lora:
                        self.lora_transceiver.on_encoder_data = self.encoder_data_callback
                        self.lora_transceiver.on_gnss_data = self.gnss_data_callback

                        self.mqtt_receiver.on_encoder_msg = do_nothing
                        self.mqtt_receiver.on_gnss_msg = do_nothing
                    
                    else:
                        self.lora_transceiver.on_encoder_data = do_nothing
                        self.lora_transceiver.on_gnss_data = do_nothing

                        self.mqtt_receiver.on_encoder_msg = self.encoder_data_callback
                        self.mqtt_receiver.on_gnss_msg = self.gnss_data_callback

                print('set RECEIVER inet:', self.receiver_internet_available, use_lora)

    def __set_sender_config(self):
        if self.socket_sender and self.lora_transceiver:
            with self.change_sender_config_lock:
                if self.connection_mode == ConnectionMode.auto:
                    if self.sender_internet_available:
                        self.sender = self.socket_sender
                    else:
                        if self.lora_available:
                            self.sender = self.lora_transceiver
                        else:
                            class NoSender:
                                def send(self, data=None):
                                    pass
                            
                            self.sender = NoSender()

                else:
                    if self.manual_connection_method == ManualConnectionMethod.internet:
                        if self.sender_internet_available:
                            self.sender = self.socket_sender
                        else:
                            class NoSender:
                                def send(self, data=None):
                                    pass
                            
                            self.sender = NoSender()


                    elif self.manual_connection_method == ManualConnectionMethod.LoRa:
                        if self.lora_available:
                            self.sender = self.lora_transceiver
                        else:
                            class NoSender:
                                def send(self, data=None):
                                    pass
                            
                            self.sender = NoSender()


                print('set sender: ', self.sender)

    def set_connection_mode(self, auto: bool, method: ManualConnectionMethod=None):
        if auto:
            self.connection_mode = ConnectionMode.auto
            self.__set_receiver_config()

        else:
            self.connection_mode = ConnectionMode.manual
            if method:
                self.manual_connection_method = method

                if method == ManualConnectionMethod.LoRa:
                    self.__set_receiver_config(use_lora=True)
                else:
                    self.__set_receiver_config()
            else:
                self.manual_connection_method = ManualConnectionMethod.LoRa
                self.__set_receiver_config(use_lora=True)

        self.__set_sender_config()


    def send(self, data: str):
        print(time.time(),'sent with ', self.sender)
        self.sender.send(data)

    def mqtt_receiver_disconnect_action(self,):
        self.__change_receiver_internet_state(internet_available=False)
        
        # if self.connection_mode == ConnectionMode.auto:
        self.__set_receiver_config()
        
            #     self.set_receiver_config(internet_available=False)
            #     self.sender = self.lora_transceiver

            # if self.manual_connection_method == ManualConnectionMethod.internet:
            #     self.set_receiver_config(internet_available=True)
            #     self.sender = self.socket_sender


    def mqtt_receiver_reconnect_action(self,):
        self.__change_receiver_internet_state(internet_available=True)
        # if self.connection_mode == ConnectionMode.auto:
            
        self.__set_receiver_config()
         
        #         self.set_receiver_config(internet_available=False)
        #         self.sender = self.lora_transceiver

        #     elif self.manual_connection_method == ManualConnectionMethod.internet:
        #         self.set_receiver_config(internet_available=True)
        #         self.sender = self.socket_sender

    def lora_transceiver_disconnect_action(self,):
        self.__change_lora_state(lora_available=False)
        # if self.connection_mode == ConnectionMode.auto:
            # if not self.sender_internet_available:
                
        self.__set_sender_config()

        # else:
        #     if self.manual_connection_method == ManualConnectionMethod.LoRa:
        #         self.__set_sender_config()

    def lora_transceiver_reconnect_action(self,):
        self.__change_lora_state(lora_available=True)
        print('lora reconn act')
        # if self.connection_mode == ConnectionMode.auto:
        #     if not self.sender_internet_available:
        self.__set_sender_config()
        # else:
        #     if self.manual_connection_method == ManualConnectionMethod.LoRa:
        #         self.__set_sender_config()

    def socket_sender_disconnect_action(self,):
        self.__change_sender_internet_state(internet_available=False)
        
        # if self.connection_mode == ConnectionMode.auto:
        self.__set_sender_config()
        
        # else:
        #     if self.manual_connection_method == ManualConnectionMethod.internet:
        #         self.__set_sender_config()


    def socket_sender_reconnect_action(self,):
        self.__change_sender_internet_state(internet_available=True)
        # if self.connection_mode == ConnectionMode.auto:
        self.__set_sender_config()
        
        # else:
        #     if self.manual_connection_method == ManualConnectionMethod.internet:
        #         self.__set_sender_config()

def nothin(non=None, ):
    pass

trans = GlobalTransceiver( nothin,nothin, nothin, nothin,  nothin)


def te1():
    while 1:
        import time
        time.sleep(1)
        # print('wachawont')

        trans.send('amogus')

def te2():
    while 1:
        import time
        print('--- changemod to intet--')
        
        trans.set_connection_mode(False, ManualConnectionMethod.internet)
        time.sleep(10)
        print('--- changemod to LORA--')
        trans.set_connection_mode(False, ManualConnectionMethod.LoRa)
        time.sleep(10)
        print('--- changemod to auto--')
        
        trans.set_connection_mode(True)
        time.sleep(10)


tre1 = threading.Thread(target=te1)
tre2 = threading.Thread(target=te2)
tre1.start()
tre2.start()
tre1.join()
tre2.join()

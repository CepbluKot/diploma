import threading
from operator_modules.transceiver_modules.socket_sender import SocketSender
from operator_modules.transceiver_modules.lora_transceiver import LoRaTransceiver
from operator_modules.transceiver_modules.mqtt_receiver import MQTTReceiver
from enum import Enum

    
class ManualConnectionMethod(Enum):
    LoRa = "LoRa"
    internet = "socket"

class ConnectionType(Enum):
    LoRa = "LoRa"
    internet = "socket"
    no_connection = "no_connection"
    
class ConnectionMode(Enum):
    auto = "auto"
    manual = "manual"


class GlobalTransceiver:
    def __init__(self,
                 lidar_data_callback,
                 depth_cam_data_callback,
                 rgb_cam_data_callback,
                 encoder_data_callback,
                 gnss_data_callback,
                 temp_hum_data_callback,
                 gui_socket_connect_callback,
                 gui_socket_disconnect_callback,
                 gui_socket_reconnect_callback,
                 gui_lora_connect_callback,
                 gui_lora_disconnect_callback,
                 gui_lora_reconnect_callback,
                 ) -> None:

        class NoSender:
            def send(self, data=None):
                pass
                
        self.no_sender = NoSender()

        self.lidar_data_callback = lidar_data_callback
        self.depth_cam_data_callback = depth_cam_data_callback
        self.rgb_cam_data_callback = rgb_cam_data_callback
        self.encoder_data_callback = encoder_data_callback
        self.gnss_data_callback = gnss_data_callback
        self.temp_hum_data_callback = temp_hum_data_callback

        self.gui_lora_reconnect_callback = gui_lora_reconnect_callback
        self.gui_socket_disconnect_callback = gui_socket_disconnect_callback
        self.gui_socket_reconnect_callback = gui_socket_reconnect_callback
        self.gui_lora_disconnect_callback = gui_lora_disconnect_callback
        self.gui_socket_connect_callback = gui_socket_connect_callback
        self.gui_lora_connect_callback = gui_lora_connect_callback

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

        self.socket_sender = None
        self.lora_transceiver = None
        self.mqtt_receiver = None

        self.socket_sender = SocketSender(self.socket_sender_connect_action,
                                          self.socket_sender_disconnect_action, 
                                          self.socket_sender_reconnect_action)
        
        self.lora_transceiver = LoRaTransceiver(self.encoder_data_callback, self.gnss_data_callback, self.temp_hum_data_callback,
                                                self.lora_transceiver_connect_action,
                                                self.lora_transceiver_disconnect_action, 
                                                self.lora_transceiver_reconnect_action)
        
        self.mqtt_receiver = MQTTReceiver(self.lidar_data_callback,
                                          self.depth_cam_data_callback,
                                          self.rgb_cam_data_callback,
                                          self.encoder_data_callback,
                                          self.gnss_data_callback,
                                          self.temp_hum_data_callback,
                                          self.mqtt_receiver_disconnect_action,
                                          self.mqtt_receiver_reconnect_action)

        
        self.sender = self.socket_sender
        self.__set_sender_config()



    def __change_sender_internet_state(self, internet_available):
        with self.change_sender_internet_state_lock:
            self.sender_internet_available = internet_available
            # print("chaneg SENDER inet state to", self.sender_internet_available)

    def __change_receiver_internet_state(self, internet_available):
        with self.change_receiver_internet_state_lock:
            self.receiver_internet_available = internet_available
            # print("chaneg RECEIVER inet state to", self.receiver_internet_available)


    def __change_lora_state(self, lora_available):
        with self.change_lora_state_lock:
            self.lora_available = lora_available
            # print("chaneg lora state to", self.lora_available)
            
    
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
                            self.sender = self.no_sender

                else:
                    if self.manual_connection_method == ManualConnectionMethod.internet:
                        if self.sender_internet_available:
                            self.sender = self.socket_sender
                        else:
                            self.sender = self.no_sender


                    elif self.manual_connection_method == ManualConnectionMethod.LoRa:
                        if self.lora_available:
                            self.sender = self.lora_transceiver
                        else:
                            self.sender = self.no_sender


    def get_curr_connection_type(self,) -> ConnectionType:
        if isinstance(self.sender, SocketSender):
            return ConnectionType.internet

        elif isinstance(self.sender, LoRaTransceiver):
            return ConnectionType.LoRa
        
        else:
            return ConnectionType.no_connection

    def set_connection_mode(self, auto: bool, method: ManualConnectionMethod=None):
        if auto:
            self.connection_mode = ConnectionMode.auto

        else:
            self.connection_mode = ConnectionMode.manual
            if method:
                self.manual_connection_method = method

            else:
                self.manual_connection_method = ManualConnectionMethod.LoRa


        self.__set_sender_config()
        print("conn mode set")

    def send(self, data: str):
        # print(time.time(),"sent with ", self.sender)
        self.sender.send(data)

    def mqtt_receiver_disconnect_action(self,):
        self.__change_receiver_internet_state(internet_available=False)


    def mqtt_receiver_reconnect_action(self,):
        self.__change_receiver_internet_state(internet_available=True)
    

    def lora_transceiver_connect_action(self,):
        self.gui_lora_connect_callback()

    def lora_transceiver_disconnect_action(self,):
        self.__change_lora_state(lora_available=False)
        self.__set_sender_config()
        self.gui_lora_disconnect_callback()

    def lora_transceiver_reconnect_action(self,):
        self.__change_lora_state(lora_available=True)
        self.__set_sender_config()
        self.gui_lora_reconnect_callback()

    def socket_sender_connect_action(self,):
        self.gui_socket_connect_callback()

    def socket_sender_disconnect_action(self,):
        self.__change_sender_internet_state(internet_available=False)
        self.__set_sender_config()
        self.gui_socket_disconnect_callback()
        


    def socket_sender_reconnect_action(self,):
        self.__change_sender_internet_state(internet_available=True)
        self.__set_sender_config()
        self.gui_socket_reconnect_callback()


def dummy(*args, **kwargs):
    pass



global_transceiver = GlobalTransceiver(dummy,
                                        dummy,
                                        dummy,
                                        dummy,
                                        dummy,
                                        dummy,
                                        dummy,
                                        dummy,
                                        dummy,
                                        dummy,
                                        dummy,
                                        dummy)

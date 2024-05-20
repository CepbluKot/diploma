import threading
from robot_modules.transceiver_modules.socket_receiver import SocketReceiver
from transceiver_modules.lora_transceiver import LoRaTransceiver
from robot_modules.transceiver_modules.mqtt_sender import MQTTSender


class GlobalTransceiver:
    def __init__(self,
                 command_data_callback,
                 ) -> None:
        
        self.socket_receiver = None
        self.lora_transceiver = None
        self.mqtt_sender = None

        self.socket_receiver = SocketReceiver(command_data_callback)
        self.lora_transceiver = LoRaTransceiver(command_data_callback)
        self.mqtt_sender = MQTTSender()


    def send(self, data: str):
        try:
            self.lora_transceiver.send(data)
            
            if 'depth_cam' in data:
                self.mqtt_sender.send_depth_cam_data(data['depth_cam'])

            if 'rgb_cam' in data:
                self.mqtt_sender.send_rgb_cam_data(data['rgb_cam'])

            if 'encoder' in data:
                self.mqtt_sender.send_encoder_data(data['encoder'])

            if 'gnss' in data:
                self.mqtt_sender.send_gnss_data(data['gnss'])

            if 'lidar' in data:
                self.mqtt_sender.send_lidar_data(data['lidar'])
        
        except Exception as e:
            print(f'error during sending: {e}')

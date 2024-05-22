from robot_modules.transceiver_modules.socket_receiver import SocketReceiver
from robot_modules.transceiver_modules.lora_transceiver import LoRaTransceiver
from robot_modules.transceiver_modules.mqtt_sender import MQTTSender
from data_formats.all_data import AllData, LoraData


class GlobalTransceiver:
    def __init__(self,
                 command_data_callback,
                 config: dict) -> None:
        
        self.socket_receiver = None
        self.lora_transceiver = None
        self.mqtt_sender = None

        self.socket_receiver = SocketReceiver(command_data_callback, config)
        self.lora_transceiver = LoRaTransceiver(command_data_callback, config)
        self.mqtt_sender = MQTTSender(config)


    def send(self, data: AllData):
        try:

            self.lora_transceiver.send(LoraData(data.dict()).json())
            
            if data.depth_cam_data is not None:
                self.mqtt_sender.send_depth_cam_data(data.depth_cam_data)

            if data.rgb_cam_data is not None:
                self.mqtt_sender.send_rgb_cam_data(data.rgb_cam_data)

            if data.encoder_data is not None:
                self.mqtt_sender.send_encoder_data(data.encoder_data.json())

            if data.gnss_data is not None:
                self.mqtt_sender.send_gnss_data(data.gnss_data.json())

            if data.lidar_data is not None:
                self.mqtt_sender.send_lidar_data(data.lidar_data)

            if data.temp_hum_data is not None:
                self.mqtt_sender.send_temp_hum_data(data.temp_hum_data.json())

        except Exception as e:
            print(f"error during sending: {e}")

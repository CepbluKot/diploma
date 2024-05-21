from numpy import ndarray
from transceiver_modules.global_transceiver import GlobalTransceiver
from senders.engine_control_sender import MoveControl
from readers.launch_all_readers import AllReaders

from data_formats.send_data import SendData
from data_formats.control_command import ControlCommand


if __name__ == "__main__":
    all_data_to_send = SendData()
    move_control = MoveControl()

    def on_control_command(raw_command: str):
        move_control.execute_command(raw_command)
        command = ControlCommand.parse_raw(raw_command)
        all_data_to_send.last_control_command = command

    transceiver = GlobalTransceiver(on_control_command)
    

    def on_encoder_data(data: str):
        all_data_to_send.encoder_data = data 
    
    def on_gnss_data(data: str):
        all_data_to_send.gnss_data = data

    def on_depth_cam_data(data: ndarray):
        all_data_to_send.depth_cam_data = data

    def on_rgb_cam_data(data: ndarray):
        all_data_to_send.rgb_cam_data = data
    
    def on_lidar_data(data: list):
        all_data_to_send.lidar_data = data

    all_readers = AllReaders(on_encoder_data, 
               on_gnss_data, 
               on_depth_cam_data,
               on_rgb_cam_data,
               on_lidar_data)

    if  all_data_to_send.lidar_data and \
        all_data_to_send.gnss_data and \
        all_data_to_send.depth_cam_data and \
        all_data_to_send.rgb_cam_data and \
        all_data_to_send.encoder_data:

        transceiver.send(all_data_to_send.dict())

import threading
import uvicorn
from numpy import ndarray
from transceiver_modules.global_transceiver import GlobalTransceiver
from senders.engine_control_sender import move_control
from readers.launch_all_readers import AllReaders

from data_formats.all_data import all_data
from data_formats.control_command import ControlCommand
from rest_api.app import app


if __name__ == "__main__":

    def on_control_command(raw_command: str):
        move_control.execute_command(raw_command)
        command = ControlCommand.parse_raw(raw_command)
        all_data.last_control_command = command

    transceiver = GlobalTransceiver(on_control_command)
    

    def on_encoder_data(data: str):
        all_data.encoder_data = data 
    
    def on_gnss_data(data: str):
        all_data.gnss_data = data

    def on_depth_cam_data(data: ndarray):
        all_data.depth_cam_data = data

    def on_rgb_cam_data(data: ndarray):
        all_data.rgb_cam_data = data
    
    def on_lidar_data(data: list):
        all_data.lidar_data = data

    def on_temp_hum_data(data: str):
        all_data.temp_hum_data = data

    all_readers = AllReaders(on_encoder_data, 
                             on_gnss_data, 
                             on_depth_cam_data,
                             on_rgb_cam_data,
                             on_lidar_data,
                             on_temp_hum_data)
    
    def send_data_job():
        while send_data_process.is_alive():
            if  all_data.lidar_data and \
                all_data.gnss_data and \
                all_data.depth_cam_data and \
                all_data.rgb_cam_data and \
                all_data.encoder_data and \
                all_data.temp_hum_data:

                transceiver.send(all_data.dict())

    send_data_process = threading.Thread(target=send_data_job)

    def fastapi_job():
        uvicorn.run(app, host="0.0.0.0", port=5001)

    fastapi_process = threading.Thread(target=fastapi_job)

    fastapi_process.start()
    send_data_process.start()
    fastapi_process.join()
    send_data_process.join()

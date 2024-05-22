import threading
import time
import uvicorn
import json
from numpy import ndarray
from robot_modules.transceiver_modules.global_transceiver import GlobalTransceiver
from robot_modules.senders.engine_control_sender import move_control
from robot_modules.readers.launch_all_readers import AllReaders
from robot_modules.rest_api.app import app

from data_formats.all_data import all_data_for_robot
from data_formats.control_command import ControlCommand
from data_formats.encoder_data import EngineEncoderData
from data_formats.gnss_data import GNSSData
from data_formats.temp_hum_data import TempHumData


def main():
    config = json.load(open("config.json"))
    
    def on_control_command(raw_command: str):
        move_control.execute_command(raw_command)
        command = ControlCommand.parse_raw(raw_command)
        all_data_for_robot.last_control_command = command

    transceiver = GlobalTransceiver(on_control_command, config)

    def on_encoder_data(data: str):
        all_data_for_robot.encoder_data = EngineEncoderData.parse_raw(data) 
    
    def on_gnss_data(data: str):
        all_data_for_robot.gnss_data = GNSSData.parse_raw(data)

    def on_depth_cam_data(data: ndarray):
        all_data_for_robot.depth_cam_data = data

    def on_rgb_cam_data(data: ndarray):
        all_data_for_robot.rgb_cam_data = data
    
    def on_lidar_data(data: list):
        all_data_for_robot.lidar_data = data

    def on_temp_hum_data(data: str):
        all_data_for_robot.temp_hum_data = TempHumData.parse_raw(data)

    all_readers = AllReaders(on_encoder_data, 
                             on_gnss_data, 
                             on_depth_cam_data,
                             on_rgb_cam_data,
                             on_lidar_data,
                             on_temp_hum_data,
                             config)
    
    def send_data_job():
        while send_data_process.is_alive():
            if  all_data_for_robot.lidar_data and \
                all_data_for_robot.gnss_data and \
                all_data_for_robot.depth_cam_data and \
                all_data_for_robot.rgb_cam_data and \
                all_data_for_robot.encoder_data and \
                all_data_for_robot.temp_hum_data:

                transceiver.send(all_data_for_robot)
                time.sleep(0.2)

    send_data_process = threading.Thread(target=send_data_job)

    def fastapi_job():
        uvicorn.run(app, host="0.0.0.0", port=config['http_server_port'])

    fastapi_process = threading.Thread(target=fastapi_job)

    fastapi_process.start()
    send_data_process.start()
    fastapi_process.join()
    send_data_process.join()

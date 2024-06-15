from robot_modules.readers.encoder_reader import EncoderReader
from robot_modules.readers.gnss_reader import GNSSReader
from robot_modules.readers.kinect_data_reader import KinectDataReader
from robot_modules.readers.lidar_data_reader import LidarDataReader
from robot_modules.readers.temp_hum_reader import TempHumReader


class AllReaders():
    def __init__(self, 
                 on_encoder_data, 
                 on_gnss_data, 
                 on_depth_cam_data,
                 on_rgb_cam_data,
                 on_lidar_data,
                 on_temp_hum_data,
                 config: dict) -> None:
        
        self.on_encoder_data = on_encoder_data  
        self.on_gnss_data = on_gnss_data
        self.on_depth_cam_data = on_depth_cam_data
        self.on_rgb_cam_data = on_rgb_cam_data
        self.on_lidar_data = on_lidar_data
        self.on_temp_hum_data = on_temp_hum_data

        self.encoder_reader = EncoderReader(on_encoder_data, config)
        self.gnss_reader = GNSSReader(on_gnss_data, config)
        self.kinect_data_reader = KinectDataReader(on_depth_cam_data, on_rgb_cam_data)
        self.lidar_data_reader = LidarDataReader(on_lidar_data, config)
        self.temp_hum_reader = TempHumReader(on_temp_hum_data, config)

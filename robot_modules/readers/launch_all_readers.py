from readers.encoder_reader import EncoderReader
from readers.gnss_reader import GNSSReader
from readers.kinect_data_reader import KinectDataReader
from readers.lidar_data_reader import LidarDataReader
from readers.temp_hum_reader import TempHumReader


class AllReaders():
    def __init__(self, 
                 on_encoder_data, 
                 on_gnss_data, 
                 on_depth_cam_data,
                 on_rgb_cam_data,
                 on_lidar_data,
                 on_temp_hum_data,
                 config: dict) -> None:
        
        EncoderReader(on_encoder_data, config)
        GNSSReader(on_gnss_data, config)
        KinectDataReader(on_depth_cam_data, on_rgb_cam_data)
        LidarDataReader(on_lidar_data, config)
        TempHumReader(on_temp_hum_data, config)

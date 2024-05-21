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
                 on_temp_hum_data) -> None:
        
        EncoderReader(on_encoder_data)
        GNSSReader(on_gnss_data)
        KinectDataReader(on_depth_cam_data, on_rgb_cam_data)
        LidarDataReader(on_lidar_data)
        TempHumReader(on_temp_hum_data)

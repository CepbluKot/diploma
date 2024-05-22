import pydantic
from typing import Optional
from data_formats.control_command import ControlCommand
from data_formats.gnss_data import GNSSData
from data_formats.encoder_data import EngineEncoderData
from data_formats.temp_hum_data import TempHumData
from numpy import ndarray


class AllData(pydantic.BaseModel):
    last_control_command: Optional[ControlCommand] = None
    lidar_data: Optional[list] = None
    gnss_data: Optional[GNSSData] = None
    depth_cam_data: Optional[ndarray] = None
    rgb_cam_data: Optional[ndarray] = None
    encoder_data: Optional[EngineEncoderData] = None
    temp_hum_data: Optional[TempHumData] = None


    class Config:
        arbitrary_types_allowed = True


class LoraData(pydantic.BaseModel):
    last_control_command: Optional[ControlCommand] = None
    gnss_data: Optional[GNSSData] = None
    encoder_data: Optional[EngineEncoderData] = None
    temp_hum_data: Optional[TempHumData] = None


all_data_for_robot = AllData()

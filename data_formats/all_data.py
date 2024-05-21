import pydantic
from typing import Optional
from data_formats.control_command import ControlCommand
from numpy import ndarray


class AllData(pydantic.BaseModel):
    last_control_command: Optional[ControlCommand] = None
    lidar_data: Optional[list] = None
    gnss_data: Optional[str] = None
    depth_cam_data: Optional[ndarray] = None
    rgb_cam_data: Optional[ndarray] = None
    encoder_data: Optional[str] = None
    temp_hum_data: Optional[str] = None


    class Config:
        arbitrary_types_allowed = True

all_data = AllData()

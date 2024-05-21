import pydantic
from typing import Optional
from control_command import ControlCommand
from numpy import ndarray


class SendData(pydantic.BaseModel):
    last_control_command: Optional[ControlCommand] = None
    lidar_data: Optional[list] = None
    gnss_data: Optional[str] = None
    depth_cam_data: Optional[ndarray] = None
    rgb_cam_data: Optional[ndarray] = None
    encoder_data: Optional[str] = None

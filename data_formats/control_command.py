import pydantic
from enum import Enum
from typing import Optional


class MoveType(Enum,):
    forward = "forward"
    backward = "backward"
    stop = "stop"

class Direction(pydantic.BaseModel):
    direction: Optional[MoveType] = None

class ControlCommand(pydantic.BaseModel):
    left: Optional[Direction] = None
    right: Optional[Direction] = None

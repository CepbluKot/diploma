import pydantic
from enum import Enum
from typing import Optional


class MoveType(Enum,):
    forward = "f"
    backward = "b"
    stop = "s"

class Direction(pydantic.BaseModel):
    direction: Optional[MoveType] = MoveType.stop

class ControlCommand(pydantic.BaseModel):
    left: Optional[Direction] = None
    right: Optional[Direction] = None

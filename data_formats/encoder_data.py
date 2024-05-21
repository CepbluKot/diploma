from typing import Optional
import pydantic


class EngineEncoderData(pydantic.BaseModel):
    left: Optional[int] = -1
    right: Optional[int] = -1

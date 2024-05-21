import pydantic


class EngineEncoderData(pydantic.BaseModel):
    left: int
    right: int

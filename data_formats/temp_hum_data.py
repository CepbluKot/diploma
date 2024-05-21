import pydantic


class TempHumData(pydantic.BaseModel):
    temperature: float
    humidity: float

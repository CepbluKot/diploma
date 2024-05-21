from typing import Optional
import pydantic


class TempHumData(pydantic.BaseModel):
    temperature: Optional[float] = -1
    humidity: Optional[float] = -1

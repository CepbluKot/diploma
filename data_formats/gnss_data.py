from typing import Optional
import pydantic


class GNSSData(pydantic.BaseModel):
    lat: Optional[float] = -1
    lat_dir: Optional[str] = None
    lon: Optional[float] = -1
    lon_dir: Optional[str] = None
    spd_over_grnd_kmph: Optional[float] = -1
    true_track: Optional[float] = -1
    altitude: Optional[float] = -1

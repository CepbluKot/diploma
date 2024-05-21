import pydantic


class GNSSData(pydantic.BaseModel):
    lat: float = -1
    lat_dir: str = None
    lon: float = -1
    lon_dir: str = None
    spd_over_grnd_kmph: float = -1
    true_track: float = -1
    altitude: float = -1

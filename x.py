from data_formats.all_data import AllData, LoraData
from data_formats.control_command import ControlCommand,Direction,MoveType
from data_formats.gnss_data import GNSSData
from data_formats.encoder_data import EngineEncoderData
from data_formats.temp_hum_data import TempHumData


alles = AllData()
alles.last_control_command = ControlCommand(right=Direction(direction=MoveType.backward),left=Direction(direction=MoveType.backward))
alles.gnss_data = GNSSData(lat= -1,
    lat_dir = "s",
    lon = -1,
    lon_dir = "s",
    spd_over_grnd_kmph = -1,
    true_track = -1,
    altitude=123)
alles.encoder_data = EngineEncoderData(left=123, right=123)
alles.temp_hum_data = TempHumData(temperature=132, humidity=123)

not_alles = LoraData.parse_obj(alles.dict())

print(not_alles)


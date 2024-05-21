import json
from enum import Enum
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware


from data_formats.all_data import all_data
from data_formats.temp_hum_data import TempHumData
from data_formats.gnss_data import GNSSData
from data_formats.encoder_data import EngineEncoderData
from data_formats.control_command import ControlCommand
from senders.engine_control_sender import move_control


app = FastAPI()
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.get("/lidar")
async def lidar_data_get():
    processed_vals = []
    for data in all_data.lidar_data:
        processed_vals.append(data[1:])

    def data_sort_key(val):
        return val[0]

    return sorted(processed_vals, key=data_sort_key)


@app.get("/depth_camera")
async def depth_cam_data():
    if all_data.depth_cam_data is not None and all_data.depth_cam_data.all():
        return json.dumps(all_data.depth_cam_data.tolist())
    else:
        return {}

@app.get("/rgb_camera")
async def rgb_cam_data():
    if all_data.rgb_cam_data is not None and all_data.rgb_cam_data.all():
        return json.dumps(all_data.rgb_cam_data.tolist())


@app.get("/temp_and_hum")
async def temp_and_hum_data() -> TempHumData:
    return TempHumData.parse_raw(all_data.temp_hum_data)


@app.get("/gnss")
async def gnss_data() -> GNSSData:
    return GNSSData.parse_raw(all_data.gnss_data)



@app.get("/engine_encoders")
async def encoders_data() -> EngineEncoderData:
    return EngineEncoderData.parse_raw(all_data.encoder_data)


@app.post("/engine_command")
async def engine_control(command: ControlCommand):
    move_control.execute_command(command)
    
    return {"status": "ok"}

from fastapi import FastAPI
import uvicorn
from fastapi.middleware.cors import CORSMiddleware
import pydantic
from enum import Enum

app = FastAPI()
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

import threading
from rplidar import RPLidar
import paho.mqtt.client as mqtt
import pickle
import json


import freenect
import paho.mqtt.client as mqtt
import pickle
import json


config = json.load(open("config.json"))
ADDRESS = config["robot_address"]
MQTT_PORT = config["MQTT_port"]

MQTT_DEPTH_CAM_TOPIC_PICKLE = config["depth_cam_topic_pickle_format"]
MQTT_DEPTH_CAM_TOPIC_STR = config["depth_cam_topic_str_format"]
MQTT_RGB_CAM_TOPIC_PICKLE = config["rgb_cam_topic_pickle_format"]
MQTT_RGB_CAM_TOPIC_STR = config["rgb_cam_topic_str_format"]

DEPTH_CAM_IND = 0

rgb_img = None
depth_img = None


def kinektik():
    print("ama alive")
    global rgb_img
    global depth_img

    while True:
        if freenect.sync_get_depth(DEPTH_CAM_IND) and freenect.sync_get_video(
            DEPTH_CAM_IND
        ):
            d = freenect.sync_get_depth(DEPTH_CAM_IND)[0]
            r = freenect.sync_get_video(DEPTH_CAM_IND)[0]

            if d.size and r.size:
                rgb_img = r
                depth_img = d


@app.get("/lidar")
async def lidar_data():
    return {}


@app.get("/depth_camera")
async def depth_cam_data():
    return str(depth_img)


@app.get("/rgb_camera")
async def rgb_cam_data():
    return str(rgb_img)


class TempAndHumSensor(pydantic.BaseModel):
    temperature: float
    humidity: float


@app.get("/temp_and_hum")
async def temp_and_hum_data() -> TempAndHumSensor:
    return {"temperature": 24.5, "humidity": 50.0}


class GPSData(pydantic.BaseModel):
    latitude: float
    longitude: float
    speed_kmph: float
    track: float


@app.get("/gnss")
async def gnss_data() -> GPSData:
    return {
        "latitude": 56.23,
        "longitude": 38.48,
        "speed_kmph": 0,
        "track": 0,
    }


class EngineEncoderValues(pydantic.BaseModel):
    left: int
    right: int


import random


@app.get("/engine_encoders")
async def encoders_data() -> EngineEncoderValues:
    return {"left": random.randint(200, 400), "right": random.randint(-400, 0)}


class MvType(Enum,):
    forward = "forward"
    backward = "backward"
    stop = "stop"


class Dir(pydantic.BaseModel):
    direction: MvType


class Engin(pydantic.BaseModel):
    left: Dir
    right: Dir


@app.post("/engine_command")
async def engine_control(com: Engin):
    return {"status": "ok"}


if __name__ == "__main__":

    t1 = threading.Thread(target=kinektik)
    t1.daemon = True
    t1.start()
    uvicorn.run(app, host="0.0.0.0", port=5001)

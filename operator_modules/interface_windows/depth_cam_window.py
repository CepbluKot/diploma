import numpy as np
import threading
import cv2
import operator_modules.frame_convert2 as frame_convert2
import pickle
from operator_modules.transceiver_modules.global_transceiver import global_transceiver


depth_msg = []
rgb_msg = []


def on_new_rgb_img(data):
    global rgb_msg
    rgb_msg =  pickle.loads(data)


def on_new_depth_img(data):
    global depth_msg
    depth_msg =  pickle.loads(data)


global_transceiver.rgb_cam_data_callback = on_new_rgb_img
global_transceiver.depth_cam_data_callback = on_new_depth_img


def run():
    depth=np.zeros((480,640))
    rgb = np.zeros((480,640,3))
    while 1:
        if len(depth_msg) and len(rgb_msg):
            try:
                depth = frame_convert2.pretty_depth_cv(depth_msg)
                rgb = frame_convert2.video_cv(rgb_msg)

            except Exception:
                pass
            
        cv2.imshow("Depth", depth)
        cv2.imshow("RGB", rgb)

        cv2.waitKey(1000)

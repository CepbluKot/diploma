from operator_modules.gui.output import init
from operator_modules.interface_windows.lidar_window import run as lidar_window_launch
from operator_modules.interface_windows.depth_cam_window import run as depth_cam_window_launch
import threading


def main():
    main_process = threading.Thread(target=init)
    lidar_view_process = threading.Thread(target=lidar_window_launch)
    cam_view_process = threading.Thread(target=depth_cam_window_launch)
    cam_view_process.start()
    main_process.start()
    lidar_view_process.start()
    main_process.join()
    lidar_view_process.join()
    cam_view_process.join()

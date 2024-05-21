from operator_modules.gui.output import init_gui
from operator_modules.interface_windows.lidar_window import run as lidar_launch
from operator_modules.interface_windows.depth_cam_window import run as depth_cam_launch
import threading


def main():
    gui_process = threading.Thread(target=init_gui)
    lidar_view_process = threading.Thread(target=lidar_launch)
    cam_view_process = threading.Thread(target=depth_cam_launch)
    cam_view_process.start()
    gui_process.start()
    lidar_view_process.start()
    gui_process.join()
    lidar_view_process.join()
    cam_view_process.join()

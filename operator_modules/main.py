from gui.output import init_gui
from interface_windows.lidar_window import launch as lidar_launch
from interface_windows.depth_cam_window import launch as depth_cam_launch
import threading


if __name__ == "__main__":
    gui_process = threading.Thread(target=init_gui)
    lidar_view_process = threading.Thread(target=lidar_launch)
    cam_view_process = threading.Thread(target=depth_cam_launch)
    cam_view_process.start()
    gui_process.start()
    lidar_view_process.start()
    gui_process.join()
    lidar_view_process.join()
    cam_view_process.join()

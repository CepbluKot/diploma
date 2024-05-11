from gui.output import init_gui
import multiprocessing
from interface_windows.lidar_window import launch as lidar_launch
from interface_windows.depth_cam_window import launch as depth_cam_launch
from interface_windows.map_window import launch as map_launch
import threading


if __name__ == '__main__':
    gui_process = multiprocessing.Process(target=init_gui)
    # lidar_view_process = multiprocessing.Process(target=lidar_launch)
    # cam_view_process = multiprocessing.Process(target=depth_cam_launch)
    # map_view_process = multiprocessing.Process(target=map_launch)
    # map_view_process.start()
    # cam_view_process.start()
    gui_process.start()
    # lidar_view_process.start()
    gui_process.join()
    # lidar_view_process.join()
    # cam_view_process.join()
    # map_view_process.join()
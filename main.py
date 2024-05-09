from gui.output import init_gui
# from gui.calls.set_params_calls import *
# from gui.calls.move_to_point_calls import *
import multiprocessing
from receiver_modules.lidar_receiver import launch as lidar_launch
from receiver_modules.depth_cam_receiver import launch as depth_cam_launch


if __name__ == '__main__':
    gui_process = multiprocessing.Process(target=init_gui)
    lidar_view_process = multiprocessing.Process(target=lidar_launch)
    cam_view_process = multiprocessing.Process(target=depth_cam_launch)
    cam_view_process.start()
    gui_process.start()
    lidar_view_process.start()
    gui_process.join()
    lidar_view_process.join()
    cam_view_process.join()

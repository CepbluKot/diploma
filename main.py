import datetime
from gui.output import init_gui
# from gui.calls.set_params_calls import *
# from gui.calls.move_to_point_calls import *
import multiprocessing
from lidar_remote import launch as lidar_launch
from depth_cam_remote import launch as depth_cam_launch


p1 = multiprocessing.Process(target=init_gui)
p2 = multiprocessing.Process(target=lidar_launch)
p3 = multiprocessing.Process(target=depth_cam_launch)
p3.start()
p1.start()
p2.start()
p1.join()
p2.join()
p3.join()

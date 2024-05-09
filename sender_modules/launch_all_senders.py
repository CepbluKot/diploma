import threading
from depth_cam_data_sender import run as depth_cam_run
from lidar_data_sender import run as lidar_run


if __name__ == '__main__':
    depth_cam_thr = threading.Thread(target=depth_cam_run)
    lidar_thr = threading.Thread(target=lidar_run)

    depth_cam_thr.start()
    lidar_thr.start()
    depth_cam_thr.join()    
    lidar_thr.join()

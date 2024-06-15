import freenect
import threading


class KinectDataReader:
    def __init__(self, on_depth_cam_data, on_rgb_cam_data) -> None:
        self.on_depth_cam_data = on_depth_cam_data
        self.on_rgb_cam_data = on_rgb_cam_data
        
        self.DEPTH_CAM_IND = 0

        self.read_thr = threading.Thread(target=self.recv_job,)
        self.read_thr.daemon = True
        self.read_thr.start()
    
    def recv_job(self):
        while self.read_thr.is_alive():
            depth_mat = freenect.sync_get_depth(self.DEPTH_CAM_IND)[0]
            video = freenect.sync_get_video(self.DEPTH_CAM_IND)[0]

            if depth_mat.size:
                self.on_depth_cam_data(depth_mat)
            
            if video.size:
                self.on_rgb_cam_data(video)

import threading
from rplidar import RPLidar


class LidarDataReader:
    def __init__(self, on_lidar_data, config: dict) -> None:
        self.on_lidar_data = on_lidar_data
        
        self.LIDAR_PORT_NAME = config['lidar_serial_port']
        self.lidar = RPLidar(self.LIDAR_PORT_NAME)

        self.read_thr = threading.Thread(target=self.recv_job,)
        self.read_thr.daemon = True
        self.read_thr.start()
    
    def recv_job(self):
        try:
            while self.read_thr.is_alive():
                for scan in self.lidar.iter_scans():
                    self.on_lidar_data(scan)
        except Exception:
            self.recv_job()

from pyPS4Controller.controller import Controller
import threading, time
    
    
class MyController(Controller):

    def __init__(self, **kwargs):
        Controller.__init__(self, **kwargs)
        self.curr_l3_val = 0
        self.curr_r3_val = 0

        self.last_cmd = None

        self.commands_deque = []

        self.add_command_lock = threading.Lock()
        self.comm_sender_thr = threading.Thread(target=self.command_sender_thr)
        self.comm_sender_thr.daemon = True
        self.comm_sender_thr.start()

    def __add_command(self, command):
        with self.add_command_lock:
            self.commands_deque.append(command)

    def __get_command(self):
        with self.add_command_lock:
            if self.commands_deque:
                return self.commands_deque.pop()

    def command_sender_thr(self):
        while self.comm_sender_thr.is_alive():
            new_command = self.__get_command()
            if new_command:
                time.sleep(0.2)
                print('executed', new_command)

    def on_R3_down(self, val):
        self.curr_r3_val = val
        self.create_command()
        
        
    def on_R3_up(self, val):
        self.curr_r3_val = val
        self.create_command()
        
        
    def on_L3_up(self, val):
        self.curr_l3_val = val
        self.create_command()
        
        
    def on_L3_down(self, val):
        self.curr_l3_val = val
        self.create_command()
    
    def on_R3_press(self):
        self.create_command(True)

    def on_L3_press(self):
        self.create_command(True)

    def on_L3_y_at_rest(self):
        self.create_command(True)

    def on_R3_y_at_rest(self):
        self.create_command(True)


    def create_command(self, stop=False):
        if not stop:
            left_eng_val = self.curr_l3_val
            right_eng_val = self.curr_r3_val
                
            left_cmd = 'stop'

            if left_eng_val >= 32768 // 2:
                left_cmd = 'bwd'
            
            elif left_eng_val <= -32768 // 2:
                left_cmd = 'fwd'
            
            right_cmd = 'stop'
            
            if right_eng_val >= 32768 // 2:
                right_cmd = 'bwd'
            
            elif right_eng_val <= -32768 // 2:
                right_cmd = 'fwd'
            

            if self.last_cmd:
                if self.last_cmd != (left_cmd, right_cmd):
                    self.last_cmd = (left_cmd, right_cmd)
                    self.__add_command((left_cmd, right_cmd))
            else:
                self.last_cmd = (left_cmd, right_cmd)
                self.__add_command((left_cmd, right_cmd))
        else:
            self.__add_command(('stop', 'stop'))


controller = MyController(interface="/dev/input/js0", connecting_using_ds4drv=False)
def controller_work_thr():
    controller.listen(timeout=60)

th1 = threading.Thread(target=controller_work_thr)

th1.start()
th1.join()

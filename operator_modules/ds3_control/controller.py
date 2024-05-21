from pyPS4Controller.controller import Controller
import threading, time, json
from data_formats.control_command import ControlCommand, Direction, MoveType


class MyController(Controller):
    def __init__(self, send_json_command, **kwargs):
        Controller.__init__(self, **kwargs)
        
        self.send_json_command = send_json_command

        self.curr_l3_val = 0
        self.curr_r3_val = 0

        self.last_cmd = None
        
        self.left_safe_lock_armed = True
        self.right_safe_lock_armed = True
        
        
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
                new_command_obj = ControlCommand(left=Direction(direction=new_command[0]),
                                                right=Direction(direction=new_command[1]),
                                                )
                time.sleep(0.2)
                self.send_json_command( new_command_obj.json())

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

    def on_L2_press(self, val):
        self.left_safe_lock_armed = False

    def on_R2_press(self, val):
        self.right_safe_lock_armed = False

    def on_L2_release(self):
        self.left_safe_lock_armed = True
        self.create_command(True)

    def on_R2_release(self):
        self.right_safe_lock_armed = True
        self.create_command(True)

    def create_command(self, stop=False):
        if not stop:
            
            if (not self.right_safe_lock_armed and not self.left_safe_lock_armed):
                left_eng_val = self.curr_l3_val
                right_eng_val = self.curr_r3_val

                left_cmd = MoveType.stop

                if left_eng_val >= 32768 // 2:
                    left_cmd = MoveType.backward

                elif left_eng_val <= -32768 // 2:
                    left_cmd = MoveType.forward

                right_cmd = MoveType.stop

                if right_eng_val >= 32768 // 2:
                    right_cmd = MoveType.backward

                elif right_eng_val <= -32768 // 2:
                    right_cmd = MoveType.forward

                if self.last_cmd:
                    if self.last_cmd != (left_cmd, right_cmd):
                        self.last_cmd = (left_cmd, right_cmd)
                        self.__add_command((left_cmd, right_cmd))
                else:
                    self.last_cmd = (left_cmd, right_cmd)
                    self.__add_command((left_cmd, right_cmd))
            else:
                self.__add_command(("stop", "stop"))

        else:
            self.__add_command(("stop", "stop"))


def run(send_json_command):
    config = json.load(open("config.json"))

    controller = MyController(interface=config["ds3_controller_port"], connecting_using_ds4drv=False, send_json_command=send_json_command)
    def controller_work_thr():
        controller.listen(timeout=60)

    th1 = threading.Thread(target=controller_work_thr)
    th1.daemon = True
    th1.start()

from enum import Enum
from data_formats.control_command import ControlCommand, Direction, MoveType


class EngineSide(Enum,):
    left = "left"
    right = "right"

class ButtonsController:
    def __init__(self, send_command) -> None:
        self.send_command = send_command
        self.left_eng = Direction()
        self.right_eng = Direction()

    def __send_command(self):
        command = ControlCommand()
        command.left = self.left_eng
        command.right = self.right_eng
        
        self.send_command(command.json())

    def stop_button_press(self, engine_side: EngineSide=None):
        if engine_side is None:
            self.left_eng.direction = MoveType.stop
            self.right_eng.direction = MoveType.stop
            
        elif engine_side == EngineSide.left:
            self.left_eng.direction = MoveType.stop
            
        elif engine_side == EngineSide.right:
            self.right_eng.direction = MoveType.stop
            
        self.__send_command()


    def fwd_button_press(self, engine_side: EngineSide=None):
        if engine_side is None:
            self.left_eng.direction = MoveType.forward
            self.right_eng.direction = MoveType.forward
            
        elif engine_side == EngineSide.left:
            self.left_eng.direction = MoveType.forward
            
        elif engine_side == EngineSide.right:
            self.right_eng.direction = MoveType.forward
            
        self.__send_command()


    def bwd_button_press(self, engine_side: EngineSide=None):
        if engine_side is None:
            self.left_eng.direction = MoveType.backward
            self.right_eng.direction = MoveType.backward
            
        elif engine_side == EngineSide.left:
            self.left_eng.direction = MoveType.backward
            
        elif engine_side == EngineSide.right:
            self.right_eng.direction = MoveType.backward
            
        self.__send_command()
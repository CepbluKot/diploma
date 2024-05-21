from time import sleep
import serial, json, threading
import serial.tools.list_ports
from data_formats.control_command import ControlCommand


class EngineControlSender:
    def __init__(self, engine_control_serial_port) -> None:

        self.engine_control_port = engine_control_serial_port
        self.baudrate = 9600

        self.serial_engine_control_conn = None
        self.serial_engine_control_conn = serial.Serial(self.engine_control_port, self.baudrate)

    def send(self, data: str):
        self.serial_engine_control_conn.write((data).encode()+b"\r")


class MoveControl():
    def __init__(self) -> None:
        self.config = json.load(open("config.json"))
        self.left_engine_control = EngineControlSender(self.config["left_engine_control_serial_port"])
        self.right_engine_control = EngineControlSender(self.config["right_engine_control_serial_port"])

    def execute_command(self, raw_command: str):
        command = ControlCommand.parse_raw(raw_command)
        self.left_engine_control.send(command.left.direction)
        self.right_engine_control.send(command.right.direction)


move_control = MoveControl()

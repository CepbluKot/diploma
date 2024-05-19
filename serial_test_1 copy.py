from time import sleep
import pydantic
import serial, threading
import serial.tools.list_ports
import json


def search_for_ports():
    ports = list(serial.tools.list_ports.comports())
    return ports


def do_staff():

    # port = search_for_ports()[0].device
    port = "/dev/ttyUSB0"
    baudrate = 9600
    serial_conn1 = serial.Serial(port, baudrate)

    # serial_conn2 = serial.Serial("/dev/ttyUSB1", baudrate)
    from random import randint, uniform

    t = float(int(uniform(20, 25)))
    h = float(int(uniform(40, 60)))

    import time

    while serial_conn1.is_open:
        for val_1 in ['forward', 'backward', 'stop']:
            for val_2 in ['forward', 'backward', 'stop']:
            
                data = {"left": {"direction": val_1}, "right": {"direction": val_2}}

                serial_conn1.write(json.dumps(data).encode() + b"\r")
        # print(json.dumps(data))
        # time.sleep(1)
        # serial_conn2.write(json.dumps(data).encode() + b"\r")

                time.sleep(1)

        pass


if __name__ == "__main__":
    do_staff()

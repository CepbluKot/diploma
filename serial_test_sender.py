from time import sleep
import pydantic
import serial, threading
import serial.tools.list_ports


def search_for_ports():
    ports = list(serial.tools.list_ports.comports())
    return ports

def do_staff():
    
    # port = search_for_ports()[0].device
    port = '/dev/ttyUSB0'
    baudrate = 9600
    serial_conn = serial.Serial(port, baudrate)
    
    while not serial_conn.is_open:
        pass
        print('not open')

    while serial_conn.is_open:
        serial_conn.write(("lool").encode()+b'\r')
        print('sent')
        sleep(2)

if __name__ == "__main__":
    do_staff()
    
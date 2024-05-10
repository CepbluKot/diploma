from time import sleep
import pydantic,time
import serial, threading
import serial.tools.list_ports


def search_for_ports():
    ports = list(serial.tools.list_ports.comports())
    return ports

def do_staff():
    
    # port = search_for_ports()[0].device
    port = '/dev/ttyUSB1'
    baudrate = 9600
    serial_conn = serial.Serial(port, baudrate)
    
    while not serial_conn.is_open:
        pass
    
    read_data = None
    while serial_conn.is_open:
        try:
            time.sleep(1)
            if serial_conn.in_waiting:
                
                read_data = serial_conn.read_until(b'\r\n')
                read_data = read_data[:-2].decode()
                print(read_data)
            else:
                if read_data:
                    serial_conn.write((read_data).encode()+b'\r')
                    print('sent test 2')
                    read_data = None

        except Exception as e:
            print('err',e)
            break


if __name__ == "__main__":
    do_staff()
    
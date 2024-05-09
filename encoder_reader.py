from time import sleep
import serial, threading
import serial.tools.list_ports


encoder_data = 0


def search_for_ports():
    ports = list(serial.tools.list_ports.comports())
    return ports

def do_staff():
    print('available ports')
    for index, port in enumerate(search_for_ports()):
        print('[{}] {}'.format(index, port.description))

    port = search_for_ports()[0].device
    baudrate = 9600
    serial_conn = serial.Serial(port, baudrate)


    while serial_conn.is_open:
        try:
            encoder_data = int(serial_conn.readline().decode("utf-8"))
            print(encoder_data)
        except:
            break


if __name__ == "__main__":
    do_staff()
    
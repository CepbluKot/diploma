import serial, time


port = '/dev/ttyUSB0'
baudrate = 9600
serial_conn = serial.Serial(port, baudrate)



while 1:
    
    if serial_conn.in_waiting:
        read_data = serial_conn.read_until(b'\r\n')
        print(read_data)

    else:
        serial_conn.write(("f").encode()+b'\r')
        time.sleep(5)
        serial_conn.write(("s").encode()+b'\r')
        time.sleep(5)

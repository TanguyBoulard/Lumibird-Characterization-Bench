import serial

port = serial.Serial('COM16', 115200)
if not port.isOpen():
    port.open()
port.flush()

command = b'b\r\n'
port.write(command)
port.close()
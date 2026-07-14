import serial
import time

ser = serial.Serial(
    port="COM5",
    baudrate=9600,
    parity=serial.PARITY_ODD,
    stopbits=serial.STOPBITS_TWO,
    bytesize=serial.SEVENBITS,
    timeout=2
)

def send_command(cmd):
    ser.write((cmd + "\r\n").encode())
    time.sleep(0.5)
    response = ser.read_all()
    print(response)
    return response

send_command("stop")

ser.close()
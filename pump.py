import serial
import time

ser = serial.Serial(
    port="COM7",
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

def stop():
    ser.write(("stop" + "\r\n").encode())
    time.sleep(0.5)
    response = ser.read_all()
    print(response)
    return response

#clear
send_command("civolume")
send_command("ctvolume")
send_command("citime")
send_command("cttime")

#check
send_command("ivolume")
send_command("tvolume")
send_command("itime")
send_command("ttime")
send_command("irate")

send_command("svolume")

#set
send_command("irate 0.5 ul/min")
send_command("ttime 5")

send_command("ttime")
send_command("irate")

send_command("irun")

ser.close()
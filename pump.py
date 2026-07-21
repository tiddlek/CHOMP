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

def clear():
    #clear
    print("clear")
    send_command("civolume")
    send_command("ctvolume")
    send_command("citime")
    send_command("cttime")

def check():
    #check
    print("check")
    send_command("ivolume")
    send_command("tvolume")
    send_command("itime")
    send_command("ttime")
    send_command("irate")
    send_command("svolume")
    send_command("diameter")

def set(d, sv, tv, r):
    #set
    print("set")
    send_command(f"diameter {d} mm")
    send_command(f"svolume {sv} uL")
    send_command(f"tvolume {tv} uL")
    send_command(f"irate {r} uL/min")
    send_command("irun")

hamilton_700_diameters = {
    "5": 0.343,
    "10": 0.485,
    "25": 0.729,
    "50": 1.03
}

clear()

v = 10
set(hamilton_700_diameters[str(v)], v, 1, 10)

ser.close()
import serial
import time

ser = serial.Serial(
    port="COM8",
    baudrate=9600,
    parity=serial.PARITY_ODD,
    stopbits=serial.STOPBITS_TWO,
    bytesize=serial.SEVENBITS,
    timeout=2
)

def send_command(cmd):
    print(f"Sending: {cmd}")

    ser.write((cmd + "\r").encode())
    ser.flush()

    time.sleep(0.2)

    response = ser.read_all()

    print("Raw:", repr(response))
    print("Decoded:", response.decode(errors="replace"))

    return response

def clear():
    #clear
    print("clear")
    send_command("civolume")
    send_command("ctvolume")
    send_command("citime")
    send_command("cttime")

hamilton_700_diameters = {
    "5": 0.343,
    "10": 0.485,
    "25": 0.729,
    "50": 1.03
}

v = 10
send_command(f"svolume {v} uL") # clears rate
send_command(f"diameter {hamilton_700_diameters[str(v)]} mm") # clears rate
send_command("irate 0.1 uL/sec")
send_command("tvolume 1 uL")
send_command("irun")



import serial
import time

ser = serial.Serial(
    port="COM7",
    baudrate=19200,
    timeout=1
)

time.sleep(0.2)

# Clear anything waiting in the input buffer
ser.reset_input_buffer()

# Set MFC to 1.0 SLPM
print("Setting flow to 1.0 SLPM...")
ser.write(b"as8.5\r")
ser.flush()

time.sleep(0.2)

# Read the response
data = ser.read(ser.in_waiting)

print("Response:")
print(data.decode(errors="replace"))

ser.close()
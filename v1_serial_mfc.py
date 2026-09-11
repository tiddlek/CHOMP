import serial
import time

ser = serial.Serial(
    port="COM7",
    baudrate=19200,
    bytesize=serial.EIGHTBITS,
    parity=serial.PARITY_NONE,
    stopbits=serial.STOPBITS_ONE,
    timeout=1
)

time.sleep(0.5)

# Clear buffers
ser.reset_input_buffer()
ser.reset_output_buffer()

command = "as7.5\r"

print(f"Sending: {repr(command)}")

ser.write(command.encode("ascii"))
ser.flush()

# Give MFC time to respond
time.sleep(0.5)

response = ser.read_all()

print(f"Raw response: {response}")
print(f"Decoded response: {response.decode(errors='replace')}")

ser.close()
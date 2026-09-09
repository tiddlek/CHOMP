import serial

ser = serial.Serial(
    port="COM7",
    baudrate=19200,
    timeout=1
)

print("Connected:", ser.is_open)
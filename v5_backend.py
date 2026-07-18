import serial
import nidaqmx
import time

class Backend:
    def __init__(self):
        self.tasks = {}

        for wire in [1, 2, 3]:
            channel = f"Dev1/ao{wire-1}"
            task = nidaqmx.Task()
            task.ao_channels.add_ao_voltage_chan(channel)
            self.tasks[wire] = task

        for light in [8, 9, 10]:
            channel = f"Dev1/port0/line{light}"
            task = nidaqmx.Task()
            task.do_channels.add_do_chan(channel)
            self.tasks[light] = task

        ozone  = 11
        channel = f"Dev1/port0/line{ozone}"
        task = nidaqmx.Task()
        task.do_channels.add_do_chan(channel)
        self.tasks[ozone] = task


        self.ser = serial.Serial(
            port="COM7",
            baudrate=9600,
            parity=serial.PARITY_ODD,
            stopbits=serial.STOPBITS_TWO,
            bytesize=serial.SEVENBITS,
            timeout=2
        )

        #clear
        self.send_command("civolume")
        self.send_command("ctvolume")
        self.send_command("citime")
        self.send_command("cttime")

        #check
        self.send_command("ivolume")
        self.send_command("tvolume")
        self.send_command("itime")
        self.send_command("ttime")
        self.send_command("irate")

    def send_command(self, cmd):
        self.ser.write((cmd + "\r\n").encode())
        time.sleep(0.5)
        response = self.ser.read_all()
        print(response)
        return response
            
    def write_voltage(self, wire_id, voltage):
        if wire_id not in self.tasks:
            raise ValueError(f"No DAQ channel for wire {wire_id}")

        self.tasks[wire_id].write(voltage)
    
    def write_lights(self, config, on):
        if config == "c":
            self.tasks[8].write(on)
            self.tasks[10].write(on)
        elif config == "m":
            self.tasks[9].write(on)


    def write_ozone(self, on):
        self.tasks[11].write(on)
    
    def write_pump(self, start, flow_rate, duration, svolume=None):
        if start == True:
            self.ser.write((f"irate  {flow_rate} " + "uL/min" + "\r\n").encode())
            self.ser.write((f"ttime  {duration} " + "\r\n").encode())
            #self.ser.write((f"svolume  {svolume} " + "\r\n").encode())
            self.send_command("ttime")
            self.send_command("irate")
            self.ser.write(("irun" + "\r\n").encode())

        elif start == False:
            self.ser.write(("stop" + "\r\n").encode())
        time.sleep(0.5)
        response = self.ser.read_all()
        print(response)
        return response
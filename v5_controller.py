import serial
import nidaqmx
import time

class NI_DAQ_SERIAL_CONTROLLER:
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

        self.hamilton_700_diameters = {
            "5.0": 0.343,
            "10.0": 0.485,
            "25.0": 0.729,
            "50.0": 1.03
        }

    def clear(self):
        #clear
        print("clear")
        self.send_command("civolume")
        self.send_command("ctvolume")
        self.send_command("citime")
        self.send_command("cttime")
    
    def set(self, d, sv, tv, r):
        #set
        print("set")
        self.send_command(f"diameter {d} mm")
        self.send_command(f"svolume {sv} uL")
        self.send_command(f"irate {r} uL/sec")
        self.send_command(f"tvolume {tv} uL")
        self.send_command("irun")

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
            self.set(self.hamilton_700_diameters[str(svolume)], svolume, flow_rate*duration, flow_rate)

        elif start == False:
            self.ser.write(("stop" + "\r\n").encode())
        time.sleep(0.5)
        response = self.ser.read_all()
        print(response)
        return response
    
    def close(self):
        self.ser.close()
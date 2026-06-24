import nidaqmx

class NI_DAQBackend:
    def __init__(self):
        self.tasks = {}

        for wire in [1, 2, 3]:
            channel = f"Dev1/ao{wire-1}"
            task = nidaqmx.Task()
            task.ao_channels.add_ao_voltage_chan(channel)
            self.tasks[wire] = task

    def write_voltage(self, wire_id, voltage):
        if wire_id not in self.tasks:
            raise ValueError(f"No DAQ channel for wire {wire_id}")

        self.tasks[wire_id].write(voltage)
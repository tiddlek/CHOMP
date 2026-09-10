from v5_devices import MFC, Pump, Ozone, Light

class TaskScheduler:
    def __init__(self, backend):
        self.mfcs = []
        self.pumps = []
        self.lights = []
        self.ozones = []
        self.current_time = 0
        self.SAFE_SLPM = 3.5
        self.log_callback = None

        # dependency injection (important part)
        self.backend = backend

    def log(self, message):
        if self.log_callback is not None:
            self.log_callback(message)

    def add_mfc(self, mfc):
        self.mfcs.append(mfc)

    def add_pump(self, pump):
        self.pumps.append(pump)
    
    def add_light(self, light):
        self.lights.append(light)

    def add_ozone(self, ozone):
        self.ozones.append(ozone)

    def reset(self):
        self.current_time = 0
        for mfc in self.mfcs:
            for task in mfc.tasks:
                task.active = False
        for pump in self.pumps:
            for task in pump.tasks:
                task.active = False
        for ozone in self.ozones:
            for task in ozone.tasks:
                task.active = False
        for light in self.lights:
            for task in light.tasks:
                task.active = False

    def update(self, current_time):
        self.current_time = current_time

        # MFCs
        for wire_id, mfc in self.wire_map.items():
            for task in mfc.tasks:
                self.check_task(mfc, task, current_time, wire_id)

        # Pumps
        for pump in self.pumps:
            for task in pump.tasks:
                self.check_task(pump, task, current_time)

        # Lights
        for light in self.lights:
            for task in light.tasks:
                self.check_task(light, task, current_time)

        for ozone in self.ozones:
            for task in ozone.tasks:
                self.check_task(ozone, task, current_time)
        
    def check_task(self, device, task, current_time, wire_id=None):

        if not task.active and task.start_time <= current_time < task.stop_time:
            task.active = True
            if isinstance(device, MFC):
                self.start_mfc_task(device, task, wire_id)
            elif isinstance(device, Pump):
                self.start_pump_task(device, task)
            elif isinstance(device, Light):
                self.start_light_task(device, task)
            elif isinstance(device, Ozone):
                self.start_ozone_task(device, task)

        if task.active and current_time >= task.stop_time:
            task.active = False
            if isinstance(device, MFC):
                self.stop_mfc_task(device, task, wire_id)
            elif isinstance(device, Pump):
                self.stop_pump_task(device, task)
            elif isinstance(device, Light):
                self.stop_light_task(device, task)
            elif isinstance(device, Ozone):
                self.stop_ozone_task(device, task)

    def start_mfc_task(self, mfc, task, wire_id=None):
        slpm = max(0.0, min(task.flow_rate, 10.0))
        self.backend.send_mfc_command(slpm, mfc.ser)

        self.log(f"[START] {mfc.name} wire={wire_id} flow={slpm}")

    def stop_mfc_task(self, mfc, task, wire_id):
        voltage = self.SAFE_SLPM / 10.0

        self.backend.write_voltage(wire_id, voltage)

        self.log(f"[STOP] {mfc.name} wire={wire_id}")
    
    def start_pump_task(self, pump, task):
        self.backend.write_pump(True, task.flow_rate, task.duration, pump.volume, pump.ser)
        self.log(f"[START] {pump.name} rate={task.flow_rate}")
    
    def stop_pump_task(self, pump, task):
        #self.backend.write_pump(False, task.flow_rate, task.duration)
        self.log(f"[STOP] {pump.name}")

    def start_light_task(self, light, task):
        self.log(f"[START] lights config={task.config}")
        self.backend.write_lights(task.config, True)
    
    def stop_light_task(self, light, task):
        self.log(f"[STOP] lights config={task.config}")
        self.backend.write_lights(task.config, False)

    def start_ozone_task(self, ozone, task):
        self.backend.write_ozone(True)
        self.log(f"[START] ozone")
    
    def stop_ozone_task(self, ozone, task):
        self.backend.write_ozone(False)
        self.log(f"[STOP] ozone")

    def remove_mfc(self, mfc):
        if mfc in self.mfcs:
            self.mfcs.remove(mfc)

        for wire, device in list(self.wire_map.items()):
            if device == mfc:
                del self.wire_map[wire]


    def remove_pump(self, pump):
        if pump in self.pumps:
            self.pumps.remove(pump)


    def remove_light(self, light):
        if light in self.lights:
            self.lights.remove(light)


    def remove_ozone(self, ozone):
        if ozone in self.ozones:
            self.ozones.remove(ozone)
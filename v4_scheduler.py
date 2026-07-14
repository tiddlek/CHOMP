from v4_devices import MFC, Pump, Ozone, Light

class TaskScheduler:
    def __init__(self, daq_backend):
        self.mfcs = []
        self.pumps = []
        self.lights = []
        self.current_time = 0
        self.wire_map = {}
        self.SAFE_SLPM = 3.5
        self.log_callback = None

        # dependency injection (important part)
        self.daq = daq_backend

    def log(self, message):
        if self.log_callback is not None:
            self.log_callback(message)

    def add_mfc(self, mfc):
        self.mfcs.append(mfc)

    def register_mfc_wire(self, mfc, wire_id):
        if wire_id in self.wire_map:
            raise ValueError(
                f"Wire {wire_id} already assigned to {self.wire_map[wire_id].name}"
            )

        for w, existing in list(self.wire_map.items()):
            if existing == mfc:
                del self.wire_map[w]

        self.wire_map[wire_id] = mfc
        mfc.wire = wire_id

    def add_pump(self, pump):
        self.pumps.append(pump)
    
    def add_light(self, light):
        self.lights.append(light)

    def reset(self):
        self.current_time = 0
        for mfc in self.mfcs:
            for task in mfc.tasks:
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
        
    def check_task(self, device, task, current_time, wire_id=None):

        if not task.active and task.start_time <= current_time < task.stop_time:
            task.active = True
            if isinstance(device, MFC):
                self.start_mfc_task(device, task, wire_id)
            elif isinstance(device, Pump):
                self.start_pump_task(device, task)

        if task.active and current_time >= task.stop_time:
            task.active = False
            if isinstance(device, MFC):
                self.stop_mfc_task(device, task, wire_id)
            elif isinstance(device, Pump):
                self.stop_pump_task(device, task)

    def start_mfc_task(self, mfc, task, wire_id=None):
        slpm = max(0.0, min(task.flow_rate, 10.0))
        voltage = slpm / 10.0

        self.daq.write_voltage(wire_id, voltage)

        self.log(f"[START] {mfc.name} wire={wire_id} flow={slpm}")

    def stop_mfc_task(self, mfc, task, wire_id):
        voltage = self.SAFE_SLPM / 10.0

        self.daq.write_voltage(wire_id, voltage)

        self.log(f"[STOP] {mfc.name} wire={wire_id}")
    
    def start_pump_task(self, pump, task):
        self.log(f"[START] {pump.name} rate={task.flow_rate}")
    
    def stop_pump_task(self, pump, task):
        self.log(f"[STOP] {pump.name} rate={task.flow_rate}")

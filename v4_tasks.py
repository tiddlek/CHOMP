class MFCTask:
    def __init__(self, flow_rate=0.0, start_time=0.0, stop_time=0.0):
        self.flow_rate = flow_rate
        self.start_time = start_time
        self.stop_time = stop_time
        self.active = False

    def set_start(self, start_time):
        self.start_time = start_time

    def set_stop(self, stop_time):
        self.stop_time = stop_time

    def set_flow_rate(self, flow_rate):
        self.flow_rate = flow_rate

class PumpTask:
    def __init__(self, flow_rate, start_time, duration):
        self.flow_rate = flow_rate
        self.start_time = start_time
        self.duration = duration
        self.stop_time = start_time + duration
        self.active = False
    
    def set_start(self, start_time):
        self.start_time = start_time

    def set_stop(self, duration):
        self.duration = duration

    def set_flow_rate(self, flow_rate):
        self.flow_rate = flow_rate


class LightsTask:
    def __init__(self, start_time, stop_time, config):
        self.config = config
        self.start_time = start_time
        self.stop_time = stop_time
        self.active = False

    def set_start(self, start_time):
        self.start_time = start_time

    def set_stop(self, stop_time):
        self.stop_time = stop_time

    def set_config(self, config):
        self.config = config

class OzoneTask:
    def __init__(self, start_time, stop_time):
        self.start_time = start_time
        self.stop_time = stop_time
        self.active = False

    def set_start(self, start_time):
        self.start_time = start_time

    def set_stop(self, stop_time):
        self.stop_time = stop_time


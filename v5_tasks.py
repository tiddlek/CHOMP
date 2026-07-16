from abc import ABC

class Task(ABC):
    def __init__(self, start_time=0.0, stop_time=0.0):
        self.start_time = start_time
        self.stop_time = stop_time
        self.active = False

    def set_start(self, start_time):
        self.start_time = start_time

    def set_stop(self, stop_time):
        self.stop_time = stop_time
    
    def to_dict(self):
        return {
            "start_time": self.start_time,
            "stop_time": self.stop_time
        }

class MFCTask(Task):
    def __init__(self, flow_rate=0.0, start_time=0.0, stop_time=0.0):
        super().__init__(start_time, stop_time)
        self.flow_rate = flow_rate

    def set_flow_rate(self, flow_rate):
        self.flow_rate = flow_rate
    
    def to_dict(self):
        data = super().to_dict()
        data["flow_rate"] = self.flow_rate
        return data

class PumpTask(Task):
    def __init__(self, flow_rate=0.0, start_time=0.0, duration=0.0, volume=0.0):
        super().__init__(start_time, start_time + duration)
        self.flow_rate = flow_rate
        self.duration = duration
        self.volume = volume

    def set_flow_rate(self, flow_rate):
        self.flow_rate = flow_rate

    def set_duration(self, duration):
        self.duration = duration
        self.stop_time = self.start_time + duration

    def set_start(self, start_time):
        super().set_start(start_time)
        self.stop_time = start_time + self.duration
    
    def to_dict(self):
        data = super().to_dict()
        data["flow_rate"] = self.flow_rate
        data["duration"] = self.duration
        data["volume"] = self.volume
        return data
    
class LightTask(Task):
    def __init__(self, start_time=0.0, stop_time=0.0, config=None):
        super().__init__(start_time, stop_time)
        self.config = config

    def set_config(self, config):
        self.config = config

    def to_dict(self):
        data = super().to_dict()
        data["config"] = self.config
        return data
    
class OzoneTask(Task):
    def __init__(self, start_time=0.0, stop_time=0.0):
        super().__init__(start_time, stop_time)
    
    def to_dict(self):
        data = super().to_dict()
        return data
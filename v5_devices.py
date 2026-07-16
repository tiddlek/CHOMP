from abc import ABC

class Chamber:
    def __init__(self, name):
        self.name = name

        self.mfcs = []
        self.pumps = []

        self.light = Light()
        self.light.chamber = self

        self.ozone = Ozone()
        self.ozone.chamber = self

    def add_mfc(self, mfc):
        mfc.chamber = self
        self.mfcs.append(mfc)

    def add_pump(self, pump):
        pump.chamber = self
        self.pumps.append(pump)

    def delete_mfc(self, index):
        if 0 <= index < len(self.mfcs):
            self.mfcs.pop(index)

    def delete_pump(self, index):
        if 0 <= index < len(self.pumps):
            self.pumps.pop(index)
    
    def to_dict(self):
        return {
            "name": self.name,

            "mfcs": [
                mfc.to_dict()
                for mfc in self.mfcs
            ],

            "pumps": [
                pump.to_dict()
                for pump in self.pumps
            ],

            "light": self.light.to_dict(),

            "ozone": self.ozone.to_dict()
        }

class Device(ABC):
    def __init__(self, name):
        self.name = name
        self.tasks = []
        self.chamber = None

    def add_task(self, task):
        self.tasks.append(task)

    def delete_task(self, index):
        if 0 <= index < len(self.tasks):
            del self.tasks[index]
    
    def to_dict(self):
        return {
            "name": self.name,
            "tasks": [
                task.to_dict()
                for task in self.tasks
            ]
        }

class MFC(Device):
    def __init__(self, name):
        super().__init__(name)
        self.wire = ""

    def to_dict(self):
        data = super().to_dict()

        data["type"] = "MFC"
        data["wire"] = self.wire

        return data

class Pump(Device):
    def __init__(self, name, volume=None, diameter=None):
        super().__init__(name)
        self.volume = volume
        self.diameter = diameter
    
    def to_dict(self):
        data = super().to_dict()

        data["type"] = "Pump"
        data["volume"] = self.volume
        data["diameter"] = self.diameter

        return data

class Light(Device):
    def __init__(self, name="Lights"):
        super().__init__(name)
    
    def to_dict(self):
        data = super().to_dict()
        data["type"] = "Light"
        return data

class Ozone(Device):
    def __init__(self, name="Ozone Generator"):
        super().__init__(name)
    
    def to_dict(self):
        data = super().to_dict()
        data["type"] = "Ozone"
        return data
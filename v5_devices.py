from abc import ABC
from v5_tasks import *

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
    
    @classmethod
    def from_dict(cls, data):

        chamber = cls(data["name"])

        for mfc_data in data.get("mfcs", []):
            mfc = MFC.from_dict(mfc_data)
            chamber.add_mfc(mfc)

        for pump_data in data.get("pumps", []):
            pump = Pump.from_dict(pump_data)
            chamber.add_pump(pump)

        chamber.light = Light.from_dict(data["light"])
        chamber.ozone = Ozone.from_dict(data["ozone"])

        return chamber

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

    @classmethod
    def from_dict(cls, data):

        mfc = cls(data["name"])

        mfc.wire = data.get("wire")

        for task_data in data.get("tasks", []):
            task = MFCTask.from_dict(task_data)
            mfc.add_task(task)

        return mfc

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
    
    @classmethod
    def from_dict(cls, data):

        pump = cls(
            name=data["name"],
            volume=data.get("volume"),
            diameter=data.get("diameter")
        )

        for task_data in data.get("tasks", []):
            task = PumpTask.from_dict(task_data)
            pump.add_task(task)
        
        return pump

class Light(Device):
    def __init__(self, name="Lights"):
        super().__init__(name)
    
    def to_dict(self):
        data = super().to_dict()
        data["type"] = "Light"
        return data

    @classmethod
    def from_dict(cls, data):

        light = cls(data["name"])

        for task_data in data.get("tasks", []):
            task = LightTask.from_dict(task_data)
            light.add_task(task)

        return light

class Ozone(Device):
    def __init__(self, name="Ozone Generator"):
        super().__init__(name)
    
    def to_dict(self):
        data = super().to_dict()
        data["type"] = "Ozone"
        return data

    @classmethod
    def from_dict(cls, data):

        ozone = cls(data["name"])

        for task_data in data.get("tasks", []):
            task = OzoneTask.from_dict(task_data)
            ozone.add_task(task)

        return ozone
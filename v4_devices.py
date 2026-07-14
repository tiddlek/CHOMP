class MFC:
    def __init__(self, name):
        self.name = name
        self.tasks = []
        self.wire = ""

    def add_task(self, task):
        self.tasks.append(task)

    def delete_task(self, index):
        if 0 <= index < len(self.tasks):
            del self.tasks[index]

class Pump:
    def __init__(self, name, volume):
        self.name = name
        self.tasks = []
    
    def add_task(self, task):
        self.tasks.append(task)
    
    def delete_task(self, index):
        if 0 <= index < len(self.tasks):
            del self.tasks[index]


class Light:
    def __init__(self, name):
        self.name = name
        self.tasks = []
    
    def add_task(self, task):
        self.tasks.append(task)
    
    def delete_task(self, index):
        if 0 <= index < len(self.tasks):
            del self.tasks[index]


class Ozone:
    def __init__(self, name):
        self.name = name
        self.tasks = []
    
    def add_task(self, task):
        self.tasks.append(task)
    
    def delete_task(self, index):
        if 0 <= index < len(self.tasks):
            del self.tasks[index]

class Chamber:
    def __init__(self, name):
        self.name = name
        self.mfcs = []
        self.pumps = []
        self.light = Light(f"Lights")
        self.ozone = Ozone(f"Ozone Generator")
        self.pump_count = 0
        self.mfc_count = 0
        self.light_count = 0

    def add_mfc(self, mfc):
        self.mfcs.append(mfc)
    
    def add_pump(self, pump):
        self.pumps.append(pump)

    def delete_mfc(self, index):
        if 0 <= index < len(self.mfcs):
            del self.mfcs[index]

    def delete_pump(self, index):
        if 0 <= index < len(self.pumps):
            del self.pumps[index]

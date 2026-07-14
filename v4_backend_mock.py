class MockDAQBackend:
    def write_voltage(self, wire_id, voltage):
        pass
    
    def write_lights(self, config, on):
        pass
    
    def write_ozone(self):
        pass
    
    def write_pump(self, rate):
        pass
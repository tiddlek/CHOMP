class MockDAQBackend:
    def write_voltage(self, wire_id, voltage):
        print(f"[MOCK DAQ] wire={wire_id} voltage={voltage:.3f}")
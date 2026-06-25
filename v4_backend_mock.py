import logging
logger = logging.getLogger(__name__)

class MockDAQBackend:
    def write_voltage(self, wire_id, voltage):
        logging.info(f"[MOCK DAQ] wire={wire_id} voltage={voltage:.3f}")
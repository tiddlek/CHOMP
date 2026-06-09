import sys
import random
import nidaqmx

from PyQt6.QtWidgets import (
    QApplication,
    QCheckBox,
    QComboBox,
    QDateEdit,
    QDateTimeEdit,
    QDial,
    QDoubleSpinBox,
    QFontComboBox,
    QLabel,
    QLCDNumber,
    QLineEdit,
    QMainWindow,
    QProgressBar,
    QPushButton,
    QRadioButton,
    QSlider,
    QSpinBox,
    QTimeEdit,
    QVBoxLayout,
    QWidget,
)
from PyQt6.QtCore import QTimer
from nidaqmx.constants import TerminalConfiguration

def systemCheck():
    system = nidaqmx.system.System.local()
    for device in system.devices:   
        print(device.name, device.product_type)

class SimpleApp(QWidget):
    def __init__(self):
        super().__init__()

        self.setWindowTitle("Read/Write MFC")

        # Labels
        self.read_label = QLabel("Read")
        self.write_label = QLabel("Write")

        # Text boxes
        self.read_box = QLineEdit()
        self.write_box = QLineEdit()
        self.read_box.setReadOnly(True)
        self.submit_button = QPushButton("Setpoint")
        self.submit_button.clicked.connect(self.write_ao)
        self.light_toggle = QCheckBox("Lights ON/OFF")
        self.light_toggle.stateChanged.connect(self.toggle_light)
        

        # Layout
        layout = QVBoxLayout()
        layout.addWidget(self.read_label)
        layout.addWidget(self.read_box)
        layout.addWidget(self.write_label)
        layout.addWidget(self.write_box)
        layout.addWidget(self.submit_button)
        layout.addWidget(self.light_toggle)

        self.setLayout(layout)

        # Creates read task
        
        self.ai_task = nidaqmx.Task()
        self.ai_task.ai_channels.add_ai_voltage_chan(
            "Dev1/ai3", terminal_config=TerminalConfiguration.RSE
        )  # voltage from pin 6
        
        self.ao_task = nidaqmx.Task()
        self.ao_task.ao_channels.add_ao_voltage_chan("Dev1/ao0")

        self.do_task = nidaqmx.Task()
        self.do_task.do_channels.add_do_chan("Dev1/port0/line8")

        self.timer = QTimer()
        self.timer.timeout.connect(self.update_read)
        self.timer.start(100)  # update every 100 ms (10 Hz)

    def update_read(self):
        # Replace this with DAQ reading
        #value = random.uniform(0, 5)
        #self.read_box.setText(f"{value:.2f}")

        # Runs read task
        
        try:
            # Read AI channel
            ai_value = self.ai_task.read(number_of_samples_per_channel=1)
            self.read_box.setText(f"{ai_value[0]*10}")
        except nidaqmx.DaqError as e:
            self.read_box.setText(f"DAQ Error: {e}")
        
    def write_ao(self):
        try:
            print("Button pressed")
            slpm = float(self.write_box.text())
            print(slpm)

            # Example conversion: 0–50 SLPM maps to 0–5 V
            voltage = slpm/10

            self.ao_task.write(voltage)

        except ValueError:
            self.read_box.setText("Invalid number")
        except nidaqmx.DaqError as e:
            self.read_box.setText(f"DAQ Error: {e}")

    def toggle_light(self):
        try:
            if self.light_toggle.isChecked():
                self.do_task.write(True)   # relay ON
                self.light_toggle.setText("Lights ON")
            else:
                self.do_task.write(False)  # relay OFF
                self.light_toggle.setText("Lights OFF")

        except nidaqmx.DaqError as e:
            self.read_box.setText(f"DAQ Error: {e}")

def main():
    #check = systemCheck()
    app = QApplication(sys.argv)
    window = SimpleApp()
    window.show()
    sys.exit(app.exec())

main()
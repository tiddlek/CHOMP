import os
import sys
import nidaqmx
import pyqtgraph as pg
from v4_styles import *
from datetime import datetime
from pyqtgraph import AxisItem
from PyQt6.QtCore import Qt, QSize, QTimer
from PyQt6.QtWidgets import (
    QApplication, QMainWindow, QWidget,
    QVBoxLayout, QHBoxLayout, QPushButton,
    QStackedWidget, QLabel, QButtonGroup,
    QLineEdit, QToolButton, QGraphicsPathItem,
    QTableWidget, QTableWidgetItem, QMessageBox, QPlainTextEdit)
from PyQt6.QtGui import (QFont, QPainterPath, QFontDatabase, QIcon, QPixmap)

from v4_backend_daq import NI_DAQBackend
from v4_backend_mock import MockDAQBackend
from v4_scheduler import TaskScheduler

class MainWindow(QMainWindow):
    def __init__(self, scheduler):
        super().__init__()

        self.setup_window()
        self.scheduler = scheduler
        self.timer = QTimer()
        self.timer.timeout.connect(self.update_stopwatch)

        self.elapsed_seconds = 0
        self.is_running = False

        self.create_pages()
        self.create_navbar()
        self.setup_layout()
    def setup_window(self):
        
        self.setWindowTitle("CHOMP")
        self.resize(1140,760)

        self.central = QWidget()
        self.setCentralWidget(self.central) 
        self.central.setStyleSheet(APP_BACKGROUND)


        self.main_layout = QVBoxLayout(self.central)

    def create_navbar(self):
        self.nav_bar = QHBoxLayout()

        self.btn_1 = QPushButton("CHOMP")
        self.btn_2 = QPushButton("Chambers")
        self.btn_3 = QPushButton("Log")

        self.run = QPushButton("Run")
        self.reset = QPushButton("Reset")
        self.pause = QPushButton("Pause")
        self.stopwatch = QLabel("00:00:00")
        
        self.run.setStyleSheet(RUN_BUTTON)
        self.reset.setStyleSheet(RESET_BUTTON)
        self.stopwatch.setStyleSheet(STOPWATCH)
        self.pause.setStyleSheet(PAUSE_BUTTON)

        self.nav_bar.addWidget(self.btn_1)
        self.nav_bar.addSpacing(60)
        self.nav_bar.addWidget(self.btn_2)
        self.nav_bar.addSpacing(30)
        self.nav_bar.addWidget(self.btn_3)
        self.nav_bar.addSpacing(100)

        self.nav_bar.addWidget(self.run)
        self.nav_bar.addWidget(self.stopwatch)
        self.nav_bar.addWidget(self.pause)
        self.nav_bar.addWidget(self.reset)

        self.run.clicked.connect(self.start_timer)
        self.pause.clicked.connect(self.pause_timer)
        self.reset.clicked.connect(self.reset_timer)

        self.btn_1.clicked.connect(lambda: self.stack.setCurrentIndex(0))
        self.btn_2.clicked.connect(lambda: self.stack.setCurrentIndex(1))
        self.btn_3.clicked.connect(lambda: self.stack.setCurrentIndex(2))

        self.group = QButtonGroup()

        self.group.addButton(self.btn_1, 0)
        self.group.addButton(self.btn_2, 1)
        self.group.addButton(self.btn_3, 2)

        self.group.setExclusive(True)

        self.group.idClicked.connect(self.stack.setCurrentIndex)
        
        self.btn_1.setCheckable(True)
        self.btn_2.setCheckable(True)
        self.btn_3.setCheckable(True)

        self.btn_1.setStyleSheet(LOGO_BUTTON)

        self.btn_2.setStyleSheet(NAV_BUTTON)
        self.btn_3.setStyleSheet(NAV_BUTTON)

        self.nav_bar.setAlignment(Qt.AlignmentFlag.AlignLeft)
        self.nav_bar.setContentsMargins(60, 30, 40, 0)

    def create_pages(self):
        self.stack = QStackedWidget()

        self.chambers_page = ChambersPage(self.scheduler)
        self.log_page = LogPage()

        self.scheduler.log_callback = self.log_page.append

        self.stack.addWidget(HomePage())
        self.stack.addWidget(self.chambers_page)
        self.stack.addWidget(self.log_page)
        self.stack.setCurrentIndex(0)

    def setup_layout(self):
        self.main_layout.addLayout(self.nav_bar)
        self.main_layout.addWidget(self.stack)

    def start_timer(self):
        if not self.is_running:
            timestamp = datetime.now().strftime("%H:%M:%S")
            hrs = self.scheduler.current_time // 3600
            mins = (self.scheduler.current_time % 3600) // 60
            secs = self.scheduler.current_time % 60
            elapsedstamp = f"{hrs:02d}:{mins:02d}:{secs:02d}"

            self.scheduler.log(
                f"[RUN]"
                f"[{elapsedstamp}]"
                f"[{timestamp}]"          
            )
            self.timer.start(1000)  # 1 second
            self.is_running = True

    def pause_timer(self):
        if self.is_running:
            self.timer.stop()
            self.is_running = False

            timestamp = datetime.now().strftime("%H:%M:%S")
            hrs = self.elapsed_seconds // 3600
            mins = (self.elapsed_seconds % 3600) // 60
            secs = self.elapsed_seconds % 60

            elapsedstamp = f"{hrs:02d}:{mins:02d}:{secs:02d}"
            self.scheduler.log(
                "[PAUSE] Timer pasued"
                f"[{elapsedstamp}]"
                f"[{timestamp}]"
                )

    def reset_timer(self):
        self.elapsed_seconds = 0
        self.update_display()
        self.scheduler.reset()

        timestamp = datetime.now().strftime("%H:%M:%S")
        hrs = self.elapsed_seconds // 3600
        mins = (self.elapsed_seconds % 3600) // 60
        secs = self.elapsed_seconds % 60

        elapsedstamp = f"{hrs:02d}:{mins:02d}:{secs:02d}"
        self.scheduler.log(
            "[RESET] Timer reset"
            f"[{elapsedstamp}]"
            f"[{timestamp}]"
            )

    def update_stopwatch(self):
            self.elapsed_seconds += 1
            self.update_display()

            self.scheduler.update(self.elapsed_seconds)

    def update_display(self):
        hrs = self.elapsed_seconds // 3600
        mins = (self.elapsed_seconds % 3600) // 60
        secs = self.elapsed_seconds % 60

        self.stopwatch.setText(f"{hrs:02d}:{mins:02d}:{secs:02d}")

class HomePage(QWidget):
    def __init__(self):
        super().__init__()
        layout = QVBoxLayout(self)

        title = QLabel("CHOMP")
        title.setAlignment(Qt.AlignmentFlag.AlignCenter)
        title.setStyleSheet(f"font-size: 62px; font-weight: bold; color: {BLUE};")

        subtitle = QLabel("atmospheriC cHamber\nautOMation Platform")
        subtitle.setAlignment(Qt.AlignmentFlag.AlignCenter)
        subtitle.setStyleSheet("font-size: 24px; font-weight: regular; color: black;")

        layout.addStretch()
        layout.addWidget(title)
        layout.addWidget(subtitle)
        layout.addStretch()

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

class PumpTask:
    def __init__(self, flow_rate, start_time, duration):
        self.flow_rate = flow_rate
        self.start_time = start_time
        self.duration = duration
        self.active = False
    
    def set_start(self, start_time):
        self.start_time = start_time

    def set_stop(self, duration):
        self.duration = duration

    def set_flow_rate(self, flow_rate):
        self.flow_rate = flow_rate
    
class Pump:
    def __init__(self, name, volume):
        self.name = name
        self.tasks = []
    
    def add_task(self, task):
        self.tasks.append(task)
    
    def delete_task(self, index):
        if 0 <= index < len(self.tasks):
            del self.tasks[index]

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

class Light:
    def __init__(self, name):
        self.name = name
        self.tasks = []
    
    def add_task(self, task):
        self.tasks.append(task)
    
    def delete_task(self, index):
        if 0 <= index < len(self.tasks):
            del self.tasks[index]

class OzoneTask:
    def __init__(self, start_time, stop_time):
        self.start_time = start_time
        self.stop_time = stop_time
        self.active = False

    def set_start(self, start_time):
        self.start_time = start_time

    def set_stop(self, stop_time):
        self.stop_time = stop_time

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

class TimeInput(QWidget):
    def __init__(self, label_text):
        super().__init__()

        layout = QHBoxLayout(self)

        self.label = QLabel(label_text)

        self.time = QLineEdit()

        self.time.setStyleSheet(LINE_EDIT)

        self.units = QLabel("sec")

        layout.addWidget(self.label)
        layout.addWidget(self.time)
        layout.addWidget(self.units)

        layout.setContentsMargins(0, 0, 0, 0)
        layout.addStretch()

class FlowInput(QWidget):
    def __init__(self, label_text):
        super().__init__()

        layout = QHBoxLayout(self)

        self.label = QLabel(label_text)

        self.time = QLineEdit()
        self.time.setStyleSheet(LINE_EDIT)
        if label_text == "Flow":
            self.slpm_unit = QLabel("SLPM")
        elif label_text == "Rate":
            self.slpm_unit = QLabel("\u00B5L/sec")
    
        layout.addWidget(self.label)
        layout.addWidget(self.time)
        layout.addWidget(self.slpm_unit)
        layout.addStretch()
        layout.setContentsMargins(0, 0, 0, 0)

class ChamberWindow(QWidget):
    def __init__(self, chamber, button, scheduler, chambers_page):
        super().__init__()
        self.setStyleSheet(f"background-color: {BACKGROUND};")
        self.mfc_windows = []
        self.pump_windows = []
        self.light_windows = []
        self.ozone_windows = []
        self.chambers_page = chambers_page
        self.chamber = chamber
        self.button = button
        self.scheduler = scheduler
        self.scheduler.add_light(chamber.light)
        self.setWindowTitle(chamber.name)
        self.resize(900,760)

        layout = QVBoxLayout(self)

        top = QHBoxLayout()
        delete = QPushButton("Delete Chamber")
        delete.setStyleSheet(RESET_BUTTON)

        title1 = QLabel(self.chamber.name.upper())
        title1.setStyleSheet(PAGE_TITLE)
        
        title0 = QLabel("Ozone Generator")
        title0.setStyleSheet(PAGE_TITLE)
        self.line0 = QHBoxLayout()
        self.ozone_generator = QToolButton()
        self.ozone_generator.setStyleSheet(MFC_BUTTON)
        self.ozone_generator.setFixedSize(100, 100)
        self.ozone_generator.setText("O\u2083")
        self.line0.addWidget(self.ozone_generator)

        self.ozone_generator.setIcon(QIcon(resource_path("imgs/ozone.png")))
        self.ozone_generator.setIconSize(QSize(90, 90))
        self.ozone_generator.setToolButtonStyle(
            Qt.ToolButtonStyle.ToolButtonTextUnderIcon
        )

        self.ozone_generator.clicked.connect(lambda: self.open_ozone(chamber.ozone, self.ozone_generator))

        title2 = QLabel("Lights")
        title2.setStyleSheet(PAGE_TITLE)
        self.line2 = QHBoxLayout()
        self.lights = QToolButton()
        self.lights.setStyleSheet(MFC_BUTTON)
        self.lights.setFixedSize(100, 100)
        self.lights.setText("h\u03BD")
        

        self.line2.addWidget(self.lights)

        self.lights.setIcon(QIcon(resource_path("imgs/lights.png")))
        self.lights.setIconSize(QSize(75, 75))
        self.lights.setToolButtonStyle(
            Qt.ToolButtonStyle.ToolButtonTextUnderIcon
        )
        self.lights.clicked.connect(lambda: self.open_light(chamber.light, self.lights))

        title3 = QLabel("MFCs")
        title3.setStyleSheet(PAGE_TITLE)
        self.line3 = QHBoxLayout()
        self.add_mfc_btn = QToolButton()
        self.add_mfc_btn.setStyleSheet(MFC_ADD_BUTTON)
        self.add_mfc_btn.setText("+\nMFC")
        self.add_mfc_btn.setFixedSize(100, 100)
        self.add_mfc_btn.clicked.connect(self.add_mfc)
        self.line3.addWidget(self.add_mfc_btn)

        title4 = QLabel("Syringe Pumps")
        title4.setStyleSheet(PAGE_TITLE)

        self.line4 = QHBoxLayout()
        self.add_pump_btn = QToolButton()
        self.add_pump_btn.setStyleSheet(MFC_ADD_BUTTON)
        self.add_pump_btn.setText("+\nPump")
        self.add_pump_btn.setFixedSize(100, 100)
        self.line4.addWidget(self.add_pump_btn)

        self.add_pump_btn.clicked.connect(self.add_pump)

        for pump in self.chamber.pumps:
            self.create_pump_button(pump)

        for mfc in self.chamber.mfcs:
            self.create_mfc_button(mfc)

        self.line0.setAlignment(Qt.AlignmentFlag.AlignLeft)
        self.line2.setAlignment(Qt.AlignmentFlag.AlignLeft)
        self.line3.setAlignment(Qt.AlignmentFlag.AlignLeft)
        self.line4.setAlignment(Qt.AlignmentFlag.AlignLeft)

        layout.setContentsMargins(80, 60, 60, 30)
        layout.setAlignment(Qt.AlignmentFlag.AlignTop)
        
        top.addWidget(title1)
        top.addWidget(delete)
        top.addStretch()

        delete.clicked.connect(self.delete_chamber)

        layout.addLayout(top)
        layout.addWidget(title0)
        layout.addLayout(self.line0)
        layout.addWidget(title2)
        layout.addLayout(self.line2)
        layout.addWidget(title3)
        layout.addLayout(self.line3)
        layout.addWidget(title4)
        layout.addLayout(self.line4)
        layout.addStretch()

    def delete_chamber(self):

        reply = QMessageBox.question(
            self,
            "Delete Chamber",
            f"Delete {self.chamber.name}?",
            QMessageBox.StandardButton.Yes |
            QMessageBox.StandardButton.No
        )

        if reply != QMessageBox.StandardButton.Yes:
            return

        if self.chamber in self.chambers_page.chambers:
            self.chambers_page.chambers.remove(self.chamber)
        
        for mfc in self.chamber.mfcs:
            if mfc in self.scheduler.mfcs:
                self.scheduler.mfcs.remove(mfc)

            if mfc.wire in self.scheduler.wire_map:
                del self.scheduler.wire_map[mfc.wire]
        for win in self.mfc_windows:
            win.close()

        self.button.setParent(None)
        self.button.deleteLater()

        self.close()

    def closeEvent(self, event):
        self.button.setEnabled(True)
        event.accept()

    def create_mfc_button(self, mfc):
        btn = QToolButton()
        btn.setText(mfc.name)
        btn.setIcon(QIcon(resource_path("imgs/mfc.png")))
        btn.setIconSize(QSize(50, 50))
        btn.setToolButtonStyle(
            Qt.ToolButtonStyle.ToolButtonTextUnderIcon
        )

        btn.setFixedSize(100, 100)
        btn.setStyleSheet(MFC_BUTTON)

        btn.clicked.connect(
            lambda _, m=mfc, b=btn: self.open_mfc(m, b)
        )

        self.line3.insertWidget(
            self.line3.count() - 1,
            btn
        )

    def create_pump_button(self, pump):
        btn = QToolButton()
        btn.setText(pump.name)
        btn.setIcon(QIcon(resource_path("imgs/syringe.png")))
        btn.setIconSize(QSize(50, 50))
        btn.setToolButtonStyle(
            Qt.ToolButtonStyle.ToolButtonTextUnderIcon
        )

        btn.setFixedSize(100, 100)
        btn.setStyleSheet(MFC_BUTTON)

        btn.clicked.connect(
            lambda _, m=pump, b=btn: self.open_pump(m, b)
        )

        self.line4.insertWidget(
            self.line4.count() - 1,
            btn
        )

    def add_mfc(self):
        self.chamber.mfc_count += 1

        mfc = MFC(f"MFC {self.chamber.mfc_count}")
        self.chamber.add_mfc(mfc)
        self.window().scheduler.add_mfc(mfc)

        self.create_mfc_button(mfc)

    def add_pump(self):
        self.chamber.pump_count += 1

        pump = Pump(f"Pump {self.chamber.pump_count}", 5)
        self.chamber.add_pump(pump)
        self.window().scheduler.add_pump(pump)

        self.create_pump_button(pump)

    def open_mfc(self, mfc, button):
        win = MFCWindow(mfc, button, self.scheduler, self)
        self.mfc_windows.append(win)

        button.setEnabled(False)
        win.show()
    
    def open_pump(self, pump, button):
        win = PumpWindow(pump, button, self.scheduler, self)
        self.pump_windows.append(win)

        button.setEnabled(False)
        win.show()
    
    def open_light(self, light, button):
        win = LightsWindow(light, button, self.scheduler, self)
        self.light_windows.append(win)

        button.setEnabled(False)
        win.show()
    
    def open_ozone(self, ozone, button):
        win = OzoneWindow(ozone, button, self.scheduler, self)
        self.ozone_windows.append(win)

        button.setEnabled(False)
        win.show()

class MFCWindow(QWidget):
    def __init__(self, mfc, button, scheduler, chamber_window):
        super().__init__()
        self.setStyleSheet(f"background-color: {BACKGROUND};")
        self.mfc = mfc
        self.chamber_window = chamber_window
        self.button = button
        self.scheduler = scheduler

        self.resize(800,760)

        self.task_boxes = []
        self.graph = self.create_plot()

        layout = QVBoxLayout(self)

        middle_layout = QHBoxLayout()
        middle_layout.setAlignment(Qt.AlignmentFlag.AlignTop)

        self.left = self.create_left()
        self.right = self.create_right()
        self.header = self.create_header()

        header_widget = QWidget()
        header_widget.setLayout(self.header)

        left_widget = QWidget()
        left_widget.setLayout(self.left)

        right_widget = QWidget()
        right_widget.setLayout(self.right)

        layout.addWidget(header_widget)
        middle_layout.addWidget(left_widget, 1)
        middle_layout.addWidget(right_widget, 1)
       
        layout.addSpacing(20)
        layout.addLayout(middle_layout)

        layout.addSpacing(50)

        layout.addWidget(self.graph)
        
        if self.mfc.wire == 1:
            self.mfc1.setChecked(True)
        elif self.mfc.wire == 2:
            self.mfc2.setChecked(True)
        elif self.mfc.wire == 3:
            self.mfc3.setChecked(True)
        
        self.load_tasks()
    
     
    def set_wire(self, wire):
        try:
            self.scheduler.register_mfc_wire(self.mfc, wire)
        except ValueError as e:
            QMessageBox.warning(self, "Wire Conflict", str(e))
            return

    def closeEvent(self, event):
        self.button.setEnabled(True)
        event.accept()

    def load_tasks(self):
        for task in self.mfc.tasks:
            self.add_task_to_ui(task)
    
    def create_header(self):
        header_layout = QHBoxLayout()
        title = QLabel(self.mfc.name)
        title.setStyleSheet(PAGE_TITLE)
        header_layout.setContentsMargins(40, 40, 0, 0)

        self.mfc1 = QPushButton("1")
        self.mfc2 = QPushButton("2")
        self.mfc3 = QPushButton("3")

        self.mfc1.setCheckable(True)
        self.mfc2.setCheckable(True)
        self.mfc3.setCheckable(True)

        self.mfc1.setFixedSize(28,28)
        self.mfc2.setFixedSize(28,28)
        self.mfc3.setFixedSize(28,28)

        self.mfc1.setStyleSheet(WIRE_BUTTON)
        self.mfc2.setStyleSheet(WIRE_BUTTON)
        self.mfc3.setStyleSheet(WIRE_BUTTON)

        if self.mfc.wire == 1:
            self.mfc1.setChecked(True)
        elif self.mfc.wire == 2:
            self.mfc2.setChecked(True)
        elif self.mfc.wire == 3:
            self.mfc3.setChecked(True)


        self.mfc_group = QButtonGroup(self)
        self.mfc_group.setExclusive(True)

        self.mfc_group.addButton(self.mfc1, 1)
        self.mfc_group.addButton(self.mfc2, 2)
        self.mfc_group.addButton(self.mfc3, 3)

        self.mfc_group.idClicked.connect(self.set_wire)

        delete = QPushButton("Delete MFC")
        delete.setStyleSheet(RESET_BUTTON)
        delete.clicked.connect(self.delete_mfc)

        header_layout.addWidget(title)
        header_layout.addSpacing(10)
        header_layout.addWidget(self.mfc1)
        header_layout.addWidget(self.mfc2)
        header_layout.addWidget(self.mfc3)
        header_layout.addWidget(delete)
        header_layout.addStretch()

        return header_layout
    
    def delete_mfc(self):

        if self.mfc.wire in self.scheduler.wire_map:
            del self.scheduler.wire_map[self.mfc.wire]

        if self.mfc in self.scheduler.mfcs:
            self.scheduler.mfcs.remove(self.mfc)

        if self.mfc in self.chamber_window.chamber.mfcs:
            self.chamber_window.chamber.mfcs.remove(self.mfc)

        self.chamber_window.line3.removeWidget(self.button)
        self.button.deleteLater()

        self.close()

    def create_left(self):    
        
        left_layout = QVBoxLayout()
        title = QLabel("Create Task")
        title.setStyleSheet(PAGE_TITLE)
        self.start_row = TimeInput("Start")
        self.stop_row = TimeInput("Stop")
        self.slpm_row = FlowInput("Flow")
        self.task_button = self.create_task_button()
        left_layout.setContentsMargins(40, 0, 20, 0)
        left_layout.setAlignment(Qt.AlignmentFlag.AlignTop)

        left_layout.addWidget(title)
        left_layout.addSpacing(6)
        left_layout.addWidget(self.start_row)
        left_layout.addSpacing(6)
        left_layout.addWidget(self.stop_row)
        left_layout.addSpacing(6)

        left_layout.addWidget(self.slpm_row)

        left_layout.addSpacing(5)
        left_layout.addWidget(self.task_button)

        return left_layout

    def create_right(self):
        
        right_layout = QVBoxLayout()
        right_layout.setAlignment(Qt.AlignmentFlag.AlignTop)

        title = QLabel("Task List")
        title.setStyleSheet(PAGE_TITLE)

        self.task_table = QTableWidget()
        self.task_table.setColumnCount(3)
        self.task_table.setHorizontalHeaderLabels(
            ["Start", "Stop", "SLPM"]
        )

        self.task_table.setFixedSize(336, 120)


        self.task_table.setStyleSheet(TABLE)

        self.task_table.setColumnWidth(0, 110)   # Start
        self.task_table.setColumnWidth(1, 110)   # Stop
        self.task_table.setColumnWidth(2, 112)   # SLPM
        self.task_table.verticalHeader().setVisible(False)
        self.task_table.setSelectionBehavior(QTableWidget.SelectionBehavior.SelectRows)
        self.task_table.setSelectionMode(QTableWidget.SelectionMode.SingleSelection)

        self.task_table.setStyleSheet(TABLE)

        self.delete_button = QPushButton("Delete Task")
        self.delete_button.setFixedHeight(30)
        self.delete_button.clicked.connect(self.delete_task)

        self.delete_button.setStyleSheet(ACTION_BUTTON)

        right_layout.setContentsMargins(20,0,40,0)
        right_layout.addStretch()
        right_layout.addWidget(title)
        right_layout.addWidget(self.task_table)

        right_layout.addSpacing(5)


        right_layout.addWidget(self.delete_button)

        return right_layout

    def create_task_button(self):

        button = QPushButton("Add Task")

        button.setFixedSize(270, 30)

        button.setStyleSheet(ACTION_BUTTON)

        button.clicked.connect(self.add_task)

        return button

    def create_plot(self):

        slpm_axis = AxisItem(orientation="left")

        slpm_ticks = [
            [(i, "") for i in range(0, 11)],
            [(i, str(i)) for i in range(0, 11, 2)]
        ]

        time_axis = AxisItem(orientation="bottom")

        time_ticks = [
            [(0, "0"),
            (20, "20"),
            (40, "40"),
            (60, "60"),
            (80, "80"),
            (100, "100"),
            (120, "120")],
            [(i, "") for i in range(0, 121, 10)]
        ]

        slpm_axis.setTicks(slpm_ticks)
        time_axis.setTicks(time_ticks)

        self.graph = pg.PlotWidget(
            axisItems={
                "left": slpm_axis,
                "bottom": time_axis
            }
        )


        self.graph.getAxis("bottom").setStyle(
            tickLength=5,
            tickTextOffset=8
        )

        self.graph.getAxis("left").setStyle(
            tickLength=5,
            tickTextOffset=8
        )

        self.graph.setBackground(BACKGROUND)
        self.graph.showGrid(x=False, y=False, alpha=1.0)
        self.graph.getAxis("left").setPen("k")
        self.graph.getAxis("bottom").setPen("k")

        self.graph.setLabel("left", "SLPM")
        self.graph.setLabel("bottom", "Time (seconds)")

        self.graph.setYRange(0, 10, padding=0)
        self.graph.setXRange(0, 120, padding=0)

        self.graph.getViewBox().setDefaultPadding(0)

        self.graph.getPlotItem().layout.setContentsMargins(10, 10, 20, 20)

        axis_pen = pg.mkPen(color="black", width=2)

        time_axis.setPen(axis_pen)
        slpm_axis.setPen(axis_pen)

        self.graph.getAxis("left").setTextPen("k")
        self.graph.getAxis("bottom").setTextPen("k")
        self.graph.setMouseEnabled(x=False, y=False)

        return self.graph

    def delete_task(self):
        row = self.task_table.currentRow()

        if row >= 0:
            # 1. remove from model FIRST
            if 0 <= row < len(self.mfc.tasks):
                self.mfc.delete_task(row)

            # 2. remove graph item
            box = self.task_boxes.pop(row)
            self.graph.removeItem(box)

            # 3. remove table row
            self.task_table.removeRow(row)

    def add_task(self):
        try:
            start = int(self.start_row.time.text())
            stop = int(self.stop_row.time.text())
            flow = float(self.slpm_row.time.text())

            if flow < 0:
                QMessageBox.warning(
                    self,
                    "Invalid Flow",
                    "Flow cannot be negative."
                )
                return

            if flow > 10:
                QMessageBox.warning(
                    self,
                    "Invalid Flow",
                    "Maximum flow is 10 SLPM."
                )
                return

            if start >= stop:
                raise ValueError("Start must be before stop")

        except ValueError as e:
            QMessageBox.warning(self, "Invalid Input", "Enter seconds in whole numbers")
            return
        
        if not self.mfc1.isChecked() and not self.mfc2.isChecked() and not self.mfc3.isChecked():
            QMessageBox.warning(
                self,
                "No Wire Selected",
                "Select a Wire."
            )
            return



        task = MFCTask(
            flow_rate=flow,
            start_time=start,
            stop_time=stop
        )

        self.mfc.add_task(task)
        self.add_task_to_ui(task)

        self.start_row.time.clear()
        self.stop_row.time.clear()
        self.slpm_row.time.clear()

        max_stop = max(
            (task.stop_time for task in self.mfc.tasks),
            default=120
        )

        self.graph.setXRange(
            0,
            max(120, max_stop * 1.05),
            padding=0
        )

    def draw_task_box(self, task):

        width = task.stop_time - task.start_time
        center = task.start_time + width / 2

        path = QPainterPath()
        path.addRoundedRect(
            center - width/2,
            0.05,
            width,
            task.flow_rate - 0.05,
            0.4,
            0.4
        )

        box = QGraphicsPathItem(path)

        box.setBrush(pg.mkBrush(BLUE))
        box.setPen(pg.mkPen(BACKGROUND, width=2))

        self.graph.addItem(box)
        self.task_boxes.append(box)

        return box

    def add_task_to_ui(self, task):
        row = self.task_table.rowCount()
        self.task_table.insertRow(row)

        self.task_table.setItem(
            row, 0,
            QTableWidgetItem(str(task.start_time))
        )

        self.task_table.setItem(
            row, 1,
            QTableWidgetItem(str(task.stop_time))
        )

        self.task_table.setItem(
            row, 2,
            QTableWidgetItem(
                str(task.flow_rate)
            )
        )

        self.draw_task_box(task)

class PumpWindow(QWidget):
    def __init__(self, pump, button, scheduler, chamber_window):
        super().__init__()
        self.setStyleSheet(f"background-color: {BACKGROUND};")
        self.pump = pump
        self.chamber_window = chamber_window
        self.button = button
        self.scheduler = scheduler

        self.resize(800,760)

        self.task_boxes = []
        self.graph = self.create_plot()

        layout = QVBoxLayout(self)

        middle_layout = QHBoxLayout()
        middle_layout.setAlignment(Qt.AlignmentFlag.AlignTop)

        self.left = self.create_left()
        self.right = self.create_right()
        self.header = self.create_header()

        header_widget = QWidget()
        header_widget.setLayout(self.header)

        left_widget = QWidget()
        left_widget.setLayout(self.left)

        right_widget = QWidget()
        right_widget.setLayout(self.right)

        layout.addWidget(header_widget)
        middle_layout.addWidget(left_widget, 1)
        middle_layout.addWidget(right_widget, 1)
       
        layout.addSpacing(20)
        layout.addLayout(middle_layout)

        layout.addSpacing(50)

        layout.addWidget(self.graph)
        
        self.load_tasks()
    
    def closeEvent(self, event):
        self.button.setEnabled(True)
        event.accept()

    def load_tasks(self):
        for task in self.pump.tasks:
            self.add_task_to_ui(task)
    
    def create_header(self):
        header_layout = QHBoxLayout()
        title = QLabel(self.pump.name)
        title.setStyleSheet(PAGE_TITLE)
        header_layout.setContentsMargins(40, 40, 0, 0)

        delete = QPushButton("Delete Pump")
        delete.setStyleSheet(RESET_BUTTON)
        delete.clicked.connect(self.delete_pump)

        header_layout.addWidget(title)
        header_layout.addSpacing(10)
        header_layout.addWidget(delete)
        header_layout.addStretch()

        return header_layout
    
    def delete_pump(self):

        if self.pump in self.scheduler.pumps:
            self.scheduler.pumps.remove(self.pump)

        if self.pump in self.chamber_window.chamber.pumps:
            self.chamber_window.chamber.pumps.remove(self.pump)

        self.chamber_window.line3.removeWidget(self.button)
        self.button.deleteLater()

        self.close()

    def create_left(self):    
        
        left_layout = QVBoxLayout()
        title = QLabel("Create Task")
        title.setStyleSheet(PAGE_TITLE)
        self.start_row = TimeInput("Start")
        self.duration = TimeInput("Duration")
        self.rate = FlowInput("Rate")
        self.task_button = self.create_task_button()
        left_layout.setContentsMargins(40, 0, 20, 0)
        left_layout.setAlignment(Qt.AlignmentFlag.AlignTop)

        self.volume = QLabel("Total Injection: Volume: ")

        self.start_row.time.textChanged.connect(self.calculate)
        self.duration.time.textChanged.connect(self.calculate)
        self.rate.time.textChanged.connect(self.calculate)

        left_layout.addWidget(title)
        left_layout.addSpacing(6)
        left_layout.addWidget(self.start_row)
        left_layout.addSpacing(6)
        left_layout.addWidget(self.duration)
        left_layout.addSpacing(6)

        left_layout.addWidget(self.rate)

        left_layout.addSpacing(5)
        left_layout.addWidget(self.volume)
        left_layout.addWidget(self.task_button)

  

        return left_layout
    
    def calculate(self):
            try:
                start = float(self.start_row.time.text())
                duration = float(self.duration.time.text())
                rate = float(self.rate.time.text())

                if duration > 0:
                    volume = duration * rate
                    self.volume.setText(f"Total Injection: Volume: {volume:.3f} \u00B5L")
                else:
                    self.volume.setText("Total Injection: Volume: --")
            except ValueError:
                self.volume.setText("Total Injection: Volume: --")


    def create_right(self):
        
        right_layout = QVBoxLayout()
        right_layout.setAlignment(Qt.AlignmentFlag.AlignTop)

        title = QLabel("Task List")
        title.setStyleSheet(PAGE_TITLE)

        self.task_table = QTableWidget()
        self.task_table.setColumnCount(3)
        self.task_table.setHorizontalHeaderLabels(
            ["Start", "Duration", "\u00B5L/sec"]
        )

        self.task_table.setFixedSize(336, 120)


        self.task_table.setStyleSheet(TABLE)

        self.task_table.setColumnWidth(0, 110)   # Start
        self.task_table.setColumnWidth(1, 110)   # Stop
        self.task_table.setColumnWidth(2, 112)   # SLPM
        self.task_table.verticalHeader().setVisible(False)
        self.task_table.setSelectionBehavior(QTableWidget.SelectionBehavior.SelectRows)
        self.task_table.setSelectionMode(QTableWidget.SelectionMode.SingleSelection)

        self.task_table.setStyleSheet(TABLE)

        self.delete_button = QPushButton("Delete Task")
        self.delete_button.setFixedHeight(30)
        self.delete_button.clicked.connect(self.delete_task)

        self.delete_button.setStyleSheet(ACTION_BUTTON)

        right_layout.setContentsMargins(20,0,40,0)
        right_layout.addStretch()
        right_layout.addWidget(title)
        right_layout.addWidget(self.task_table)

        right_layout.addSpacing(5)


        right_layout.addWidget(self.delete_button)

        return right_layout

    def create_task_button(self):

        button = QPushButton("Add Task")

        button.setFixedSize(270, 30)

        button.setStyleSheet(ACTION_BUTTON)

        button.clicked.connect(self.add_task)

        return button

    def create_plot(self):

        slpm_axis = AxisItem(orientation="left")

        slpm_ticks = [
            [(i, "") for i in [0, 0.2, 0.4, 0.6, 0.8, 1.0]],
            [(i, f"{i:.1f}") for i in [0, 0.2, 0.4, 0.6, 0.8, 1.0]]
        ]

        time_axis = AxisItem(orientation="bottom")

        time_ticks = [
            [(0, "0"),
            (20, "20"),
            (40, "40"),
            (60, "60"),
            (80, "80"),
            (100, "100"),
            (120, "120")],
            [(i, "") for i in range(0, 121, 10)]
        ]

        slpm_axis.setTicks(slpm_ticks)
        time_axis.setTicks(time_ticks)

        self.graph = pg.PlotWidget(
            axisItems={
                "left": slpm_axis,
                "bottom": time_axis
            }
        )


        self.graph.getAxis("bottom").setStyle(
            tickLength=5,
            tickTextOffset=8
        )

        self.graph.getAxis("left").setStyle(
            tickLength=5,
            tickTextOffset=8
        )

        self.graph.setBackground(BACKGROUND)
        self.graph.showGrid(x=False, y=False, alpha=1.0)
        self.graph.getAxis("left").setPen("k")
        self.graph.getAxis("bottom").setPen("k")

        self.graph.setLabel("left", "\u00B5L/sec")
        self.graph.setLabel("bottom", "Time (seconds)")

        self.graph.setYRange(0, 1, padding=0)
        self.graph.setXRange(0, 120, padding=0)

        self.graph.getViewBox().setDefaultPadding(0)

        self.graph.getPlotItem().layout.setContentsMargins(10, 10, 20, 20)

        axis_pen = pg.mkPen(color="black", width=2)

        time_axis.setPen(axis_pen)
        slpm_axis.setPen(axis_pen)

        self.graph.getAxis("left").setTextPen("k")
        self.graph.getAxis("bottom").setTextPen("k")
        self.graph.setMouseEnabled(x=False, y=False)

        return self.graph

    def delete_task(self):
        row = self.task_table.currentRow()

        if row >= 0:
            # 1. remove from model FIRST
            if 0 <= row < len(self.pump.tasks):
                self.pump.delete_task(row)

            # 2. remove graph item
            box = self.task_boxes.pop(row)
            self.graph.removeItem(box)

            # 3. remove table row
            self.task_table.removeRow(row)

    def add_task(self):
        try:
            start = int(self.start_row.time.text())
            duration = int(self.duration.time.text())
            flow = float(self.rate.time.text())

            if flow < 0:
                QMessageBox.warning(
                    self,
                    "Invalid Flow",
                    "Flow cannot be negative."
                )
                return

            if flow > 10:
                QMessageBox.warning(
                    self,
                    "Invalid Flow",
                    "Maximum flow is 10 SLPM."
                )
                return

            if duration < 1 or (duration % 1) != 0:
                raise ValueError("Duration must be a positive whole number")

        except ValueError as e:
            QMessageBox.warning(self, "Invalid Input", "Enter seconds in whole numbers")
            return

        task = PumpTask(
            flow_rate=flow,
            start_time=start,
            duration=duration
        )

        self.pump.add_task(task)
        self.add_task_to_ui(task)

        self.start_row.time.clear()
        self.duration.time.clear()
        self.rate.time.clear()

        max_stop = max(
            (task.duration for task in self.pump.tasks),
            default=120
        )

        self.graph.setXRange(
            0,
            max(120, max_stop * 1.05),
            padding=0
        )

    def draw_task_box(self, task):

        width = task.duration
        center = task.start_time + width / 2

        path = QPainterPath()
        path.addRoundedRect(
            center - width/2,
            0.005,
            width,
            task.flow_rate - 0.005,
            0.2,
            0.2
        )

        box = QGraphicsPathItem(path)

        box.setBrush(pg.mkBrush(BLUE))
        box.setPen(pg.mkPen(BACKGROUND, width=2))

        self.graph.addItem(box)
        self.task_boxes.append(box)

        return box

    def add_task_to_ui(self, task):
        row = self.task_table.rowCount()
        self.task_table.insertRow(row)

        self.task_table.setItem(
            row, 0,
            QTableWidgetItem(str(task.start_time))
        )

        self.task_table.setItem(
            row, 1,
            QTableWidgetItem(str(task.duration))
        )

        self.task_table.setItem(
            row, 2,
            QTableWidgetItem(
                str(task.flow_rate)
            )
        )

        self.draw_task_box(task)

class LightsWindow(QWidget):
    def __init__(self, lights, button, scheduler, chamber_window):
        super().__init__()
        self.setStyleSheet(f"background-color: {BACKGROUND};")
        self.lights = lights
        self.chamber_window = chamber_window
        self.button = button
        self.scheduler = scheduler

        self.resize(800,760)

        self.task_boxes = []
        self.graph_c = self.create_plot()
        self.graph_m = self.create_plot()

        layout = QVBoxLayout(self)

        middle_layout = QHBoxLayout()
        middle_layout.setAlignment(Qt.AlignmentFlag.AlignTop)

        self.left = self.create_left()
        self.right = self.create_right()
        self.header = self.create_header()

        header_widget = QWidget()
        header_widget.setLayout(self.header)

        left_widget = QWidget()
        left_widget.setLayout(self.left)

        right_widget = QWidget()
        right_widget.setLayout(self.right)

        layout.addWidget(header_widget)
        middle_layout.addWidget(left_widget, 1)
        middle_layout.addWidget(right_widget, 1)
       
        layout.addSpacing(20)
        layout.addLayout(middle_layout)

        layout.addSpacing(50)

        g_c = QHBoxLayout()
        g_m = QHBoxLayout()

        button = QToolButton()
        
        button.setIcon(QIcon(resource_path("imgs/middle.png")))

        button.setIconSize(QSize(100, 100))
        button.setFixedSize(50, 50)

        button.setToolButtonStyle(
            Qt.ToolButtonStyle.ToolButtonIconOnly
        )

        button.setStyleSheet(PLOT_BUTTON)

        g_c.addWidget(button, alignment=Qt.AlignmentFlag.AlignTop)

        g_c.addWidget(self.graph_c)

        button2 = QToolButton()

        button2.setIcon(QIcon(resource_path("imgs/corner.png")))

        button2.setIconSize(QSize(100, 100))
        button2.setFixedSize(50, 50)

        button2.setToolButtonStyle(
            Qt.ToolButtonStyle.ToolButtonIconOnly
        )

        button2.setStyleSheet(PLOT_BUTTON)

        g_m.addWidget(button2, alignment=Qt.AlignmentFlag.AlignTop)
        g_m.addWidget(self.graph_m)

        layout.addLayout(g_c)
        layout.addLayout(g_m)
        
        self.load_tasks()
    
    def closeEvent(self, event):
        self.button.setEnabled(True)
        event.accept()

    def load_tasks(self):
        for task in self.lights.tasks:
            self.add_task_to_ui(task)
    
    def create_header(self):
        header_layout = QHBoxLayout()
        title = QLabel(self.lights.name)
        title.setStyleSheet(PAGE_TITLE)
        header_layout.setContentsMargins(40, 40, 0, 0)

        delete = QPushButton("Delete lights")
        delete.setStyleSheet(RESET_BUTTON)
        delete.clicked.connect(self.delete_lights)

        header_layout.addWidget(title)
        header_layout.addSpacing(10)
        header_layout.addWidget(delete)
        header_layout.addStretch()

        return header_layout
    
    def delete_lights(self):

        if self.lights in self.scheduler.lightss:
            self.scheduler.lightss.remove(self.lights)

        if self.lights in self.chamber_window.chamber.lightss:
            self.chamber_window.chamber.lightss.remove(self.lights)

        self.chamber_window.line3.removeWidget(self.button)
        self.button.deleteLater()

        self.close()

    def create_left(self):    
        
        left_layout = QVBoxLayout()
        title = QLabel("Create Task")
        title.setStyleSheet(PAGE_TITLE)
        self.start_row = TimeInput("Start")
        self.stop_row = TimeInput("Stop")
        self.task_button = self.create_task_button()
        left_layout.setContentsMargins(40, 0, 20, 0)
        left_layout.setAlignment(Qt.AlignmentFlag.AlignTop)

        configs = QHBoxLayout()
        self.btn1 = QToolButton()
        self.btn2 = QToolButton()

        self.btn1.setStyleSheet(CONFIG_BUTTON)
        self.btn2.setStyleSheet(CONFIG_BUTTON)

        self.btn1.setFixedSize(100, 100)
        self.btn2.setFixedSize(100, 100)

        self.btn1.setText("Middle")
        self.btn2.setText("Corner")
        self.btn1.setCheckable(True)
        self.btn2.setCheckable(True)

        self.group = QButtonGroup()
        self.group.addButton(self.btn1)
        self.group.addButton(self.btn2)
        self.group.setExclusive(True)
        self.btn1.setChecked(True)

        self.btn1.setIcon(QIcon(resource_path("imgs/middle.png")))
        self.btn1.setIconSize(QSize(50, 50))
        self.btn1.setToolButtonStyle(Qt.ToolButtonStyle.ToolButtonTextUnderIcon)

        self.btn2.setIcon(QIcon(resource_path("imgs/corner.png")))
        self.btn2.setIconSize(QSize(50, 50))
        self.btn2.setToolButtonStyle(Qt.ToolButtonStyle.ToolButtonTextUnderIcon)

        configs.addWidget(self.btn1)
        configs.addWidget(self.btn2)


        left_layout.addWidget(title)
        left_layout.addSpacing(6)
        left_layout.addWidget(self.start_row)
        left_layout.addSpacing(6)
        left_layout.addWidget(self.stop_row)
        left_layout.addSpacing(6)
        left_layout.addLayout(configs)
        left_layout.addWidget(self.task_button)

        return left_layout
    
    def create_right(self):
        
        right_layout = QVBoxLayout()
        right_layout.setAlignment(Qt.AlignmentFlag.AlignTop)

        title = QLabel("Task List")
        title.setStyleSheet(PAGE_TITLE)

        self.task_table = QTableWidget()
        self.task_table.setColumnCount(3)
        self.task_table.setHorizontalHeaderLabels(
            ["Start", "Stop", "Config"]
        )

        self.task_table.setFixedSize(336, 120)


        self.task_table.setStyleSheet(TABLE)

        self.task_table.setColumnWidth(0, 110)   # Start
        self.task_table.setColumnWidth(1, 110)   # Stop
        self.task_table.setColumnWidth(2, 112)   # SLPM
        self.task_table.verticalHeader().setVisible(False)
        self.task_table.setSelectionBehavior(QTableWidget.SelectionBehavior.SelectRows)
        self.task_table.setSelectionMode(QTableWidget.SelectionMode.SingleSelection)

        self.task_table.setStyleSheet(TABLE)

        self.delete_button = QPushButton("Delete Task")
        self.delete_button.setFixedHeight(30)
        self.delete_button.clicked.connect(self.delete_task)

        self.delete_button.setStyleSheet(ACTION_BUTTON)

        right_layout.setContentsMargins(20,0,40,0)
        right_layout.addStretch()
        right_layout.addWidget(title)
        right_layout.addWidget(self.task_table)

        right_layout.addSpacing(5)


        right_layout.addWidget(self.delete_button)

        return right_layout

    def create_task_button(self):

        button = QPushButton("Add Task")

        button.setFixedSize(270, 30)

        button.setStyleSheet(ACTION_BUTTON)

        button.clicked.connect(self.add_task)

        return button

    def create_plot(self):

        time_axis = AxisItem(orientation="bottom")

        time_ticks = [
            [(0, "0"),
            (20, "20"),
            (40, "40"),
            (60, "60"),
            (80, "80"),
            (100, "100"),
            (120, "120")],
            [(i, "") for i in range(0, 121, 10)]
        ]

        time_axis.setTicks(time_ticks)

        self.graph = pg.PlotWidget(
            axisItems={
                "bottom": time_axis
            }
        )

        self.graph.hideAxis("left")

        self.graph.getAxis("bottom").setStyle(
            tickLength=5,
            tickTextOffset=8
        )


        self.graph.setBackground(BACKGROUND)
        self.graph.showGrid(x=False, y=False, alpha=1.0)
        self.graph.getAxis("bottom").setPen("k")

        self.graph.setLabel("bottom", "Time (seconds)")

        self.graph.setXRange(0, 120, padding=0)

        self.graph.getViewBox().setDefaultPadding(0)

        self.graph.getPlotItem().layout.setContentsMargins(10, 10, 20, 20)

        axis_pen = pg.mkPen(color="black", width=2)

        time_axis.setPen(axis_pen)

        self.graph.getAxis("left").setTextPen("k")
        
        self.graph.setMouseEnabled(x=False, y=False)

        return self.graph

    def delete_task(self):
        row = self.task_table.currentRow()

        if row >= 0:
            # 1. remove from model FIRST
            if 0 <= row < len(self.lights.tasks):
                self.lights.delete_task(row)

            # 2. remove graph item
            box = self.task_boxes.pop(row)
            self.graph.removeItem(box)

            # 3. remove table row
            self.task_table.removeRow(row)

    def add_task(self):
        try:
            start = int(self.start_row.time.text())
            stop = int(self.stop_row.time.text())

            if stop - start < 0:
                raise ValueError("Duration must be a positive whole number")

        except ValueError as e:
            QMessageBox.warning(self, "Invalid Input", "Enter seconds in whole numbers")
            return


        if self.btn1.isChecked():
            config = "c"
        elif self.btn2.isChecked():
            config = "m"
        
        task = LightsTask(
            start_time=start,
            stop_time=stop,
            config=config
        )

        self.lights.add_task(task)
        self.add_task_to_ui(task)

        self.start_row.time.clear()
        self.stop_row.time.clear()

        max_stop = max(
            (task.stop_time for task in self.lights.tasks),
            default=120
        )

        self.graph.setXRange(
            0,
            max(120, max_stop * 1.05),
            padding=0
        )

    def draw_task_box(self, task):

        width = task.stop_time - task.start_time
        center = task.start_time + width / 2

        path = QPainterPath()
        path.addRoundedRect(
            center - width/2,
            0.005,
            width,
            10,
            0.2,
            0.2
        )

        box = QGraphicsPathItem(path)

        box.setBrush(pg.mkBrush(BLUE))
        box.setPen(pg.mkPen(BACKGROUND, width=2))

        if task.config == "c":
            self.graph_c.addItem(box)
        elif task.config == "m":
            self.graph_m.addItem(box)

        self.task_boxes.append(box)

        return box

    def add_task_to_ui(self, task):
        row = self.task_table.rowCount()
        self.task_table.insertRow(row)

        self.task_table.setItem(
            row, 0,
            QTableWidgetItem(str(task.start_time))
        )

        self.task_table.setItem(
            row, 1,
            QTableWidgetItem(str(task.stop_time))
        )

        self.task_table.setItem(
            row, 2,
            QTableWidgetItem(
                str(task.config)
            )
        )

        self.draw_task_box(task)

class OzoneWindow(QWidget):
    def __init__(self, ozone, button, scheduler, chamber_window):
        super().__init__()
        self.setStyleSheet(f"background-color: {BACKGROUND};")
        self.ozone = ozone
        self.chamber_window = chamber_window
        self.button = button
        self.scheduler = scheduler

        self.resize(800,760)

        self.task_boxes = []
        self.graph = self.create_plot()

        layout = QVBoxLayout(self)

        middle_layout = QHBoxLayout()
        middle_layout.setAlignment(Qt.AlignmentFlag.AlignTop)

        self.left = self.create_left()
        self.right = self.create_right()
        self.header = self.create_header()

        header_widget = QWidget()
        header_widget.setLayout(self.header)

        left_widget = QWidget()
        left_widget.setLayout(self.left)

        right_widget = QWidget()
        right_widget.setLayout(self.right)

        layout.addWidget(header_widget)
        middle_layout.addWidget(left_widget, 1)
        middle_layout.addWidget(right_widget, 1)
       
        layout.addSpacing(20)
        layout.addLayout(middle_layout)

        layout.addSpacing(50)

        layout.addWidget(self.graph)
        
        self.load_tasks()
    
    def closeEvent(self, event):
        self.button.setEnabled(True)
        event.accept()

    def load_tasks(self):
        for task in self.ozone.tasks:
            self.add_task_to_ui(task)
    
    def create_header(self):
        header_layout = QHBoxLayout()
        title = QLabel(self.ozone.name)
        title.setStyleSheet(PAGE_TITLE)
        header_layout.setContentsMargins(40, 40, 0, 0)

        delete = QPushButton("Delete ozone")
        delete.setStyleSheet(RESET_BUTTON)
        delete.clicked.connect(self.delete_ozone)

        header_layout.addWidget(title)
        header_layout.addSpacing(10)
        header_layout.addWidget(delete)
        header_layout.addStretch()

        return header_layout
    
    def delete_ozone(self):

        if self.ozone in self.scheduler.ozones:
            self.scheduler.ozones.remove(self.ozone)

        if self.ozone in self.chamber_window.chamber.ozones:
            self.chamber_window.chamber.ozones.remove(self.ozone)

        self.chamber_window.line3.removeWidget(self.button)
        self.button.deleteLater()

        self.close()

    def create_left(self):    
        
        left_layout = QVBoxLayout()
        title = QLabel("Create Task")
        title.setStyleSheet(PAGE_TITLE)
        self.start_row = TimeInput("Start")
        self.duration = TimeInput("Duration")
        self.rate = FlowInput("Rate")
        self.task_button = self.create_task_button()
        left_layout.setContentsMargins(40, 0, 20, 0)
        left_layout.setAlignment(Qt.AlignmentFlag.AlignTop)

        self.volume = QLabel("Total Injection: Volume: ")

        self.start_row.time.textChanged.connect(self.calculate)
        self.duration.time.textChanged.connect(self.calculate)
        self.rate.time.textChanged.connect(self.calculate)

        left_layout.addWidget(title)
        left_layout.addSpacing(6)
        left_layout.addWidget(self.start_row)
        left_layout.addSpacing(6)
        left_layout.addWidget(self.duration)
        left_layout.addSpacing(6)

        left_layout.addWidget(self.rate)

        left_layout.addSpacing(5)
        left_layout.addWidget(self.volume)
        left_layout.addWidget(self.task_button)

  

        return left_layout
    
    def calculate(self):
            try:
                start = float(self.start_row.time.text())
                duration = float(self.duration.time.text())
                rate = float(self.rate.time.text())

                if duration > 0:
                    volume = duration * rate
                    self.volume.setText(f"Total Injection: Volume: {volume:.3f} \u00B5L")
                else:
                    self.volume.setText("Total Injection: Volume: --")
            except ValueError:
                self.volume.setText("Total Injection: Volume: --")


    def create_right(self):
        
        right_layout = QVBoxLayout()
        right_layout.setAlignment(Qt.AlignmentFlag.AlignTop)

        title = QLabel("Task List")
        title.setStyleSheet(PAGE_TITLE)

        self.task_table = QTableWidget()
        self.task_table.setColumnCount(3)
        self.task_table.setHorizontalHeaderLabels(
            ["Start", "Duration", "\u00B5L/sec"]
        )

        self.task_table.setFixedSize(336, 120)


        self.task_table.setStyleSheet(TABLE)

        self.task_table.setColumnWidth(0, 110)   # Start
        self.task_table.setColumnWidth(1, 110)   # Stop
        self.task_table.setColumnWidth(2, 112)   # SLPM
        self.task_table.verticalHeader().setVisible(False)
        self.task_table.setSelectionBehavior(QTableWidget.SelectionBehavior.SelectRows)
        self.task_table.setSelectionMode(QTableWidget.SelectionMode.SingleSelection)

        self.task_table.setStyleSheet(TABLE)

        self.delete_button = QPushButton("Delete Task")
        self.delete_button.setFixedHeight(30)
        self.delete_button.clicked.connect(self.delete_task)

        self.delete_button.setStyleSheet(ACTION_BUTTON)

        right_layout.setContentsMargins(20,0,40,0)
        right_layout.addStretch()
        right_layout.addWidget(title)
        right_layout.addWidget(self.task_table)

        right_layout.addSpacing(5)


        right_layout.addWidget(self.delete_button)

        return right_layout

    def create_task_button(self):

        button = QPushButton("Add Task")

        button.setFixedSize(270, 30)

        button.setStyleSheet(ACTION_BUTTON)

        button.clicked.connect(self.add_task)

        return button

    def create_plot(self):

        slpm_axis = AxisItem(orientation="left")

        slpm_ticks = [
            [(i, "") for i in [0, 0.2, 0.4, 0.6, 0.8, 1.0]],
            [(i, f"{i:.1f}") for i in [0, 0.2, 0.4, 0.6, 0.8, 1.0]]
        ]

        time_axis = AxisItem(orientation="bottom")

        time_ticks = [
            [(0, "0"),
            (20, "20"),
            (40, "40"),
            (60, "60"),
            (80, "80"),
            (100, "100"),
            (120, "120")],
            [(i, "") for i in range(0, 121, 10)]
        ]

        slpm_axis.setTicks(slpm_ticks)
        time_axis.setTicks(time_ticks)

        self.graph = pg.PlotWidget(
            axisItems={
                "left": slpm_axis,
                "bottom": time_axis
            }
        )


        self.graph.getAxis("bottom").setStyle(
            tickLength=5,
            tickTextOffset=8
        )

        self.graph.getAxis("left").setStyle(
            tickLength=5,
            tickTextOffset=8
        )

        self.graph.setBackground(BACKGROUND)
        self.graph.showGrid(x=False, y=False, alpha=1.0)
        self.graph.getAxis("left").setPen("k")
        self.graph.getAxis("bottom").setPen("k")

        self.graph.setLabel("left", "\u00B5L/sec")
        self.graph.setLabel("bottom", "Time (seconds)")

        self.graph.setYRange(0, 1, padding=0)
        self.graph.setXRange(0, 120, padding=0)

        self.graph.getViewBox().setDefaultPadding(0)

        self.graph.getPlotItem().layout.setContentsMargins(10, 10, 20, 20)

        axis_pen = pg.mkPen(color="black", width=2)

        time_axis.setPen(axis_pen)
        slpm_axis.setPen(axis_pen)

        self.graph.getAxis("left").setTextPen("k")
        self.graph.getAxis("bottom").setTextPen("k")
        self.graph.setMouseEnabled(x=False, y=False)

        return self.graph

    def delete_task(self):
        row = self.task_table.currentRow()

        if row >= 0:
            # 1. remove from model FIRST
            if 0 <= row < len(self.ozone.tasks):
                self.ozone.delete_task(row)

            # 2. remove graph item
            box = self.task_boxes.pop(row)
            self.graph.removeItem(box)

            # 3. remove table row
            self.task_table.removeRow(row)

    def add_task(self):
        try:
            start = int(self.start_row.time.text())
            duration = int(self.duration.time.text())
            flow = float(self.rate.time.text())

            if flow < 0:
                QMessageBox.warning(
                    self,
                    "Invalid Flow",
                    "Flow cannot be negative."
                )
                return

            if flow > 10:
                QMessageBox.warning(
                    self,
                    "Invalid Flow",
                    "Maximum flow is 10 SLPM."
                )
                return

            if duration < 1 or (duration % 1) != 0:
                raise ValueError("Duration must be a positive whole number")

        except ValueError as e:
            QMessageBox.warning(self, "Invalid Input", "Enter seconds in whole numbers")
            return

        task = OzoneTask(
            flow_rate=flow,
            start_time=start,
            duration=duration
        )

        self.ozone.add_task(task)
        self.add_task_to_ui(task)

        self.start_row.time.clear()
        self.duration.time.clear()
        self.rate.time.clear()

        max_stop = max(
            (task.duration for task in self.ozone.tasks),
            default=120
        )

        self.graph.setXRange(
            0,
            max(120, max_stop * 1.05),
            padding=0
        )

    def draw_task_box(self, task):

        width = task.duration
        center = task.start_time + width / 2

        path = QPainterPath()
        path.addRoundedRect(
            center - width/2,
            0.005,
            width,
            task.flow_rate - 0.005,
            0.2,
            0.2
        )

        box = QGraphicsPathItem(path)

        box.setBrush(pg.mkBrush(BLUE))
        box.setPen(pg.mkPen(BACKGROUND, width=2))

        self.graph.addItem(box)
        self.task_boxes.append(box)

        return box

    def add_task_to_ui(self, task):
        row = self.task_table.rowCount()
        self.task_table.insertRow(row)

        self.task_table.setItem(
            row, 0,
            QTableWidgetItem(str(task.start_time))
        )

        self.task_table.setItem(
            row, 1,
            QTableWidgetItem(str(task.duration))
        )

        self.task_table.setItem(
            row, 2,
            QTableWidgetItem(
                str(task.flow_rate)
            )
        )

        self.draw_task_box(task)

class ChambersPage(QWidget):
    def __init__(self, scheduler):
        super().__init__()

        self.chamber_count = 0
        self.chambers = []
        self.windows = []

        self.scheduler = scheduler

        self.main_layout = QVBoxLayout(self)
        self.main_layout.setContentsMargins(100, 30, 60, 30)
        self.main_layout.setAlignment(Qt.AlignmentFlag.AlignTop)

        title = QLabel("Atmospheric Chambers")
        title.setStyleSheet(PAGE_TITLE)

        self.chamber_layout = QHBoxLayout()

        self.add_button = QToolButton()
        self.add_button.setText("+ \n Add Chamber")
        self.add_button.setStyleSheet(ADD_BUTTON)
        self.add_button.setFixedSize(300, 450)
        self.add_button.clicked.connect(self.add_chamber)

        self.chamber_layout.addWidget(self.add_button)

        self.main_layout.addWidget(title)
        self.main_layout.addSpacing(20)
        self.main_layout.addLayout(self.chamber_layout)

    def add_chamber(self):
        self.chamber_count += 1

        chamber = Chamber(f"Chamber {self.chamber_count}")
        self.chambers.append(chamber)

        btn = QToolButton()
        btn.setText(f"Chamber {self.chamber_count}")
        btn.setIcon(QIcon(resource_path("imgs/chamber.png")))
        btn.setToolButtonStyle(Qt.ToolButtonStyle.ToolButtonTextUnderIcon)
        btn.setIconSize(QSize(200, 200))
        btn.setFixedSize(300, 450)
        btn.setStyleSheet(CHAMBER_BUTTON)

        btn.clicked.connect(lambda _, c=chamber, b=btn: self.open_chamber(c, b))

        self.chamber_layout.insertWidget(
            self.chamber_layout.count() - 1,
            btn
        )

    def open_chamber(self, chamber, button):
        win = ChamberWindow(chamber, button, self.scheduler, self)
        self.windows.append(win)
        button.setEnabled(False) 
        win.show()

class LogPage(QWidget):
    def __init__(self):
        super().__init__()
        layout = QVBoxLayout(self)

        layout.setContentsMargins(100, 30, 60, 30)
        layout.setAlignment(Qt.AlignmentFlag.AlignTop)

        title = QLabel("Log")
        title.setStyleSheet(PAGE_TITLE)

        self.log = QPlainTextEdit()
        self.log.setReadOnly(True)

        layout.addWidget(title)
        layout.addWidget(self.log)

    def append(self, message):
        timestamp = datetime.now().strftime("%H:%M:%S")
        self.log.appendPlainText(f"[{timestamp}] {message}")

def load_fonts():
    regular = resource_path("Cantarell/Cantarell-Regular.ttf")
    bold = resource_path("Cantarell/Cantarell-Bold.ttf")

    QFontDatabase.addApplicationFont(regular)
    QFontDatabase.addApplicationFont(bold)

def systemCheck():
    system = nidaqmx.system.System.local()
    for device in system.devices:   
        print(device.name, device.product_type)

def resource_path(relative_path):
    if hasattr(sys, "_MEIPASS"):
        return os.path.join(sys._MEIPASS, relative_path)
    return os.path.join(os.path.abspath("."), relative_path)

def main():
    daq = MockDAQBackend()
    #daq = NI_DAQBackend()
    scheduler = TaskScheduler(daq)

    app = QApplication([])
    
    load_fonts()

    app.setFont(QFont("Cantarell", 16))

    w = MainWindow(scheduler)
    w.show()

    app.exec()

#systemCheck()
main()

# TODO add lights to chambers
# TODO add ozone to chambers
# TODO change scheduler to pick up mfc and pump and lights and O3 tasks
# TODO rebuild mac and windows 
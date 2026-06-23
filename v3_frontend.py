import os
import pyqtgraph as pg
from v3_styles import *
from pyqtgraph import AxisItem
from PyQt6.QtCore import Qt, QSize, QTimer
from PyQt6.QtWidgets import (
    QApplication, QMainWindow, QWidget,
    QVBoxLayout, QHBoxLayout, QPushButton,
    QStackedWidget, QLabel, QButtonGroup,
    QLineEdit, QToolButton, QGraphicsPathItem,
    QTableWidget, QTableWidgetItem, QMessageBox)
from PyQt6.QtGui import (
    QFont, QPainterPath, QFontDatabase, QIcon)

class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()

        self.setup_window()
        self.create_pages()
        self.create_navbar()
        self.setup_layout()

        self.timer = QTimer()
        self.timer.timeout.connect(self.update_stopwatch)

        self.elapsed_seconds = 0
        self.is_running = False

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
        self.btn_3 = QPushButton("Reagents")

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

        self.chambers_page = ChambersPage()
        self.reagents_page = ReagentsPage()

        self.stack.addWidget(HomePage())
        self.stack.addWidget(self.chambers_page)
        self.stack.addWidget(self.reagents_page)

    def setup_layout(self):
        self.main_layout.addLayout(self.nav_bar)
        self.main_layout.addWidget(self.stack)

    def start_timer(self):
        if not self.is_running:
            self.timer.start(1000)  # 1 second
            self.is_running = True

    def pause_timer(self):
        if self.is_running:
            self.timer.stop()
            self.is_running = False

    def reset_timer(self):
        self.elapsed_seconds = 0
        self.update_display()

    def update_stopwatch(self):
        self.elapsed_seconds += 1
        self.update_display()

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

class Chamber:
    def __init__(self, name):
        self.name = name
        self.mfcs = []
        self.mfc_count = 0

    def add_mfc(self, mfc):
        self.mfcs.append(mfc)

    def delete_mfc(self, index):
        if 0 <= index < len(self.mfcs):
            del self.mfcs[index]

class TimeInput(QWidget):
    def __init__(self, label_text):
        super().__init__()

        layout = QHBoxLayout(self)

        self.label = QLabel(label_text)

        self.time = QLineEdit()

        self.time.setStyleSheet(LINE_EDIT)

        self.units = QLabel("min")

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
        self.slpm_unit = QLabel("SLPM")
    
        layout.addWidget(self.label)
        layout.addWidget(self.time)
        layout.addWidget(self.slpm_unit)
        layout.addStretch()
        layout.setContentsMargins(0, 0, 0, 0)

class ChamberWindow(QWidget):
    def __init__(self, chamber, button):
        super().__init__()
        self.setStyleSheet(f"background-color: {BACKGROUND};")
        self.mfc_windows = []
        self.chamber = chamber
        self.button = button

        self.setWindowTitle(chamber.name)
        self.resize(900,700)

        layout = QVBoxLayout(self)

        title1 = QLabel(self.chamber.name.upper())
        title1.setStyleSheet(PAGE_TITLE)

        title2 = QLabel("Lights")
        title2.setStyleSheet(PAGE_TITLE)

        title3 = QLabel("MFCs")
        title3.setStyleSheet(PAGE_TITLE)
        self.line3 = QHBoxLayout()
        self.add_mfc_btn = QToolButton()
        self.add_mfc_btn.setStyleSheet(MFC_ADD_BUTTON)
        self.add_mfc_btn.setText("+\nMFC")
        self.add_mfc_btn.setFixedSize(100, 100)
        self.add_mfc_btn.clicked.connect(self.add_mfc)
        self.line3.addWidget(self.add_mfc_btn)
        for mfc in self.chamber.mfcs:
            self.create_mfc_button(mfc)

        layout.setContentsMargins(80, 60, 60, 30)
        layout.setAlignment(Qt.AlignmentFlag.AlignTop)
        layout.addWidget(title1)
        layout.addWidget(title2)
        layout.addWidget(title3)
        layout.addLayout(self.line3)
        layout.addStretch()

    def closeEvent(self, event):
        self.button.setEnabled(True)
        event.accept()

    def create_mfc_button(self, mfc):
        btn = QToolButton()
        btn.setText(mfc.name)
        btn.setIcon(QIcon("mfc.png"))
        btn.setIconSize(QSize(50, 50))
        btn.setToolButtonStyle(
            Qt.ToolButtonStyle.ToolButtonTextUnderIcon
        )

        btn.setFixedSize(100, 100)
        btn.setStyleSheet(MFC_BUTTON)

        btn.clicked.connect(
            lambda _, m=mfc, b=self.button: self.open_mfc(m, b)
        )

        self.line3.insertWidget(
            self.line3.count() - 1,
            btn
        )

    def add_mfc(self):
        self.chamber.mfc_count += 1

        mfc = MFC(f"MFC {self.chamber.mfc_count}")
        self.chamber.add_mfc(mfc)

        self.create_mfc_button(mfc)

    def open_mfc(self, mfc, button):
        win = MFCWindow(mfc, button)
        self.mfc_windows.append(win)

        button.setEnabled(False)
        win.show()

class MFCWindow(QWidget):
    def __init__(self, mfc, button):
        super().__init__()
        self.setStyleSheet(f"background-color: {BACKGROUND};")
        self.mfc = mfc
        self.button = button

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

        self.mfc1.clicked.connect(lambda: self.set_wire(1))
        self.mfc2.clicked.connect(lambda: self.set_wire(2))
        self.mfc3.clicked.connect(lambda: self.set_wire(3))

        if self.mfc.wire == 1:
            self.mfc1.setChecked(True)
        elif self.mfc.wire == 2:
            self.mfc2.setChecked(True)
        elif self.mfc.wire == 3:
            self.mfc3.setChecked(True)


        self.mfc_group = QButtonGroup(self)
        self.mfc_group.setExclusive(True)

        self.mfc_group.addButton(self.mfc1)
        self.mfc_group.addButton(self.mfc2)
        self.mfc_group.addButton(self.mfc3)

        header_layout.addWidget(title)
        header_layout.addSpacing(10)
        header_layout.addWidget(self.mfc1)
        header_layout.addWidget(self.mfc2)
        header_layout.addWidget(self.mfc3)
        header_layout.addStretch()

        return header_layout

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
    
    def set_wire(self, wire):
        self.mfc.wire = wire

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
        self.graph.setLabel("bottom", "Time (minutes)")

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

            if start >= stop:
                raise ValueError("Start must be before stop")

        except ValueError as e:
            QMessageBox.warning(self, "Invalid Input", "Enter minutes in whole numbers")
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

class ChambersPage(QWidget):
    def __init__(self):
        super().__init__()

        self.chamber_count = 0
        self.chambers = []
        self.windows = []

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
        btn.setIcon(QIcon("chamber.png"))
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
        win = ChamberWindow(chamber, button)
        self.windows.append(win)
        button.setEnabled(False) 
        win.show()

class ReagentsPage(QWidget):
    def __init__(self):
        super().__init__()
        layout = QVBoxLayout(self)
        layout.addWidget(QLabel("Reagents"))

def load_fonts():
    base_path = os.path.dirname(__file__)
    font_dir = os.path.join(base_path, "Cantarell")

    regular = os.path.join(font_dir, "Cantarell-Regular.ttf")
    bold = os.path.join(font_dir, "Cantarell-Bold.ttf")

    QFontDatabase.addApplicationFont(regular)
    QFontDatabase.addApplicationFont(bold)

def main():
    app = QApplication([])

    load_fonts()

    app.setFont(QFont("Cantarell", 16))

    w = MainWindow()
    w.show()

    app.exec()

main()
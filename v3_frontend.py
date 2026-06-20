import os
import pyqtgraph as pg
from v3_styles import *
from pyqtgraph import AxisItem
from PyQt6.QtCore import Qt, QPointF, QSize
from PyQt6.QtWidgets import (
    QApplication, QMainWindow, QWidget,
    QVBoxLayout, QHBoxLayout, QPushButton,
    QStackedWidget, QLabel, QButtonGroup,
    QLineEdit, QToolButton, QGraphicsPathItem,
    QTableWidget, QTableWidgetItem, QMessageBox,
    QGraphicsPolygonItem, QGraphicsScene, QGraphicsView)
from PyQt6.QtGui import (
    QFont, QPainterPath, QPolygonF,
    QPen, QBrush, QColor, QFontDatabase, 
    QIcon)

class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()

        self.setup_window()
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
        self.btn_3 = QPushButton("Reagents")

        self.nav_bar.addWidget(self.btn_1)
        self.nav_bar.addSpacing(60)
        self.nav_bar.addWidget(self.btn_2)
        self.nav_bar.addSpacing(30)

        self.nav_bar.addWidget(self.btn_3)

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
        self.color = "#"

    def add_task(self, task):
        self.tasks.append(task)

    def delete_task(self, index):
        if 0 <= index < len(self.tasks):
            del self.tasks[index]

    def plot(self):
        """
        Later:
        x-axis = time
        y-axis = flow rate

        Build step-function from tasks and
        draw on pyqtgraph.
        """
        pass

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
        self.time.setInputMask("00:00")

        self.am = QToolButton()
        self.pm = QToolButton()

        self.am.setText("AM")
        self.pm.setText("PM")

        self.am.setCheckable(True)
        self.pm.setCheckable(True)

        group = QButtonGroup(self)
        group.setExclusive(True)
        group.addButton(self.am)
        group.addButton(self.pm)

        self.am.setChecked(True)

        layout.addWidget(self.label)
        layout.addWidget(self.time)
        layout.addWidget(self.am)
        layout.addWidget(self.pm)
        layout.addStretch()

class ChamberWindow(QWidget):
    def __init__(self, chamber):
        super().__init__()

        self.mfc_windows = []
        self.chamber = chamber

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
            lambda _, m=mfc: self.open_mfc(m)
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

    def open_mfc(self, mfc):
        win = MFCWindow(mfc)
        self.mfc_windows.append(win)
        win.show()

class MFCWindow(QWidget):
    def __init__(self, mfc):
        super().__init__()

        self.mfc = mfc

        self.setWindowTitle(mfc.name)
        self.resize(700, 500)

        layout = QVBoxLayout(self)

        title = QLabel(mfc.name)
        title.setStyleSheet(PAGE_TITLE)

        layout.addWidget(title)
        layout.addWidget(QLabel("MFC control panel goes here"))

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

        btn.clicked.connect(lambda _, c=chamber: self.open_chamber(c))

        self.chamber_layout.insertWidget(
            self.chamber_layout.count() - 1,
            btn
        )

    def open_chamber(self, chamber):
        win = ChamberWindow(chamber)
        self.windows.append(win)
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


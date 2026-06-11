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

class Chamber:
    def __init__(self, name):
        self.name = name
        self.pressure = 1.0
        self.flow_rate = 0.0

class ChamberWindow(QWidget):
   def __init__(self, chamber):
        super().__init__()

        self.chamber = chamber

        self.setWindowTitle(chamber.name)
        self.resize(600, 400)

        layout = QVBoxLayout(self)

        title = QLabel(chamber.name)
        layout.addWidget(title)

        self.pressure_label = QLabel(f"Pressure: {chamber.pressure}")
        layout.addWidget(self.pressure_label)

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
        btn.setText(f"({self.chamber_count})")
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


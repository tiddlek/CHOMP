import pyqtgraph as pg
from styles import *
from pyqtgraph import AxisItem
from PyQt6.QtCore import Qt, QPointF
from PyQt6.QtWidgets import (
    QApplication, QMainWindow, QWidget,
    QVBoxLayout, QHBoxLayout, QPushButton,
    QStackedWidget, QLabel, QButtonGroup,
    QLineEdit, QToolButton, QGraphicsPathItem,
    QTableWidget, QTableWidgetItem, QMessageBox,
    QGraphicsPolygonItem, QGraphicsScene, QGraphicsView
)
from PyQt6.QtGui import (
    QFont, QPainterPath, QPolygonF,
    QPen, QBrush, QColor)

class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()

        self.setup_window()
        self.create_pages()
        self.create_navbar()
        self.setup_layout()

    def setup_window(self):
        
        self.setWindowTitle("CHOMP")
        self.resize(900,700)

        self.central = QWidget()
        self.setCentralWidget(self.central) 
        self.central.setStyleSheet(APP_BACKGROUND)


        self.main_layout = QVBoxLayout(self.central)

    def create_navbar(self):
        self.nav_bar = QHBoxLayout()

        self.btn_1 = QPushButton("CHOMP")
        self.btn_2 = QPushButton("Mass Flow Controllers")
        self.btn_3 = QPushButton("Lights")
        self.btn_4 = QPushButton("Ozone Generator")
        self.btn_5 = QPushButton("Liquid Handler")

        self.nav_bar.addWidget(self.btn_1)
        self.nav_bar.addSpacing(10)
        self.nav_bar.addWidget(self.btn_2)
        self.nav_bar.addWidget(self.btn_3)
        self.nav_bar.addWidget(self.btn_4)
        self.nav_bar.addWidget(self.btn_5)

        self.btn_1.clicked.connect(lambda: self.stack.setCurrentIndex(0))
        self.btn_2.clicked.connect(lambda: self.stack.setCurrentIndex(1))
        self.btn_3.clicked.connect(lambda: self.stack.setCurrentIndex(2))
        self.btn_4.clicked.connect(lambda: self.stack.setCurrentIndex(3))
        self.btn_5.clicked.connect(lambda: self.stack.setCurrentIndex(4))

        self.group = QButtonGroup()

        self.group.addButton(self.btn_1, 0)
        self.group.addButton(self.btn_2, 1)
        self.group.addButton(self.btn_3, 2)
        self.group.addButton(self.btn_4, 3)
        self.group.addButton(self.btn_5, 4)

        self.group.setExclusive(True)

        self.group.idClicked.connect(self.stack.setCurrentIndex)
        
        self.btn_1.setCheckable(True)
        self.btn_2.setCheckable(True)
        self.btn_3.setCheckable(True)
        self.btn_4.setCheckable(True)
        self.btn_5.setCheckable(True)

        self.btn_1.setStyleSheet(LOGO_BUTTON)
        
        self.btn_2.setStyleSheet(NAV_BUTTON)
        self.btn_3.setStyleSheet(NAV_BUTTON)
        self.btn_4.setStyleSheet(NAV_BUTTON)
        self.btn_5.setStyleSheet(NAV_BUTTON)

        self.nav_bar.setContentsMargins(40, 30, 40, 0)
        self.nav_bar.addStretch()
        self.nav_bar.setSpacing(30)

    def create_pages(self):
        self.stack = QStackedWidget()

        self.mfc_page = MFCPage()
        self.lights_page = LightsPage()
        self.ozone_page = OzonePage()
        self.liquid_page = LiquidPage()

        self.stack.addWidget(HomePage())
        self.stack.addWidget(self.mfc_page)
        self.stack.addWidget(self.lights_page)
        self.stack.addWidget(self.ozone_page)
        self.stack.addWidget(self.liquid_page)

    def setup_layout(self):
        self.main_layout.addLayout(self.nav_bar)
        self.main_layout.addWidget(self.stack)

class HomePage(QWidget):
    def __init__(self):
        super().__init__()
        layout = QVBoxLayout(self)

        title = QLabel("CHOMP")
        title.setAlignment(Qt.AlignmentFlag.AlignCenter)
        title.setStyleSheet("font-size: 62px; font-weight: bold; color: #2C5158;")

        subtitle = QLabel("atmospheriC cHamber\nautOMation Platform")
        subtitle.setAlignment(Qt.AlignmentFlag.AlignCenter)
        subtitle.setStyleSheet("font-size: 24px; font-weight: regular; color: black;")

        layout.addStretch()
        layout.addWidget(title)
        layout.addWidget(subtitle)
        layout.addStretch()

class MFCPage(QWidget):
    def __init__(self):
        super().__init__()

        self.task_count = 0
        self.task_boxes = []
        self.task_table = QTableWidget()
        self.graph = self.create_plot()

        layout = QVBoxLayout(self)

        top_layout = QHBoxLayout()

        self.left = self.create_left()
        self.right = self.create_right()

        left_widget = QWidget()
        left_widget.setLayout(self.left)

        right_widget = QWidget()
        right_widget.setLayout(self.right)

        top_layout.addWidget(left_widget, 1)
        top_layout.addWidget(right_widget, 1)
       
        layout.addLayout(top_layout)

        layout.addSpacing(50)

        layout.addWidget(self.graph)

    def create_left(self):    
        
        left_layout = QVBoxLayout()
        title = QLabel("Mass Flow Controllers")
        title.setStyleSheet(SECTION_TITLE)

        self.mfc1 = QPushButton("1")
        self.mfc2 = QPushButton("2")

        self.mfc1.setCheckable(True)
        self.mfc2.setCheckable(True)

        self.mfc1.setFixedSize(28,28)
        self.mfc2.setFixedSize(28,28)

        def mfc_button_style(color):
            return f"""
            QPushButton {{
                background-color: transparent;
                color: {color};
                border: 2px solid {color};
                border-radius: 4px;
                font-weight: bold;
            }}

            QPushButton:checked {{
                background-color: {color};
                color: white;
                border: 2px solid {color};
            }}

            QPushButton:hover {{
                border: 2px solid {color};
            }}
            """

        self.mfc1.setStyleSheet(mfc_button_style(MFC1))

        self.mfc2.setStyleSheet(mfc_button_style(MFC2))

        self.start_row = self.create_start()
        self.stop_row = self.create_stop()
        self.slpm_row = self.create_slpm()
        self.task_button = self.create_task_button()
        self.plot = self.create_plot()
        left_layout.setContentsMargins(40, 20, -20, 0)
        title_row = QHBoxLayout()
        title_row.addWidget(title)
        title_row.addSpacing(10)
        title_row.addWidget(self.mfc1)
        title_row.addWidget(self.mfc2)
        title_row.addStretch()

        left_layout.addLayout(title_row)
        left_layout.setAlignment(Qt.AlignmentFlag.AlignTop)
        left_layout.addSpacing(10)
        left_layout.addLayout(self.start_row)
        left_layout.addLayout(self.stop_row)
        left_layout.addLayout(self.slpm_row)
        left_layout.addSpacing(5)
        left_layout.addWidget(self.task_button)

        return left_layout

    def create_right(self):
        
        right_layout = QVBoxLayout()

        title = QLabel("Task List")
        title.setStyleSheet(SECTION_TITLE)

        self.task_table = QTableWidget()
        self.task_table.setColumnCount(4)
        self.task_table.setHorizontalHeaderLabels(
            ["Device", "Start", "Stop", "SLPM"]
        )

        self.task_table.setFixedSize(336, 120)


        self.task_table.setStyleSheet(TABLE)

        self.task_table.setColumnWidth(0, 83)   # Task
        self.task_table.setColumnWidth(1, 83)   # Start
        self.task_table.setColumnWidth(2, 83)   # Stop
        self.task_table.setColumnWidth(3, 83)   # SLPM
        self.task_table.verticalHeader().setVisible(False)
        self.task_table.setSelectionBehavior(QTableWidget.SelectionBehavior.SelectRows)
        self.task_table.setSelectionMode(QTableWidget.SelectionMode.SingleSelection)

        self.task_table.setStyleSheet(TABLE)

        self.delete_button = QPushButton("Delete Task")
        self.delete_button.setFixedHeight(30)
        self.delete_button.clicked.connect(self.delete_task)

        self.delete_button.setStyleSheet(ACTION_BUTTON)

        right_layout.setContentsMargins(40,20,40,0)
        right_layout.addWidget(title)
        right_layout.addWidget(self.task_table)

        right_layout.addSpacing(5)


        right_layout.addWidget(self.delete_button)

        return right_layout

    def create_start(self):
        start_row = QHBoxLayout()
        
        self.start_label = QLabel("Start Time")
        self.start_input = QLineEdit()
        self.start_am = QToolButton()
        self.start_pm = QToolButton()

        
        self.start_input.setInputMask("00:00")
        self.start_input.setMaximumWidth(60)
        self.start_am.setText("AM")
        self.start_pm.setText("PM")
        self.start_am.setCheckable(True)
        self.start_pm.setCheckable(True)
        

        start_group = QButtonGroup(self)
        start_group.setExclusive(True)
        start_group.addButton(self.start_am)
        start_group.addButton(self.start_pm)

        self.start_am.setChecked(True)

        start_row.addWidget(self.start_label)
        start_row.addWidget(self.start_input)
        start_row.addWidget(self.start_am)
        start_row.addWidget(self.start_pm)
        start_row.addStretch()

        self.start_am.setStyleSheet(TOOL_BUTTON)
        self.start_pm.setStyleSheet(TOOL_BUTTON)

        self.start_input.setStyleSheet(LINE_EDIT)

        return start_row

    def create_stop(self):

        stop_row = QHBoxLayout()

        self.stop_label = QLabel("Stop Time")
        self.stop_input = QLineEdit()
        self.stop_am = QToolButton()
        self.stop_pm = QToolButton()

        self.stop_input.setInputMask("00:00")
        self.stop_input.setMaximumWidth(60)
        self.stop_am.setText("AM")
        self.stop_pm.setText("PM")
        self.stop_am.setCheckable(True)
        self.stop_pm.setCheckable(True)
        
        stop_group = QButtonGroup(self)
        stop_group.setExclusive(True)
        stop_group.addButton(self.stop_am)
        stop_group.addButton(self.stop_pm)
        
        self.stop_am.setChecked(True)

        stop_row.addWidget(self.stop_label)
        stop_row.addWidget(self.stop_input)
        stop_row.addWidget(self.stop_am)
        stop_row.addWidget(self.stop_pm)
        stop_row.addStretch()

        self.stop_am.setStyleSheet(TOOL_BUTTON)
        self.stop_pm.setStyleSheet(TOOL_BUTTON)


        self.stop_input.setStyleSheet(LINE_EDIT)

        return stop_row

    def create_slpm(self):

        slpm_row = QHBoxLayout()

        self.slpm_unit = QLabel("SLPM")
        self.slpm_label = QLabel("Flow Rate")
        self.slpm_input = QLineEdit()
        
        self.slpm_input.setInputMask("00.00")
        self.slpm_input.setMaximumWidth(60)


        slpm_row.addWidget(self.slpm_label)
        slpm_row.addWidget(self.slpm_input)
        slpm_row.addWidget(self.slpm_unit)
        slpm_row.addStretch()

        self.slpm_input.setStyleSheet(LINE_EDIT)
        
        return slpm_row

    def create_task_button(self):

        button = QPushButton("Add Task")

        button.setFixedSize(270, 30)

        button.setStyleSheet(ACTION_BUTTON)

        button.clicked.connect(self.add_task)

        return button

    def create_plot(self):

        slpm_axis = AxisItem(orientation="left")
        slpm_ticks = [
            [(i, "") for i in range(0, 11)],          # minor ticks (no labels)
            [(i, str(i)) for i in range(0, 11, 2)]    # major ticks (labels)
        ]

        time_axis = AxisItem(orientation="bottom")
        time_ticks = [
        [(4,  "4:00"),
        (8,  "8:00"),
        (12, "12:00"),
        (16, "4:00"),
        (20, "8:00"),
        (24, "12:00")],
        [(i, "") for i in range(0, 25, 1)]
        ]

        slpm_axis.setTicks(slpm_ticks)
        time_axis.setTicks(time_ticks)
        time_axis.setTickSpacing(4,4)


        self.graph = pg.PlotWidget(axisItems={
            "left": slpm_axis,
            "bottom": time_axis
        })

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
        self.graph.setLabel("bottom", "Time (hours)")

        self.graph.setYRange(0, 10, padding=0)
        self.graph.setXRange(0, 24, padding=0)

        self.graph.getViewBox().setDefaultPadding(0)

        self.graph.getPlotItem().layout.setContentsMargins(10, 10, 20, 20)

        axis_pen = pg.mkPen(color="black", width=2)

        time_axis.setPen(axis_pen)
        slpm_axis.setPen(axis_pen)

        self.graph.getAxis("left").setTextPen("k")
        self.graph.getAxis("bottom").setTextPen("k")
        self.graph.setMouseEnabled(x=False, y=False)

        return self.graph

    def parse_time(self, t, is_pm):
        h, m = t.split(":")

        h = int(h)
        m = int(m)

        # validate 12-hour clock input
        if not (1 <= h <= 12):
            raise ValueError("Hour must be 1–12")

        if not (0 <= m <= 59):
            raise ValueError("Minutes must be 00–59")

        # convert to 24-hour decimal
        if is_pm and h != 12:
            h += 12
        if not is_pm and h == 12:
            h = 0

        return h + m / 60

    def format_time(self, t):
        """Convert decimal hours -> 'H:MM AM/PM'"""
        h = int(t)
        m = int(round((t - h) * 60))

        if m == 60:
            h += 1
            m = 0

        am_pm = "am"
        display_h = h

        if h >= 12:
            am_pm = "pm"
        if h > 12:
            display_h = h - 12
        if h == 0:
            display_h = 12

        return f"{display_h}:{m:02d} {am_pm}"

    def delete_task(self):
        row = self.task_table.currentRow()

        if row >= 0:
            box = self.task_boxes.pop(row)
            self.graph.removeItem(box)
            self.task_table.removeRow(row)

    def add_task(self):
        try:
            start_pm = self.start_pm.isChecked()
            stop_pm = self.stop_pm.isChecked()

            start = self.parse_time(self.start_input.text(), start_pm)
            stop = self.parse_time(self.stop_input.text(), stop_pm)
            flow = float(self.slpm_input.text())

            if start >= stop:
                raise ValueError("Start must be before stop")

        except ValueError as e:
            QMessageBox.warning(self, "Invalid Input", str(e))
            return
        
        selected = []
        colors = []

        if self.mfc1.isChecked():
            selected.append("1")
            colors.append(MFC1)      # blue

        if self.mfc2.isChecked():
            selected.append("2")
            colors.append(MFC2)      # orange

        if not selected:
            QMessageBox.warning(
                self,
                "No MFC Selected",
                "Select at least one MFC."
            )
            return

        number_text = ", ".join(selected)

        row = self.task_table.rowCount()
        self.task_table.insertRow(row)

        self.task_table.setItem(row, 0, QTableWidgetItem(number_text))
        self.task_table.setItem(row, 1, QTableWidgetItem(self.format_time(start)))
        self.task_table.setItem(row, 2, QTableWidgetItem(self.format_time(stop)))
        self.task_table.setItem(row, 3, QTableWidgetItem(str(flow)))

        

        width = stop - start
        center = start + width / 2

        if len(colors) == 2:
            BOX_COLOR = MFC1     # blend-ish color when both selected
        else:
            BOX_COLOR = colors[0]

        path = QPainterPath()
        path.addRoundedRect(
            center - width/2,       # x
            0.05,                   # y
            width,                  # width
            flow-0.05,              # height
            0.3,                    # x radius
            0.3                     # y radius
        )

        box = QGraphicsPathItem(path)

        box.setBrush(pg.mkBrush(BOX_COLOR))
        box.setPen(pg.mkPen(BACKGROUND, width=2))

        self.graph.addItem(box)
        self.task_boxes.append(box)

class LightsPage(QWidget):
    def __init__(self):
        super().__init__()

        self.task_count = 0
        self.task_boxes = []
        self.task_table = QTableWidget()

        layout = QHBoxLayout(self)


        self.left = self.create_left()
        self.right = self.create_right()

        left_widget = QWidget()
        left_widget.setLayout(self.left)

        right_widget = QWidget()
        right_widget.setLayout(self.right)

        layout.addWidget(left_widget, 1)
        layout.addWidget(right_widget, 1)
    
    def create_left(self):    
        left_layout = QVBoxLayout()

        title = QLabel("Lights")
        title.setStyleSheet(SECTION_TITLE)

        lights_start_row = self.create_start()
        lights_stop_row = self.create_stop()
        lights_task_button = self.create_task_button()

        # ----- LIGHTS TASK TABLE -----
        self.task_table = QTableWidget()
        self.task_table.setColumnCount(3)
        self.task_table.setHorizontalHeaderLabels(
            ["Device", "Start", "Stop"]
        )

        self.task_table.setColumnWidth(0, 90)
        self.task_table.setColumnWidth(1, 90)
        self.task_table.setColumnWidth(2, 90)
        self.task_table.setFixedSize(274, 300)

        self.task_table.verticalHeader().setVisible(False)

        self.task_table.setSelectionBehavior(
            QTableWidget.SelectionBehavior.SelectRows
        )

        self.task_table.setSelectionMode(
            QTableWidget.SelectionMode.SingleSelection
        )

        self.task_table.setStyleSheet(TABLE)

        left_layout.setContentsMargins(40,20,40,20)

        left_layout.addWidget(title)
        left_layout.addSpacing(10)

        left_layout.addLayout(lights_start_row)
        left_layout.addLayout(lights_stop_row)

        left_layout.addSpacing(5)
        left_layout.addWidget(lights_task_button)

        # TABLE BELOW BUTTON
        left_layout.addSpacing(10)
        left_layout.addWidget(self.task_table)

        self.delete_button = QPushButton("Delete Task")
        self.delete_button.setFixedSize(280, 30)
        self.delete_button.clicked.connect(self.delete_task)


        self.delete_button.setStyleSheet(ACTION_BUTTON)
        left_layout.addWidget(self.delete_button)
        left_layout.addStretch()

        return left_layout

    def create_right(self):
        right_layout = QVBoxLayout()

        right_layout.setContentsMargins(40,20,40,20)

        title = QLabel("Chamber Lights")
        title.setStyleSheet(SECTION_TITLE)

        scene = QGraphicsScene()
        scene2 = QGraphicsScene()
        

        # parallelogram coordinates
        poly = QPolygonF([
            QPointF(120, 40),
            QPointF(240, 40),
            QPointF(140, 120),
            QPointF(20, 120)
        ])

        poly2 = QPolygonF([
            QPointF(120, -20),
            QPointF(240, -20),
            QPointF(140, 60),
            QPointF(20, 60)
        ])

        parallelogram = QGraphicsPolygonItem(poly)
        parallelogram_2 = QGraphicsPolygonItem(poly2)
        scene2.setSceneRect(poly2.boundingRect())

        orange = QColor(ORANGE)

        parallelogram.setBrush(QBrush(Qt.BrushStyle.NoBrush))
        parallelogram.setPen(QPen(orange, 5))

        parallelogram_2.setBrush(QBrush(Qt.BrushStyle.NoBrush))
        parallelogram_2.setPen(QPen(orange, 5))

        scene.addItem(parallelogram)
        scene2.addItem(parallelogram_2)

        view1 = QGraphicsView(scene)
        view1.setStyleSheet("""
            background: transparent;
            border: none;
        """)

        view2 = QGraphicsView(scene2)
        view2.setStyleSheet("""
            background: transparent;
            border: none;
        """)

        self.light_group = QButtonGroup(self)
        self.light_group.setExclusive(False)

        row = QHBoxLayout()
        row.setSpacing(0)

        self.light_buttons = []

        for i in range(6):

            btn = QPushButton()
            btn.setFixedSize(15, 200)
            btn.setCheckable(True)

            self.light_buttons.append(btn)

            btn.setStyleSheet(LIGHT_BUTTON)

            self.light_group.addButton(btn, i)

            group_index = i % 3
            top_offset = group_index * 40

            wrapper = QVBoxLayout()
            wrapper.setContentsMargins(5, 2-0, 5, top_offset)

            container = QWidget()
            container.setLayout(wrapper)
            wrapper.addWidget(btn)

            row.addWidget(container)

            if i == 2:
                row.addSpacing(60)

        # center row
        outer = QHBoxLayout()
        outer.addStretch()
        outer.addLayout(row)
        outer.addStretch()

        view1.setAlignment(Qt.AlignmentFlag.AlignCenter | Qt.AlignmentFlag.AlignTop)
        view2.setAlignment(Qt.AlignmentFlag.AlignCenter | Qt.AlignmentFlag.AlignTop)


        right_layout.addWidget(title)
        right_layout.addSpacing(10)
        right_layout.addWidget(view1)
        right_layout.addSpacing(20)
        right_layout.addLayout(outer)

        right_layout.addWidget(view2)


        return right_layout

    def create_start(self):
        start_row = QHBoxLayout()
        
        self.start_label = QLabel("Start Time")
        self.start_input = QLineEdit()
        self.start_am = QToolButton()
        self.start_pm = QToolButton()

        
        self.start_input.setInputMask("00:00")
        self.start_input.setMaximumWidth(60)
        self.start_am.setText("AM")
        self.start_pm.setText("PM")
        self.start_am.setCheckable(True)
        self.start_pm.setCheckable(True)
        

        start_group = QButtonGroup(self)
        start_group.setExclusive(True)
        start_group.addButton(self.start_am)
        start_group.addButton(self.start_pm)

        self.start_am.setChecked(True)

        start_row.addWidget(self.start_label)
        start_row.addWidget(self.start_input)
        start_row.addWidget(self.start_am)
        start_row.addWidget(self.start_pm)
        start_row.addStretch()

        self.start_am.setStyleSheet(TOOL_BUTTON)
        self.start_pm.setStyleSheet(TOOL_BUTTON)

        self.start_input.setStyleSheet(LINE_EDIT)

        return start_row

    def create_stop(self):

        stop_row = QHBoxLayout()

        self.stop_label = QLabel("Stop Time")
        self.stop_input = QLineEdit()
        self.stop_am = QToolButton()
        self.stop_pm = QToolButton()

        self.stop_input.setInputMask("00:00")
        self.stop_input.setMaximumWidth(60)
        self.stop_am.setText("AM")
        self.stop_pm.setText("PM")
        self.stop_am.setCheckable(True)
        self.stop_pm.setCheckable(True)
        
        stop_group = QButtonGroup(self)
        stop_group.setExclusive(True)
        stop_group.addButton(self.stop_am)
        stop_group.addButton(self.stop_pm)
        
        self.stop_am.setChecked(True)

        stop_row.addWidget(self.stop_label)
        stop_row.addWidget(self.stop_input)
        stop_row.addWidget(self.stop_am)
        stop_row.addWidget(self.stop_pm)
        stop_row.addStretch()

        self.stop_am.setStyleSheet(TOOL_BUTTON)
        self.stop_pm.setStyleSheet(TOOL_BUTTON)


        self.stop_input.setStyleSheet(LINE_EDIT)

        return stop_row

    def create_task_button(self):

        button = QPushButton("Add Task")

        button.setFixedSize(270, 30)

        button.setStyleSheet(ACTION_BUTTON)

        button.clicked.connect(self.add_task)

        return button

    def parse_time(self, t, is_pm):
        h, m = t.split(":")

        h = int(h)
        m = int(m)

        # validate 12-hour clock input
        if not (1 <= h <= 12):
            raise ValueError("Hour must be 1–12")

        if not (0 <= m <= 59):
            raise ValueError("Minutes must be 00–59")

        # convert to 24-hour decimal
        if is_pm and h != 12:
            h += 12
        if not is_pm and h == 12:
            h = 0

        return h + m / 60

    def format_time(self, t):
        """Convert decimal hours -> 'H:MM AM/PM'"""
        h = int(t)
        m = int(round((t - h) * 60))

        if m == 60:
            h += 1
            m = 0

        am_pm = "am"
        display_h = h

        if h >= 12:
            am_pm = "pm"
        if h > 12:
            display_h = h - 12
        if h == 0:
            display_h = 12

        return f"{display_h}:{m:02d} {am_pm}"

    def delete_task(self):
        row = self.task_table.currentRow()

        if row >= 0:
            self.task_table.removeRow(row)
    
    def add_task(self):
        try:
            start_pm = self.start_pm.isChecked()
            stop_pm = self.stop_pm.isChecked()

            start = self.parse_time(self.start_input.text(), start_pm)
            stop = self.parse_time(self.stop_input.text(), stop_pm)

            if start >= stop:
                raise ValueError("Start must be before stop")

        except ValueError as e:
            QMessageBox.warning(self, "Invalid Input", str(e))
            return

        # determine selected light numbers
        selected = []

        for i, btn in enumerate(self.light_buttons):
            if btn.isChecked():
                selected.append(str(i + 1))

        if not selected:
            QMessageBox.warning(
                self,
                "No Lights Selected",
                "Select at least one light."
            )
            return

        number_text = ", ".join(selected)

        row = self.task_table.rowCount()
        self.task_table.insertRow(row)

        self.task_table.setItem(
            row, 0,
            QTableWidgetItem(number_text)
        )

        self.task_table.setItem(
            row, 1,
            QTableWidgetItem(self.format_time(start))
        )

        self.task_table.setItem(
            row, 2,
            QTableWidgetItem(self.format_time(stop))
        )

class OzonePage(QWidget):
    def __init__(self):
        super().__init__()
        layout = QVBoxLayout(self)
        layout.addWidget(QLabel("Ozone Generator"))

class LiquidPage(QWidget):
    def __init__(self):
        super().__init__()
        layout = QVBoxLayout(self)
        layout.addWidget(QLabel("Liquid Handler"))

def main():
    app = QApplication([])
    app.setFont(QFont("Cantarell", 16))

    w = MainWindow()
    w.show()

    app.exec()

main()
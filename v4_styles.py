BACKGROUND = "#F3F1EB"
BLUE = "#094D5A"
BUTTON = "#FFFFFF"
PRESSED = "#E6E2DA"

APP_BACKGROUND = f"QWidget {{background-color: {BACKGROUND};}}"

LOGO_BUTTON = f"""
QPushButton {{
    background-color: transparent;
    border: none;
    color: {BLUE};
    font-size: 42px;
    font-weight: bold;
    font-family: Cantarell;
}}"""

NAV_BUTTON = f"""
QPushButton {{
    background-color: transparent;
    border: none;
    color: black;
    font-size: 20px;
    font-weight: regular;
    font-family: Cantarell;
    min-height: 35px;
}}

QPushButton:hover {{
    color: {BLUE};
    background-color: transparent;
}}

QPushButton:checked {{
    background-color: transparent;
    border-bottom: 2px solid {BLUE};
}}"""

CHAMBER_BUTTON =f"""
QToolButton {{
    background-color: {BUTTON};
    color: black;
    border-radius: 8px;
    padding-top: 70px;
    font-size: 22px;
    font-weight: normal;
}}

QToolButton:hover {{
    background-color: {BACKGROUND};
}}

QToolButton:pressed {{
    background-color: {PRESSED};
}}

QToolButton:disabled {{
    background-color: {PRESSED};
}}
"""

ADD_BUTTON = f"""
QToolButton {{
    background-color: {BUTTON};
    color: black;
    border-radius: 8px;
    font-size: 22px;
    font-weight: bold;
}}

QToolButton:hover {{
    background-color: {BACKGROUND};
}}

QToolButton:pressed {{
    background-color: {PRESSED};
}}

QToolButton:disabled {{
    background-color: #F0F0F0;
    color: #A0A0A0;
}}
"""

PAGE_TITLE = """
font-size: 20px;
font-weight: bold;
"""

LINE_EDIT = """
QLineEdit {
    min-width: 50px;
    max-width: 50px;
    border: 1px solid black;
    border-radius: 2px;
    padding: 4px;
    letter-spacing: 1px;
    font-size: 14px;
}"""

ACTION_BUTTON = f"""
QPushButton {{
    background-color: transparent;
    color: {BLUE};
    border: 2px solid {BLUE};
    border-radius: 15px;
    font-weight: bold;
}}

QPushButton:hover {{
    color: {BLUE};
    border: 2px solid {BLUE};
}}

QPushButton:pressed {{
    background-color: {BLUE};
    border: 2px solid {BLUE};
    color: white;
}}
"""

MFC_BUTTON = f"""
QToolButton {{
    background-color: {BUTTON};
    color: black;
    border-radius: 4px;
    padding-top: 10px;
    font-size: 22px;
    font-weight: regular;
}}

QToolButton:hover {{
    background-color: {BACKGROUND};
}}

QToolButton:pressed {{
    background-color: {PRESSED};
}}

QToolButton:disabled {{
    background-color: {PRESSED};
}}

QToolButton:checked {{
    background-color: {PRESSED};
}}
"""

MFC_ADD_BUTTON = f"""
QToolButton {{
    background-color: {BUTTON};
    color: black;
    border-radius: 4px;
    padding-top: 10px;
    font-size: 22px;
    font-weight: bold;
}}

QToolButton:hover {{
    background-color: {BACKGROUND};
}}

QToolButton:pressed {{
    background-color: {PRESSED};
}}

QToolButton:disabled {{
    background-color: #F0F0F0;
    color: #A0A0A0;
}}
"""

TABLE = f"""
QTableWidget {{
    border: 2px solid black;
    background-color: {BACKGROUND};
    gridline-color: #D0D0D0;
}}

QHeaderView::section {{
    background-color: {BACKGROUND};
    font-weight: bold;
    padding: 4px;
}}

QTableWidget::item:selected {{
    background-color: {BLUE};
    color: white;
}}
"""

WIRE_BUTTON = f"""
    QPushButton {{
        background-color: transparent;
        color: {BLUE};
        border: 2px solid {BLUE};
        border-radius: 4px;
        font-weight: bold;
    }}

    QPushButton:checked {{
        background-color: {BLUE};
        color: white;
        border: 2px solid {BLUE};
    }}

    QPushButton:hover {{
        border: 2px solid {BLUE};
    }}
"""

AM_PM = f"""
QToolButton {{
    background-color: transparent;
    color: {BLUE};
    border: 1.5px solid {BLUE};
    border-radius: 10px;
    padding: 4px 10px;
    font-size: 12px;
    font-weight: regular;
}}

QToolButton:!checked {{
    background-color: transparent;
    color: {BLUE};
    border: 1.5px solid {BLUE};
}}

QToolButton:checked {{
    background-color: {BLUE};
    color: white;
    border: 1.5px solid {BLUE};
}}
"""

RUN_BUTTON = """
    QPushButton {
        background-color: transparent;
        color: #22C55E;
        border: 2px solid #22C55E;
        border-radius: 8px;
        font-size: 14px;
        font-weight: 600;
        padding: 6px 12px;
    }

    QPushButton:hover {
        background-color: #22C55E;
        color: white;
    }

    QPushButton:pressed {
        background-color: #16A34A;
        border: 2px solid #16A34A;
        color: white;
    }"""

RESET_BUTTON = """
    QPushButton {
        background-color: transparent;
        color: #EF4444;
        border: 2px solid #EF4444;
        border-radius: 8px;
        font-size: 14px;
        font-weight: 600;
        padding: 6px 12px;
    }

    QPushButton:hover {
        background-color: #EF4444;
        color: white;
    }

    QPushButton:pressed {
        background-color: #DC2626;
        border: 2px solid #DC2626;
        color: white;
    }"""

PAUSE_BUTTON = f"""
    QPushButton {{
        background-color: transparent;
        color: #F59E0B;
        border: 2px solid #F59E0B;
        border-radius: 8px;
        font-size: 14px;
        font-weight: 600;
        padding: 6px 12px;
    }}

    QPushButton:hover {{
        background-color: #F59E0B;
        color: white;
    }}

    QPushButton:pressed {{
        background-color: #D97706;
        border: 2px solid #D97706;
        color: white;
    }}"""

STOPWATCH = f"""
    QLabel {{
        background-color: transparent;
        color: black;
        border:2px solid black;
        border-radius: 8px;
        font-weight: Regular;
        font-size: 20px;
        padding: 6px 12px;

    }}"""

CONFIG_BUTTON = f"""
QToolButton {{
    background-color: {BACKGROUND};
    color: black;
    border-radius: 4px;
    padding-top: 10px;
    font-size: 22px;
    font-weight: normal;
}}

QToolButton:hover {{
    background-color: {PRESSED};
}}

QToolButton:pressed {{
    background-color: {PRESSED};
}}

QToolButton:disabled {{
    background-color: {PRESSED};
}}

QToolButton:checked {{
    background-color: {PRESSED};
}}
"""

PLOT_BUTTON = f"""
QToolButton {{
    background-color: {BACKGROUND};
    color: black;
    border-radius: 4px;
    font-size: 22px;
    font-weight: normal;
}}

QToolButton:hover {{
    background-color: {PRESSED};
}}

QToolButton:pressed {{
    background-color: {PRESSED};
}}

QToolButton:disabled {{
    background-color: {PRESSED};
}}

QToolButton:checked {{
    background-color: {PRESSED};
}}
"""
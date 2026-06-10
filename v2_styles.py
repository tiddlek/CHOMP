# COLORS

BACKGROUND = "#F5F6FA"
BLUE = "#2C5158"
ORANGE = "#F0B197"

MFC1 = "#4F8A5B"
MFC2 = "#7A5EA8"


APP_BACKGROUND = f"""
QWidget {{
    background-color: {BACKGROUND};
}}
"""
# ---------------------------------
# NAVIGATION
# ---------------------------------

NAV_BUTTON = f"""
QPushButton {{
    background-color: transparent;
    border: none;
    color: black;
    font-size: 18px;
    font-weight: regular;
    font-family: Cantarell;
}}

QPushButton:hover {{
    color: {ORANGE};
    background-color: transparent;
}}

QPushButton:checked {{
    color: {ORANGE};
    background-color: transparent;
}}
"""

LOGO_BUTTON = f"""
QPushButton {{
    background-color: transparent;
    border: none;
    color: {BLUE};
    font-size: 36px;
    font-weight: bold;
    font-family: Cantarell;
}}

QPushButton:hover {{
    color: {BLUE};
}}

QPushButton:checked {{
    color: {BLUE};
}}
"""


# ---------------------------------
# INPUTS
# ---------------------------------

LINE_EDIT = """
QLineEdit {
    border: 1px solid black;
    border-radius: 4px;
    padding: 4px;
    letter-spacing: 1px;
    font-size: 14px;
}

QLineEdit:focus {
    border: 2px solid #2563EB;
}
"""


TOOL_BUTTON = f"""
QToolButton {{
    background-color: transparent;
    color: {BLUE};
    border: 1.5px solid {BLUE};
    border-radius: 10px;
    padding: 4px 10px;
    font-size: 12px;
    font-weight: 600;
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


# ---------------------------------
# ACTION BUTTONS
# ---------------------------------

ACTION_BUTTON = f"""
QPushButton {{
    background-color: transparent;
    color: {BLUE};
    border: 2px solid {BLUE};
    border-radius: 15px;
    font-weight: bold;
}}

QPushButton:hover {{
    color: {ORANGE};
    border: 2px solid {ORANGE};
}}

QPushButton:pressed {{
    background-color: {ORANGE};
    border: 2px solid {ORANGE};
    color: white;
}}
"""


# ---------------------------------
# TABLES
# ---------------------------------

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
    background-color: {ORANGE};
    color: black;
}}
"""


# ---------------------------------
# TITLES
# ---------------------------------

SECTION_TITLE = """
font-size: 18px;
font-weight: bold;
"""

LIGHT_BUTTON = """
QPushButton {
    background-color: #2C5158;
    border: none;
    border-radius: 7px;
}
QPushButton:hover { background-color: #3A6871; }
QPushButton:checked { background-color: #F0B197; }

"""
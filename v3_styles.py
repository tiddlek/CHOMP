BACKGROUND = "#F0F3F9"
BLUE = "#094D5A"

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

CHAMBER_BUTTON = """
QToolButton {
    background-color: white;
    color: black;
    border: 1px solid #D0D0D0;
    border-radius: 12px;
    padding-top: 70px;
    font-size: 22px;
    font-weight: regular;
}

QToolButton:hover {
    background-color: #F7F7F7;
}

QToolButton:pressed {
    background-color: #EAEAEA;
}

QToolButton:disabled {
    background-color: #F0F0F0;
    color: #A0A0A0;
}
"""

ADD_BUTTON = """
QToolButton {
    background-color: white;
    color: black;
    border: 1px solid #D0D0D0;
    border-radius: 12px;
    font-size: 22px;
    font-weight: bold;
}

QToolButton:hover {
    background-color: #F7F7F7;
}

QToolButton:pressed {
    background-color: #EAEAEA;
}

QToolButton:disabled {
    background-color: #F0F0F0;
    color: #A0A0A0;
}
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
    border-radius: 4px;
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

MFC_BUTTON = """
QToolButton {
    background-color: white;
    color: black;
    border: 1px solid #D0D0D0;
    border-radius: 12px;
    padding-top: 10px;
    font-size: 22px;
    font-weight: regular;
}

QToolButton:hover {
    background-color: #F7F7F7;
}

QToolButton:pressed {
    background-color: #EAEAEA;
}

QToolButton:disabled {
    background-color: #F0F0F0;
    color: #A0A0A0;
}
"""

MFC_ADD_BUTTON = """
QToolButton {
    background-color: white;
    color: black;
    border: 1px solid #D0D0D0;
    border-radius: 12px;
    padding-top: 10px;
    font-size: 22px;
    font-weight: bold;
}

QToolButton:hover {
    background-color: #F7F7F7;
}

QToolButton:pressed {
    background-color: #EAEAEA;
}

QToolButton:disabled {
    background-color: #F0F0F0;
    color: #A0A0A0;
}
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
    color: black;
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

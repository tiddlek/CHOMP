BACKGROUND = "#E5E8EF"
BLUE = "#32497A"

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
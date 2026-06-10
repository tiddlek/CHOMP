BACKGROUND = "#F5F6FA"
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
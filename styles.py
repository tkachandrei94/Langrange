# Material Design theme in blue-gray colors
MAIN_STYLE = """
    QWidget {
        background-color: #ECEFF1;  /* Светло-голубой фон */
        color: #37474F;  /* Темно-серый текст */
        font-family: 'Segoe UI', Arial, sans-serif;
    }

    QPushButton {
        background-color: #90A4AE;  /* Голубовато-серый */
        color: white;
        border: none;
        padding: 8px 16px;
        border-radius: 4px;
        font-weight: bold;
    }

    QPushButton:hover {
        background-color: #78909C;  /* Темнее при наведении */
    }

    QPushButton:pressed {
        background-color: #607D8B;  /* Еще темнее при нажатии */
    }

    QLineEdit {
        background-color: white;
        border: 1px solid #B0BEC5;
        border-radius: 4px;
        padding: 6px;
    }

    QLineEdit:focus {
        border: 2px solid #78909C;
    }

    QLabel {
        color: #37474F;
    }

    QComboBox {
        background-color: white;
        border: 1px solid #B0BEC5;
        border-radius: 4px;
        padding: 6px;
    }

    QComboBox:hover {
        border: 1px solid #78909C;
    }

    QSpinBox {
        background-color: white;
        border: 1px solid #B0BEC5;
        border-radius: 4px;
        padding: 6px;
    }

    QRadioButton {
        spacing: 18px;
    }

    QComboBox {
        font-size: 12px;
        font-weight: bold;
        color: #455A64;
        background: #f0f0f0;
        border: 1px solid #333;
        border-radius: 5px;
        padding: 4px 8px;
    }
    QComboBox QAbstractItemView {
        font-size: 12px;
        color: #455A64;
        background: #ffffff;
        selection-background-color: #a5f7b2;
    }
    QComboBox QLabel {
        font-size: 12px;
        color: #455A64;
        background: #ffffff;
        selection-background-color: #a5f7b2;
    }
    QComboBox QLabel {
        font-size: 12px;
        color: #455A64;
        background: #ffffff;
        selection-background-color: #a5f7b2;
    }
"""

# Специальные стили для конкретных элементов
STEP_TITLE_STYLE = """
    QLabel {
        font-size: 20px;
        font-weight: bold;
        color: #455A64;
        padding: 10px 0;
    }
"""

CONCLUSION_CONTAINER_STYLE = """
    QFrame {
        background-color: white;
        border: 2px solid #90A4AE;
        border-radius: 8px;
        padding: 15px;
    }
"""

CONCLUSION_TITLE_STYLE = """
    QLabel {
        font-size: 16px;
        font-weight: bold;
        color: #455A64;
        padding-bottom: 10px;
    }
"""

FEEDBACK_STYLE = """
    QLabel {
        padding: 16px;
        color: #455A64;
        border-radius: 4px;
    }
"""

NAVIGATION_BUTTON_STYLE = """
    QPushButton {
        min-width: 100px;
        padding: 10px 20px;
        font-size: 14px;
    }
"""

INACTIVE_NEXT_BUTTON_STYLE = """
QPushButton {
    border: 2px solid #333;
    border-radius: 4px;
    background-color: #e0e0e0;
    color: #888;
    font-size: 16px;
    font-weight: bold;
    padding: 6px;
}
"""

ACTIVE_NEXT_BUTTON_STYLE = """
QPushButton {
    border: 2px solid #333;
    border-radius: 4px;
    background-color: #a5f7b2;  /* светло-зеленый */
    color: black;
    font-size: 16px;
    font-weight: bold;
    padding: 6px;
}
QPushButton:hover {
    background-color: #7be495;
}
"""
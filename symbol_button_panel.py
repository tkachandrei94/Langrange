# symbol_button_panel.py
from PyQt6.QtWidgets import QHBoxLayout, QPushButton

class SymbolButtonPanel(QHBoxLayout):
    def __init__(self, symbols, target_entry, parent=None):
        super().__init__(parent)
        self.addStretch()  # Чтобы кнопки были справа
        for symbol in symbols:
            button = QPushButton(symbol)
            button.setFixedSize(30, 30)
            button.setStyleSheet("""
                QPushButton {
                    color: #000000;
                    border: 1px solid #333;
                    border-radius: 5px;
                    background-color: #f0f0f0;
                    font-size: 16px;
                    font-weight: bold;
                    padding: 2px;
                    margin: 1px;
                }
                QPushButton:hover {
                    background-color: #e0e0e0;
                    border: 1px solid #000;
                }
                QPushButton:pressed {
                    background-color: #d0d0d0;
                }
            """)
            button.clicked.connect(lambda _, s=symbol: self.insert_symbol(target_entry, s))
            self.addWidget(button)

    def insert_symbol(self, entry, symbol):
        current_text = entry.text()
        cursor_pos = entry.cursorPosition()
        new_text = current_text[:cursor_pos] + symbol + current_text[cursor_pos:]
        entry.setText(new_text)
        entry.setCursorPosition(cursor_pos + len(symbol))
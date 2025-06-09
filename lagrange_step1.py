import re
from PyQt6.QtWidgets import QWidget, QLabel, QVBoxLayout, QPushButton, QLineEdit, QGridLayout, QHBoxLayout
from PyQt6.QtGui import QRegularExpressionValidator
from PyQt6.QtCore import QRegularExpression
from test_config import test_config_step1
from styles import MAIN_STYLE, STEP_TITLE_STYLE, CONCLUSION_CONTAINER_STYLE, CONCLUSION_TITLE_STYLE, FEEDBACK_STYLE, NAVIGATION_BUTTON_STYLE
from sympy import Symbol, sympify, SympifyError
from PyQt6.QtWidgets import QMessageBox

class LagrangeStep1(QWidget):
    def __init__(self, parent, switch_step_callback):
        super().__init__(parent)
        self.setStyleSheet(MAIN_STYLE)
        self.switch_step = switch_step_callback
        self.num_variables = 2
        self.num_constraints = 1
        self.function_entry = None
        self.constraint_entries = []
        self.variables = ['x', 'y']

        self.layout = QVBoxLayout(self)
        self.instruction_label = QLabel("<b>Етап 1: Запис функції Лагранжа</b><br>"
                                       "Введіть цільову функцію (F) та обмеження (g).<br>"
                                       "<b>Примітка:</b> Використовуйте '*' для множення (наприклад, 2*x).<br>"
                                       "Для множників Лагранжа використовуйте <b>λ1</b>, <b>λ2</b> і так далі.")
        self.instruction_label.setStyleSheet(STEP_TITLE_STYLE)
        self.layout.addWidget(self.instruction_label)

        self.function_layout = QHBoxLayout()
        self.function_label = QLabel("Цільова функція (F)(")
        self.function_label.setStyleSheet(STEP_TITLE_STYLE)

        self.function_entry = QLineEdit()
        self.function_entry.setText(test_config_step1[0] if test_config_step1 else "")
        self.function_entry.setStyleSheet(STEP_TITLE_STYLE)
        self.function_layout.addWidget(self.function_label, 2)
        self.function_layout.addWidget(self.function_entry, 5)
        self.layout.addLayout(self.function_layout)
        self.layout.addSpacing(30)

        self.constraints_grid_layout = QGridLayout()
        self.layout.addLayout(self.constraints_grid_layout)

        # Кнопка "Далі"
        self.next_button = QPushButton("Далі")
        self.next_button.setStyleSheet(NAVIGATION_BUTTON_STYLE)
        self.next_button.clicked.connect(self._go_to_next_step) # Змінено назву методу
        self.layout.addWidget(self.next_button)

        self.setLayout(self.layout)

    def create_symbol_button(self, symbol, target_entry):
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
        button.clicked.connect(lambda: self.insert_symbol(target_entry, symbol))
        return button

    def insert_symbol(self, entry, symbol):
        current_text = entry.text()
        cursor_pos = entry.cursorPosition()
        new_text = current_text[:cursor_pos] + symbol + current_text[cursor_pos:]
        entry.setText(new_text)
        entry.setCursorPosition(cursor_pos + len(symbol))

    def create_symbol_panel(self, target_entry):
        panel = QHBoxLayout()
        panel.addStretch()  # Добавляем stretch в начало, чтобы кнопки были справа
        symbols = ['λ', '+', '-', '*', '/']
        
        for symbol in symbols:
            button = self.create_symbol_button(symbol, target_entry)
            panel.addWidget(button)
        return panel

    def setup_input_fields(self, variables, num_constraints):
        self.variables = variables
        self.num_constraints = num_constraints

        layouts_to_remove = []
        for i in reversed(range(self.layout.count())):
            item = self.layout.itemAt(i)
            # Удаляем только QHBoxLayout/QVBoxLayout, которые не function_layout, constraints_grid_layout или instruction_label
            if isinstance(item, QHBoxLayout) or isinstance(item, QVBoxLayout):
                if item is not self.function_layout and item is not self.constraints_grid_layout:
                    layouts_to_remove.append(i)
        for i in layouts_to_remove:
            item = self.layout.takeAt(i)
            # Удаляем все виджеты из layout
            while item.count():
                subitem = item.takeAt(0)
                widget = subitem.widget()
                if widget is not None:
                    widget.deleteLater()

        # Оновлення тексту для цільової функції
        self.function_label.setText(f"Цільова функція (F)({', '.join(self.variables)}):")

        # Очищення попередніх полів обмежень
        for i in reversed(range(self.constraints_grid_layout.count())):
            widget = self.constraints_grid_layout.itemAt(i).widget()
            if widget is not None:
                widget.deleteLater()
        self.constraint_entries = []

        # Створення полів для обмежень
        for i in range(self.num_constraints):
            # Создаем контейнер для каждой строки
            row_container = QVBoxLayout()
            
            # Создаем горизонтальный layout для label и entry
            input_layout = QHBoxLayout()
            
            constraint_label = QLabel(f"Обмеження {i + 1} (g{i + 1})({', '.join(self.variables)}):")
            constraint_label.setStyleSheet(STEP_TITLE_STYLE)
            constraint_entry = QLineEdit()
            constraint_entry.setStyleSheet(STEP_TITLE_STYLE)
            constraint_entry.setText(test_config_step1[i + 1] if test_config_step1 else "")
            
            # Создаем панель с символами
            symbol_panel = self.create_symbol_panel(constraint_entry)
            row_container.addLayout(symbol_panel)

            input_layout.addWidget(constraint_label, 2)
            input_layout.addWidget(constraint_entry, 5)
            
            # Добавляем input_layout в контейнер строки
            row_container.addLayout(input_layout)
            
            # Добавляем контейнер в grid
            self.constraints_grid_layout.addLayout(row_container, i, 0, 1, 2)
            self.constraint_entries.append(constraint_entry)

        # Добавляем панель символов для целевой функции перед полем ввода
        function_symbol_panel = self.create_symbol_panel(self.function_entry)
        self.layout.insertLayout(1, function_symbol_panel)  # Вставляем перед полем ввода функции

        # Регулярний вираз для дозволених символів
        allowed_chars = QRegularExpression(r"^[0-9" + "".join(self.variables) + r"λλ\+\-\*\/\^\.\,\s()\*]*$")
        validator = QRegularExpressionValidator(allowed_chars)
        self.function_entry.setValidator(validator)
        for entry in self.constraint_entries:
            entry.setValidator(validator)

    def get_constraint_texts(self):
        return [entry.text() for entry in self.constraint_entries]

    def validate_expression(self, expression):
        try:
            # Создаем словарь с переменными
            symbol_map = {var: Symbol(var) for var in self.variables}
            # Добавляем лямбду в словарь
            symbol_map['λ'] = Symbol('λ')
            
            # Пробуем преобразовать выражение
            sympify(expression, locals=symbol_map)
            return True
        except (SympifyError, SyntaxError) as e:
            return False
        
    def _go_to_next_step(self):
        function_str = self.function_entry.text()
        constraint_strs = self.get_constraint_texts()

        # Проверяем целевой функцию
        if not self.validate_expression(function_str):
            QMessageBox.warning(
                self,
                "Помилка введення",
                "Неправильний формат цільової функції. Перевірте правильність введення."
            )
            return

        # Проверяем ограничения
        for i, constraint in enumerate(constraint_strs):
            if not self.validate_expression(constraint):
                QMessageBox.warning(
                    self,
                    "Помилка введення",
                    f"Неправильний формат обмеження {i + 1}. Перевірте правильність введення."
                )
                return

        # Если все проверки пройдены, переходим к следующему шагу
        self.switch_step(2, 
                        function_str=function_str, 
                        constraint_strs=constraint_strs, 
                        variables=self.variables, 
                        num_constraints=self.num_constraints)
        
    def auto_multiply(self, expression):
        return expression
    
    def closeEvent(self, event):
        """Обработчик закрытия виджета"""
        print('Закрытие шага 1...')
        # Очищаем ресурсы
        event.accept()
import re
from PyQt6.QtWidgets import QWidget, QLabel, QVBoxLayout, QPushButton, QLineEdit, QGridLayout, QHBoxLayout
from PyQt6.QtGui import QRegularExpressionValidator
from PyQt6.QtCore import QRegularExpression

class LagrangeStep1(QWidget):
    def __init__(self, parent, switch_step_callback):
        super().__init__(parent)
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
        self.layout.addWidget(self.instruction_label)

        self.function_layout = QHBoxLayout()
        self.function_label = QLabel("Цільова функція (F)(")

        # TODO 
        self.test1 = "x * y"
        self.test2 = "2 * x + y - 5"

        self.function_entry = QLineEdit()
        self.function_entry.setText(self.test1)
        self.function_layout.addWidget(self.function_label)
        self.function_layout.addWidget(self.function_entry)
        self.layout.addLayout(self.function_layout)

        self.constraints_grid_layout = QGridLayout()
        self.layout.addLayout(self.constraints_grid_layout)

        # Кнопка "Далі"
        self.next_button = QPushButton("Далі")
        self.next_button.clicked.connect(self._go_to_next_step) # Змінено назву методу
        self.layout.addWidget(self.next_button)

        self.setLayout(self.layout)

    def setup_input_fields(self, variables, num_constraints):
        self.variables = variables
        self.num_constraints = num_constraints

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
            constraint_label = QLabel(f"Обмеження {i + 1} (g{i + 1})({', '.join(self.variables)}):")
            constraint_entry = QLineEdit()
            constraint_entry.setText(self.test2)
            self.constraints_grid_layout.addWidget(constraint_label, i, 0)
            self.constraints_grid_layout.addWidget(constraint_entry, i, 1)
            self.constraint_entries.append(constraint_entry)

        # Регулярний вираз для дозволених символів (додано 'λ')
        allowed_chars = QRegularExpression(r"^[0-9" + "".join(self.variables) + r"λλ\+\-\*\/\^\.\,\s()\*]*$")
        validator = QRegularExpressionValidator(allowed_chars)
        self.function_entry.setValidator(validator)
        for entry in self.constraint_entries:
            entry.setValidator(validator)

    def get_constraint_texts(self):
        print("constraint_entries:", self.constraint_entries)
        return [entry.text() for entry in self.constraint_entries]

    def _go_to_next_step(self): # Внутрішній метод для обробки натискання "Далі"
        function_str = self.function_entry.text()
        constraint_strs = self.get_constraint_texts()
        self.switch_step(2, function_str=function_str, constraint_strs=constraint_strs, variables=self.variables, num_constraints=self.num_constraints)

    def auto_multiply(self, expression):
        return expression
    
    def closeEvent(self, event):
        """Обработчик закрытия виджета"""
        print('Закрытие шага 1...')
        # Очищаем ресурсы
        event.accept()
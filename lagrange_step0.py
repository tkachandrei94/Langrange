from PyQt6.QtWidgets import QWidget, QLabel, QVBoxLayout, QSpinBox, QPushButton, QHBoxLayout

class LagrangeStep0(QWidget):
    def __init__(self, parent, switch_step_callback):
        super().__init__(parent)
        self.switch_step = switch_step_callback

        layout = QVBoxLayout(self)

        # Введення кількості змінних
        variables_layout = QHBoxLayout()
        variables_label = QLabel("Введіть кількість змінних (x, y, z, q, w):")
        variables_layout.addWidget(variables_label)
        self.num_variables_spinbox = QSpinBox()
        self.num_variables_spinbox.setMinimum(2)  # Мінімум 2 змінні (x, y)
        self.num_variables_spinbox.setMaximum(5)
        self.num_variables_spinbox.setValue(2)  # Значення за замовчуванням
        variables_layout.addWidget(self.num_variables_spinbox)
        layout.addLayout(variables_layout)

        # Введення кількості обмежень
        constraints_layout = QHBoxLayout()
        constraints_label = QLabel("Введіть кількість обмежень:")
        constraints_layout.addWidget(constraints_label)
        self.num_constraints_spinbox = QSpinBox()
        self.num_constraints_spinbox.setMinimum(0)  # Може бути 0 обмежень
        self.num_constraints_spinbox.setMaximum(5)
        self.num_constraints_spinbox.setValue(1)  # Значення за замовчуванням
        constraints_layout.addWidget(self.num_constraints_spinbox)
        layout.addLayout(constraints_layout)

        self.next_button = QPushButton("Далі")
        self.next_button.clicked.connect(self.go_to_next_step)
        layout.addWidget(self.next_button)

        self.setLayout(layout)

    def go_to_next_step(self):
        num_variables = self.num_variables_spinbox.value()
        num_constraints = self.num_constraints_spinbox.value()
        self.switch_step(1, num_variables=num_variables, num_constraints=num_constraints)

    def closeEvent(self, event):
        """Обработчик закрытия виджета"""
        print('Закрытие шага 0...')
        # Очищаем ресурсы
        event.accept()
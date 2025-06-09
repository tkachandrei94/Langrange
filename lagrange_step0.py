from PyQt6.QtWidgets import QWidget, QLabel, QVBoxLayout, QSpinBox, QPushButton, QHBoxLayout
from test_config import test_config_step0
from styles import MAIN_STYLE, STEP_TITLE_STYLE, CONCLUSION_CONTAINER_STYLE, CONCLUSION_TITLE_STYLE, FEEDBACK_STYLE, NAVIGATION_BUTTON_STYLE

class LagrangeStep0(QWidget):
    def __init__(self, parent, switch_step_callback):
        super().__init__(parent)
        self.setStyleSheet(MAIN_STYLE)
        self.switch_step = switch_step_callback

        layout = QVBoxLayout(self)
        default_num_variables = 2
        default_num_constraints = 1
        
        num_variables = test_config_step0[0] if test_config_step0 else default_num_variables
        num_constraints = test_config_step0[1] if test_config_step0 else default_num_constraints

        layout.addStretch()

        # Введення кількості змінних
        variables_layout = QHBoxLayout()
        variables_label = QLabel("Введіть кількість змінних (x, y, z, q, w):")
        variables_label.setStyleSheet(STEP_TITLE_STYLE)
        variables_layout.addWidget(variables_label)
        self.num_variables_spinbox = QSpinBox()
        self.num_variables_spinbox.setMinimum(2)
        self.num_variables_spinbox.setMaximum(5)
        self.num_variables_spinbox.setValue(num_variables )  # Значення за замовчуванням
        variables_layout.addWidget(self.num_variables_spinbox)
        layout.addLayout(variables_layout)

        # Введення кількості обмежень
        constraints_layout = QHBoxLayout()
        constraints_label = QLabel("Введіть кількість обмежень:")
        constraints_label.setStyleSheet(STEP_TITLE_STYLE)
        constraints_layout.addWidget(constraints_label)
        self.num_constraints_spinbox = QSpinBox()
        self.num_constraints_spinbox.setMinimum(0)  # Може бути 0 обмежень
        self.num_constraints_spinbox.setMaximum(5)
        self.num_constraints_spinbox.setValue(num_constraints)  # Значення за замовчуванням
        constraints_layout.addWidget(self.num_constraints_spinbox)

        layout.addLayout(constraints_layout)
        layout.addStretch()

        self.next_button = QPushButton("Далі")
        self.next_button.setFixedHeight(50)
        self.next_button.setStyleSheet("""
            QPushButton {
                border: 2px solid #333;
                border-radius: 10px;
                background-color: #f0f0f0;
                color: black;
                font-size: 16px;
                font-weight: bold;
                padding: 10px;
            }
        """)

        self.next_button.clicked.connect(self.go_to_next_step)
        layout.addWidget(self.next_button)

        self.setLayout(layout)

    def go_to_next_step(self):
        print("LagrangeStep0 go_to_next_step")
        print("num_variables:", self.num_variables_spinbox.value())
        print("num_constraints:", self.num_constraints_spinbox.value())

        num_variables = self.num_variables_spinbox.value()
        num_constraints = self.num_constraints_spinbox.value()
        self.switch_step(1, num_variables=num_variables, num_constraints=num_constraints)

    def closeEvent(self, event):
        """Обработчик закрытия виджета"""
        print('Закрытие шага 0...')
        # Очищаем ресурсы
        event.accept()
from PyQt6.QtWidgets import QWidget, QLabel, QVBoxLayout, QPushButton, QHBoxLayout, QLineEdit, QButtonGroup, \
    QRadioButton, QSpacerItem, QSizePolicy # Додано QSpacerItem, QSizePolicy
from PyQt6.QtCore import Qt
import sympy as sp


class LagrangeStep6(QWidget):
    def __init__(self, parent=None, switch_step_callback=None):
        super().__init__(parent)
        self.switch_step = switch_step_callback
        self.determinant_value = None
        self.solutions = {}
        self.function_str = ""
        self.variables = []

        # TODO remove
        self.test = ["5/4", "5/2", "25/8"]

        main_layout = QVBoxLayout()
        main_layout.setAlignment(Qt.AlignmentFlag.AlignTop)

        instruction_label = QLabel("<b>Етап 6: Аналіз розв'язку та висновок</b><br>"
                                   "На цьому етапі ви можете переглянути отримані рішення та зробити висновки.")
        main_layout.addWidget(instruction_label)
        main_layout.addSpacing(10)

        self.solution_point_label = QLabel("Знайдені рішення у вигляді точки:")
        main_layout.addWidget(self.solution_point_label)
        main_layout.addSpacing(5)

        self.determinant_display_label = QLabel("Значення визначника матриці Гессе (Δ):")
        main_layout.addWidget(self.determinant_display_label)
        main_layout.addSpacing(15)

        # --- Блок для візуалізації функції та підстановки ---
        # 1. Z з вибором min/max/saddle та відображенням функції
        z_extremum_function_layout = QHBoxLayout()
        z_extremum_function_layout.setAlignment(Qt.AlignmentFlag.AlignLeft)

        self.z_label = QLabel("Z")
        self.z_label.setStyleSheet("font-size: 24px; font-weight: bold;")
        z_extremum_function_layout.addWidget(self.z_label)

        self.extremum_type_group = QButtonGroup(self)
        self.max_radio = QRadioButton("max")
        self.min_radio = QRadioButton("min")
        self.saddle_radio = QRadioButton("сідлова точка")

        self.extremum_type_group.addButton(self.max_radio, 1)
        self.extremum_type_group.addButton(self.min_radio, 2)
        self.extremum_type_group.addButton(self.saddle_radio, 3)
        # При зміні радіокнопки оновлюємо відображення функції
        self.extremum_type_group.buttonClicked.connect(self.update_z_function_display)
        self.extremum_type_group.buttonClicked.connect(self.check_extremum_type)

        extremum_radio_layout = QVBoxLayout()
        extremum_radio_layout.addWidget(self.max_radio)
        extremum_radio_layout.addWidget(self.min_radio)
        extremum_radio_layout.addWidget(self.saddle_radio)
        extremum_radio_layout.setContentsMargins(0, 0, 0, 0)
        extremum_radio_layout.setSpacing(0)

        z_with_options_layout = QVBoxLayout()
        z_with_options_layout.addWidget(self.z_label,
                                        alignment=Qt.AlignmentFlag.AlignBottom | Qt.AlignmentFlag.AlignLeft)
        z_with_options_layout.addLayout(extremum_radio_layout)
        z_with_options_layout.setContentsMargins(0, 0, 0, 0)
        z_with_options_layout.setSpacing(0)

        z_extremum_function_layout.addLayout(z_with_options_layout)

        # Новий QLabel для відображення " = x * y"
        self.z_function_display_label = QLabel("")
        self.z_function_display_label.setStyleSheet("font-size: 18px;")
        z_extremum_function_layout.addWidget(self.z_function_display_label)


        main_layout.addLayout(z_extremum_function_layout)
        main_layout.addSpacing(10)

        # 2. Рядок для підстановки значень та вводу результату: F( [_x_] , [_y_] ) = [_результат_]
        # Новий QHBoxLayout для всього рядка F(...)
        substitution_full_layout = QHBoxLayout()
        substitution_full_layout.setAlignment(Qt.AlignmentFlag.AlignLeft)

        # Створюємо внутрішній QHBoxLayout для "F(" та змінних.
        # Це дозволить нам краще контролювати простір всередині дужок.
        f_and_variables_layout = QHBoxLayout()
        f_and_variables_layout.setContentsMargins(0, 0, 0, 0) # Прибираємо внутрішні відступи
        f_and_variables_layout.setSpacing(0) # Прибираємо стандартні проміжки

        f_and_variables_layout.addWidget(QLabel("F("))

        # self.substitution_variables_inputs_layout тепер буде вкладатися в f_and_variables_layout
        self.substitution_variables_inputs_layout = QHBoxLayout()
        self.substitution_variables_inputs_layout.setContentsMargins(0, 0, 0, 0)
        self.substitution_variables_inputs_layout.setSpacing(5) # Невеликий простір між полями

        f_and_variables_layout.addLayout(self.substitution_variables_inputs_layout)

        f_and_variables_layout.addWidget(QLabel(")")) # Дужка після змінних

        # Додаємо внутрішній layout до повного рядка підстановки
        substitution_full_layout.addLayout(f_and_variables_layout)

        substitution_full_layout.addWidget(QLabel(" = "))

        self.final_function_value_entry = QLineEdit()
        self.final_function_value_entry.setPlaceholderText("Обчислити значення")
        self.final_function_value_entry.setFixedWidth(40)
        substitution_full_layout.addWidget(self.final_function_value_entry)

        # Додаємо "розтягувач" (spacer) в кінці, щоб все притиснулося до лівого краю
        substitution_full_layout.addSpacerItem(
            QSpacerItem(0, 0, QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Minimum))  # ВИПРАВЛЕНО ТУТ!

        main_layout.addLayout(substitution_full_layout)
        main_layout.addSpacing(15)

        self.extremum_feedback_label = QLabel("")
        main_layout.addWidget(self.extremum_feedback_label)

        self.function_value_feedback_label = QLabel("")
        main_layout.addWidget(self.function_value_feedback_label)
        main_layout.addSpacing(15)

        self.check_function_value_button = QPushButton("Перевірити значення та тип екстремуму")
        self.check_function_value_button.clicked.connect(self.check_all_values)
        main_layout.addWidget(self.check_function_value_button, alignment=Qt.AlignmentFlag.AlignLeft)

        self.conclusion_instruction_label = QLabel("<b>Зробіть висновок:</b><br>"
                                                   "На основі значення визначника (Δ) та ваших знань, визначте, чи є знайдена точка локальним мінімумом, максимумом чи сідловою точкою.<br>"
                                                   "<ul>"
                                                   "<li>Якщо Δ > 0 і $L_{xx} > 0$ (або $F_{xx} > 0$), то це локальний мінімум.</li>"
                                                   "<li>Якщо Δ > 0 і $L_{xx} < 0$ (або $F_{xx} < 0$), то це локальний максимум.</li>"
                                                   "<li>Якщо Δ < 0, то це сідлова точка.</li>"
                                                   "<li>Якщо Δ = 0, потрібен додатковий аналіз.</li>"
                                                   "</ul>"
                                                   "*(Примітка: $L_{xx}$ - це друга часткова похідна функції Лагранжа за змінною x, або $F_{xx}$ для цільової функції, якщо обмежень немає і ви працюєте з нею напряму.)*")
        main_layout.addWidget(self.conclusion_instruction_label)
        main_layout.addSpacing(20)

        navigation_layout = QHBoxLayout()
        prev_button = QPushButton("Назад")
        prev_button.clicked.connect(self.go_to_prev_step)
        navigation_layout.addWidget(prev_button)

        self.restart_button = QPushButton("Почати заново")
        self.restart_button.clicked.connect(self.go_to_start)
        navigation_layout.addWidget(self.restart_button)

        main_layout.addLayout(navigation_layout)
        self.setLayout(main_layout)

        self.variable_value_entries = {}

    def set_data(self, determinant_value, solutions, function_str, variables):
        print(f"Отримано дані для 6-го етапу:")
        print(f"  determinant_value: {determinant_value}")
        print(f"  solutions: {solutions}")
        print(f"  function_str: {function_str}")
        print(f"  variables: {variables}")

        self.determinant_value = determinant_value
        self.solutions = solutions
        self.function_str = function_str
        self.variables = variables
        self.display_results()

        self.update_z_function_display()

        checked_button = self.extremum_type_group.checkedButton()
        self.extremum_type_group.setExclusive(False)
        self.max_radio.setChecked(False)
        self.min_radio.setChecked(False)
        self.saddle_radio.setChecked(False)
        self.extremum_type_group.setExclusive(True)
        if checked_button:
            checked_button.setChecked(True)

        self.extremum_feedback_label.clear()
        self.function_value_feedback_label.clear()


    def display_results(self):
        solution_point_text = "<b>Знайдені рішення у вигляді точки:</b> A("
        sorted_variables = sorted([var for var in self.variables if var in self.solutions])
        point_coords = []
        for var in sorted_variables:
            point_coords.append(f"{var}={str(self.solutions[var])}")
        solution_point_text += ", ".join(point_coords) + ")"
        self.solution_point_label.setText(solution_point_text)

        self.determinant_display_label.setText(
            f"<b>Значення визначника матриці Гессе (Δ):</b> {self.determinant_value}")

        # --- Очищення та заповнення полів вводу для підстановки ---
        while self.substitution_variables_inputs_layout.count():
            item = self.substitution_variables_inputs_layout.takeAt(0)
            if item.widget():
                item.widget().deleteLater()
            elif item.layout():
                while item.layout().count():
                    sub_item = item.layout().takeAt(0)
                    if sub_item.widget():
                        sub_item.widget().deleteLater()
                item.layout().deleteLater()
        self.variable_value_entries.clear()

        first_variable = True
        for var in sorted_variables:
            if not first_variable:
                comma_label = QLabel(", ")
                self.substitution_variables_inputs_layout.addWidget(comma_label)

            var_entry = QLineEdit()
            var_entry.setPlaceholderText(f"{var}")
            var_entry.setFixedWidth(60)
            self.variable_value_entries[var] = var_entry
            self.substitution_variables_inputs_layout.addWidget(var_entry)

            first_variable = False

        self.final_function_value_entry.clear()

    def update_z_function_display(self):
        """Оновлює відображення функції поруч з Z."""
        if self.function_str:
            self.z_function_display_label.setText(f"= {self.function_str}")
        else:
            self.z_function_display_label.clear()


    def check_all_values(self):
        self.check_extremum_type()
        self._check_function_value_internal()

    def check_extremum_type(self):
        selected_button = self.extremum_type_group.checkedButton()
        if not selected_button:
            self.extremum_feedback_label.setText("<span style='color: red;'>Будь ласка, оберіть тип екстремуму.</span>")
            return

        user_choice_id = self.extremum_type_group.checkedId()

        correct_extremum_id = None
        try:
            det = float(self.determinant_value)
            if det > 0:
                pass
            elif det < 0:
                correct_extremum_id = 3
            else:
                correct_extremum_id = 0
        except (ValueError, TypeError):
            correct_extremum_id = 0

        if correct_extremum_id == 0:
            self.extremum_feedback_label.setText(
                "<span style='color: orange;'>Неможливо визначити тип екстремуму за значенням визначника (Δ = 0 або невідомий). Потрібен додатковий аналіз.</span>")
        elif correct_extremum_id == 3:
            if user_choice_id == 3:
                self.extremum_feedback_label.setText(
                    "<span style='color: green;'>Вірно! Це сідлова точка (Δ < 0).</span>")
            else:
                self.extremum_feedback_label.setText(
                    "<span style='color: red;'>Неправильно. При Δ < 0 це завжди сідлова точка.</span>")
        elif det > 0:
            if user_choice_id == 1:
                self.extremum_feedback_label.setText(
                    "<span style='color: orange;'>Можливо вірно. Для точного визначення локального максимуму потрібно перевірити $L_{xx} < 0$.</span>")
            elif user_choice_id == 2:
                self.extremum_feedback_label.setText(
                    "<span style='color: orange;'>Можливо вірно. Для точного визначення локального мінімуму потрібно перевірити $L_{xx} > 0$.</span>")
            else:
                self.extremum_feedback_label.setText(
                    "<span style='color: red;'>Неправильно. При Δ > 0 це завжди локальний екстремум (min або max), а не сідлова точка.</span>")

    def _check_function_value_internal(self):
        user_substituted_values = {}
        all_variables_filled = True
        for var, entry in self.variable_value_entries.items():
            text = entry.text().strip()
            if not text:
                all_variables_filled = False
                break
            try:
                user_substituted_values[sp.symbols(var)] = sp.sympify(text)
            except sp.SympifyError:
                self.function_value_feedback_label.setText(
                    f"<span style='color: red;'>Будь ласка, введіть дійсний вираз для змінної {var}.</span>")
                return

        if not all_variables_filled:
            self.function_value_feedback_label.setText(
                "<span style='color: red;'>Будь ласка, заповніть всі поля для змінних.</span>")
            return

        entered_final_value_str = self.final_function_value_entry.text().strip()
        if not entered_final_value_str:
            self.function_value_feedback_label.setText(
                "<span style='color: red;'>Будь ласка, введіть обчислене значення функції.</span>")
            return

        try:
            entered_final_value = float(sp.sympify(entered_final_value_str))
        except sp.SympifyError:
            self.function_value_feedback_label.setText(
                "<span style='color: red;'>Будь ласка, введіть дійсне число або математичний вираз для фінального значення.</span>")
            return
        except ValueError:
            self.function_value_feedback_label.setText(
                "<span style='color: red;'>Будь ласка, введіть числове значення функції.</span>")
            return

        func_expr = sp.sympify(self.function_str)

        calculated_value = func_expr.subs(user_substituted_values)

        if abs(float(calculated_value) - entered_final_value) < 1e-6:
            self.function_value_feedback_label.setText(
                f"<span style='color: green;'>Значення цільової функції обчислено правильно: F = {calculated_value.evalf(4)}!</span>")
        else:
            self.function_value_feedback_label.setText(
                f"<span style='color: red;'>Неправильне значення. Очікується: F = {calculated_value.evalf(4)}.</span>")

    def go_to_prev_step(self):
        self.switch_step(5)

    def go_to_start(self):
        self.switch_step(0)


    def closeEvent(self, event):
        """Обработчик закрытия виджета"""
        print('Закрытие шага 6...')
        event.accept()
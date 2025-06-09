from PyQt6.QtWidgets import QWidget, QLabel, QVBoxLayout, QPushButton, QComboBox, QHBoxLayout, QLineEdit, QButtonGroup, \
    QRadioButton, QSpacerItem, QSizePolicy # Додано QSpacerItem, QSizePolicy
from PyQt6.QtCore import Qt
import sympy as sp
import json


class LagrangeStep6(QWidget):
    def __init__(self, parent=None, switch_step_callback=None):
        super().__init__(parent)
        
        self.main_window = parent
        self.switch_step = switch_step_callback
        self.determinant_value = None
        # self.solutions = {}
        self.function_str = ""
        self.variables = []
        self.all_solutions_data = [] # Для зберігання всіх рішень

        main_layout = QVBoxLayout()
        main_layout.setAlignment(Qt.AlignmentFlag.AlignTop)

        instruction_label = QLabel("<b>Етап 6: Аналіз розв'язку та висновок</b><br>"
                                   "На цьому етапі ви можете переглянути отримані рішення та зробити висновки.")
        main_layout.addWidget(instruction_label)
        main_layout.addSpacing(5)

        # Елементи для вибору рішення, якщо їх декілька
        self.solution_choice_label = QLabel("Оберіть рішення для аналізу:")
        self.solution_choice_label.setStyleSheet("font-weight: bold; font-size: 14pt;")
        self.solution_selector_combo = QComboBox()
        self.solution_selector_combo.currentIndexChanged.connect(self._on_solution_selected)
        
        main_layout.addWidget(self.solution_choice_label)
        main_layout.addWidget(self.solution_selector_combo)
        self.solution_choice_label.hide() # Сховати за замовчуванням
        self.solution_selector_combo.hide() # Сховати за замовчуванням
        main_layout.addSpacing(5)

        self.solution_point_label = QLabel()
        main_layout.addWidget(self.solution_point_label)
        main_layout.addSpacing(5)

        self.determinant_display_label = QLabel("Значення визначника матриці Гессе (Δ):")
        main_layout.addWidget(self.determinant_display_label)
        main_layout.addSpacing(5)

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
        self.final_function_value_entry.setMinimumWidth(100)
        
        substitution_full_layout.addWidget(self.final_function_value_entry)

        # Додаємо "розтягувач" (spacer) в кінці, щоб все притиснулося до лівого краю
        substitution_full_layout.addSpacerItem(
            QSpacerItem(0, 0, QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Minimum))  # ВИПРАВЛЕНО ТУТ!

        main_layout.addLayout(substitution_full_layout)
        main_layout.addSpacing(15)

        self.extremum_feedback_label = QLabel("")
        main_layout.addWidget(self.extremum_feedback_label)
        self.extremum_feedback_label.setWordWrap(True)
        main_layout.addSpacing(5)

        self.function_value_feedback_label = QLabel("")
        main_layout.addWidget(self.function_value_feedback_label)
        main_layout.addSpacing(15)

        self.check_function_value_button = QPushButton("Перевірити значення та тип екстремуму")
        self.check_function_value_button.clicked.connect(self.check_all_values)
        main_layout.addWidget(self.check_function_value_button, alignment=Qt.AlignmentFlag.AlignLeft)

        self.conclusion_instruction_label = QLabel("<b>Зробіть висновок:</b><br>"
                                                   "На основі значення визначника ((Δ &lt; 0)) та ваших знань, визначте, чи є знайдена точка локальним мінімумом, максимумом чи сідловою точкою.<br>"
                                                   "<ul>"
                                                   "<li>Якщо (Δ &lt; 0) > 0 і $L_{xx} > 0$ (або $F_{xx} > 0$), то це локальний мінімум.</li>"
                                                   "<li>Якщо (Δ &lt; 0) > 0 і $L_{xx} < 0$ (або $F_{xx} < 0$), то це локальний максимум.</li>"
                                                   "<li>Якщо (Δ &lt; 0) < 0, то це сідлова точка.</li>"
                                                   "<li>Якщо (Δ &lt; 0) = 0, потрібен додатковий аналіз.</li>"
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
        
        # self.all_solutions_data = self.main_window.all_solutions_step3
        # print(f"  all_solutions_step3 from main_window: {self.all_solutions_data}")

        raw_solutions_data = self.main_window.all_solutions_step3
        self.all_solutions_data = []
        if raw_solutions_data:
            for sol_dict in raw_solutions_data:
                processed_sol = {}
                for var_name, data_dict in sol_dict.items():
                    processed_data = data_dict.copy() # Копіюємо, щоб не змінювати оригінал у main_window
                    if 'float_val' in processed_data and isinstance(processed_data['float_val'], (float, int)):
                        processed_data['float_val'] = round(processed_data['float_val'], 3)
                    processed_sol[var_name] = processed_data
                self.all_solutions_data.append(processed_sol)
        print(f"  all_solutions_step3 from main_window (після округлення): {json.dumps(self.all_solutions_data, indent=2, ensure_ascii=False)}")

        self.determinant_value = determinant_value
        # self.solutions = solutions
        self.function_str = function_str
        self.variables = variables
        self.display_results()

        self._setup_solution_selector() # Налаштовуємо комбо-бокс
        self._update_display_for_current_selection() # Оновлюємо UI на основі поточного вибору (або першого рішення)

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


    def _setup_solution_selector(self):
        self.solution_selector_combo.blockSignals(True) # Блокуємо сигнали під час заповнення
        self.solution_selector_combo.clear()

        if self.all_solutions_data and len(self.all_solutions_data) > 1:
            self.solution_choice_label.show()
            self.solution_selector_combo.show()
            for i, sol_data in enumerate(self.all_solutions_data):
                # Формуємо рядок для відображення в комбо-боксі
                # Використовуємо self.variables для правильного порядку та набору змінних
                parts = []
                for var_name in sorted(self.variables): # Використовуємо self.variables для порядку
                    if var_name in sol_data:
                        parts.append(f"{var_name}={sol_data[var_name]['fraction_str']}")
                    elif str(var_name) in sol_data: # На випадок, якщо var_name це символ
                         parts.append(f"{str(var_name)}={sol_data[str(var_name)]['fraction_str']}")

                # Додаємо множники Лагранжа, якщо вони є в рішенні та не в self.variables
                for var_name in sorted(sol_data.keys()):
                    if var_name not in self.variables and var_name not in [p.split('=')[0] for p in parts]:
                         parts.append(f"{var_name}={sol_data[var_name]['fraction_str']}")
                
                solution_text = f"Рішення {i + 1}: ({', '.join(parts)})"
                self.solution_selector_combo.addItem(solution_text)
        else:
            self.solution_choice_label.hide()
            self.solution_selector_combo.hide()
        
        self.solution_selector_combo.blockSignals(False) # Розблоковуємо сигнали

    def _on_solution_selected(self):
        self._update_display_for_current_selection()

    def _update_display_for_current_selection(self):
        current_solution_to_display = None
        
        if self.solution_selector_combo.isVisible() and self.solution_selector_combo.currentIndex() != -1:
            if self.all_solutions_data and self.solution_selector_combo.currentIndex() < len(self.all_solutions_data):
                current_solution_to_display = self.all_solutions_data[self.solution_selector_combo.currentIndex()]
        elif self.all_solutions_data: # Одне рішення, комбо-бокс невидимий
            current_solution_to_display = self.all_solutions_data[0]

        # Очищення полів вводу для підстановки перед заповненням
        while self.substitution_variables_inputs_layout.count():
            item = self.substitution_variables_inputs_layout.takeAt(0)
            widget_to_delete = item.widget()
            if widget_to_delete:
                widget_to_delete.deleteLater()
            layout_to_delete = item.layout()
            if layout_to_delete:
                while layout_to_delete.count():
                    sub_item = layout_to_delete.takeAt(0)
                    if sub_item.widget():
                        sub_item.widget().deleteLater()
                layout_to_delete.deleteLater()

        self.variable_value_entries.clear()

        if current_solution_to_display:
            point_coords = []
            # Використовуємо self.variables для гарантованого порядку та набору змінних для підстановки
            # Множники Лагранжа тут не потрібні для підстановки в цільову функцію
            for var_name in sorted(self.variables): # self.variables - це ['x', 'y'], наприклад
                print(f"  var_name: {var_name}")
                if var_name in current_solution_to_display:
                    val_data = current_solution_to_display[var_name]
                    rounded_val = round(float(val_data['float_val']), 3)
                    point_coords.append(f"{var_name}={rounded_val}")      

                    var_entry = QLineEdit()
                    var_entry.setMinimumWidth(100)
                    var_entry.setPlaceholderText(f"{var_name}")
                    var_entry.setText(str(val_data['float_val'])) 

                    self.variable_value_entries[var_name] = var_entry
                    self.substitution_variables_inputs_layout.addWidget(QLabel(", "))
                    self.substitution_variables_inputs_layout.addWidget(var_entry)

            self.solution_point_label.setText(f"<b>Обране рішення:</b> A( {', '.join(point_coords)} )")
            self.final_function_value_entry.clear() # Очищаємо поле результату функції
        else:
            self.solution_point_label.setText("Рішення не обрано або не знайдено.")
            # Очистити поля вводу, якщо немає рішення
            self.final_function_value_entry.clear()


        # Визначник відображається незалежно від обраного рішення (поточна логіка)
        self.determinant_display_label.setText(
            f"<b>Значення визначника матриці Гессе ((Δ &lt; 0)):</b> {self.determinant_value}")


    def display_results(self):
        self._update_display_for_current_selection() # Гарантує оновлення

        # if len(all_solutions) > 1:
        #     # вівести в строку ответы
        #     self.solution_point_label.setText(f"Знайдені рішення у вигляді точки: {all_solutions}")
        # else:
        #     solution_point_text = "<b>Знайдені рішення у вигляді точки:</b> A("
        #     sorted_variables = sorted([var for var in self.variables if var in self.solutions])
        #     point_coords = []
        #     for var in sorted_variables:
        #         point_coords.append(f"{var}={str(self.solutions[var])}")
        #     solution_point_text += ", ".join(point_coords) + ")"
        #     self.solution_point_label.setText(solution_point_text)
            
        # sorted_variables = sorted([var for var in self.variables if var in self.solutions])
        # point_coords = []
        # for var in sorted_variables:
        #     point_coords.append(f"{var}={str(self.solutions[var])}")
        # self.solution_point_label.setText(f"<b>Знайдені рішення у вигляді точки:</b> A( {", ".join(point_coords)} )")

        # self.determinant_display_label.setText(
        #     f"<b>Значення визначника матриці Гессе ((Δ &lt; 0)):</b> {self.determinant_value}")

        # # --- Очищення та заповнення полів вводу для підстановки ---
        # while self.substitution_variables_inputs_layout.count():
        #     item = self.substitution_variables_inputs_layout.takeAt(0)
        #     if item.widget():
        #         item.widget().deleteLater()
        #     elif item.layout():
        #         while item.layout().count():
        #             sub_item = item.layout().takeAt(0)
        #             if sub_item.widget():
        #                 sub_item.widget().deleteLater()
        #         item.layout().deleteLater()
        # self.variable_value_entries.clear()

        # first_variable = True
        # for var in sorted_variables:
        #     if not first_variable:
        #         comma_label = QLabel(", ")
        #         self.substitution_variables_inputs_layout.addWidget(comma_label)

        #     var_entry = QLineEdit()
        #     var_entry.setPlaceholderText(f"{var}")
        #     var_entry.setFixedWidth(60)
        #     self.variable_value_entries[var] = var_entry
        #     self.substitution_variables_inputs_layout.addWidget(var_entry)

        #     first_variable = False

        # self.final_function_value_entry.clear()

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
                "<span style='color: orange;'>Неможливо визначити тип екстремуму за значенням визначника ((Δ &lt; 0) = 0 або невідомий). Потрібен додатковий аналіз.</span>")
        elif correct_extremum_id == 3:
            if user_choice_id == 3:
                self.extremum_feedback_label.setText(
                    "<div style='color: green;'>Вірно! Це сідлова точка (Δ &lt; 0) < 0). </div>")
            else:
                self.extremum_feedback_label.setText(
                    "<span style='color: red;'>Неправильно. При (Δ &lt; 0) < 0 це завжди сідлова точка.</span>")
        elif det > 0:
            if user_choice_id == 1:
                self.extremum_feedback_label.setText(
                    "<span style='color: orange;'>Можливо вірно. Для точного визначення локального максимуму потрібно перевірити $L_{xx} < 0$.</span>")
            elif user_choice_id == 2:
                self.extremum_feedback_label.setText(
                    "<span style='color: orange;'>Можливо вірно. Для точного визначення локального мінімуму потрібно перевірити $L_{xx} > 0$.</span>")
            else:
                self.extremum_feedback_label.setText(
                    "<span style='color: red;'>Неправильно. При (Δ &lt; 0) > 0 це завжди локальний екстремум (min або max), а не сідлова точка.</span>")

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

        print(f"calculated_value: {calculated_value}")
        print(f"entered_final_value: {entered_final_value}")

        if round(float(calculated_value), 3) == round(float(entered_final_value), 3):
            self.function_value_feedback_label.setText(
                f"<span style='color: green;'>Значення цільової функції обчислено правильно: F = {round(float(calculated_value), 3)}!</span>")
        else:
            self.function_value_feedback_label.setText(
                f"<span style='color: red;'>Неправильне значення. Очікується: F = {round(float(calculated_value), 3)}.</span>")

    def go_to_prev_step(self):
        self.switch_step(5)

    def go_to_start(self):
        self.switch_step(0)


    def closeEvent(self, event):
        """Обработчик закрытия виджета"""
        print('Закрытие шага 6...')
        event.accept()
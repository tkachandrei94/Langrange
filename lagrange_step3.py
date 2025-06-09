from PyQt6.QtWidgets import QWidget, QLabel, QVBoxLayout, QPushButton, QLineEdit, QHBoxLayout, QGridLayout, QComboBox
from sympy import symbols, sympify, solve, Eq, Rational
import sympy as sp
import matplotlib.pyplot as plt
import io
from PyQt6.QtGui import QPixmap, QImage
from test_config import test_config_step3
import json 

class LagrangeStep3(QWidget):
    def __init__(self, parent, switch_step_callback):
        super().__init__(parent)
        self.switch_step = switch_step_callback
        self.initial_derivatives = []
        self.current_equations_sympy = [] # Зберігаємо рівняння як sympy об'єкти Eq
        self.var_symbols = []
        self.lambda_syms = []
        self.equation_widgets = {} # Для відображення та вибору рівнянь
        self.solution_entries = {}
        self.feedback_label = None
        self.next_button = None
        self.main_window = parent # Додано для доступу до MainWindow

        layout = QVBoxLayout(self)

        instruction_label = QLabel("<b>Етап 3: Розв'язання системи рівнянь</b><br>"
                                   "Виберіть рівняння, виразіть змінну та підставте в інше рівняння.")
        layout.addWidget(instruction_label)

        self.equations_grid = QGridLayout()
        layout.addLayout(self.equations_grid)

        expression_layout = QHBoxLayout()
        self.express_equation_combo = QComboBox()
        expression_layout.addWidget(QLabel("З рівняння: "))
        expression_layout.addWidget(self.express_equation_combo)
        self.express_variable_combo = QComboBox()
        expression_layout.addWidget(QLabel("виразіть: "))
        expression_layout.addWidget(self.express_variable_combo)
        self.substitution_target_combo = QComboBox()
        expression_layout.addWidget(QLabel("та підставте в рівняння: "))
        expression_layout.addWidget(self.substitution_target_combo)
        self.substitute_button = QPushButton("Підставити")
        self.substitute_button.clicked.connect(self.perform_substitution)
        expression_layout.addWidget(self.substitute_button)
        layout.addLayout(expression_layout)

        solution_label = QLabel("Введіть розв'язки:")
        layout.addWidget(solution_label)
        self.solutions_grid_layout = QGridLayout()
        layout.addLayout(self.solutions_grid_layout)

        check_button = QPushButton("Перевірити розв'язок")
        check_button.clicked.connect(self.check_solution)
        layout.addWidget(check_button)
        self.check_button = check_button

        self.feedback_label = QLabel("")
        layout.addWidget(self.feedback_label)

        navigation_layout = QHBoxLayout()
        prev_button = QPushButton("Назад")
        prev_button.clicked.connect(self.go_to_prev_step)
        navigation_layout.addWidget(prev_button)

        next_button = QPushButton("Далі")
        next_button.setEnabled(True) # Кнопка "Далі" активна за замовчуванням
        next_button.clicked.connect(self.go_to_next_step)
        navigation_layout.addWidget(next_button)

        layout.addLayout(navigation_layout)
        self.next_button = next_button

        self.setLayout(layout)

    def set_derivatives(self, derivatives, var_symbols, lambda_syms):
        self.initial_derivatives = list(derivatives)
        self.current_equations_sympy = [Eq(sympify(eq), 0) for eq in derivatives]
        self.var_symbols = list(var_symbols)
        self.lambda_syms = list(lambda_syms)
        self._display_equations()
        self._setup_solution_fields()
        self._update_equation_choices()

        # symbols_to_solve = self.var_symbols + list(self.lambda_syms)
        # try:
        #     self.precomputed_solutions = solve(self.current_equations_sympy, symbols_to_solve)
        # except Exception as e:
        #     print(f"Ошибка при вычислении решений: {e}")
        #     self.precomputed_solutions = None
    def _display_equations(self):
        # Очищаємо попередні віджети рівнянь
        for i in reversed(range(self.equations_grid.count())):
            widget = self.equations_grid.itemAt(i).widget()
            if widget is not None:
                widget.deleteLater()
        self.equation_widgets = {}

        for i, eq_sympy in enumerate(self.current_equations_sympy):
            eq_latex = f"${sp.latex(eq_sympy)}$" # Обертаємо LaTeX у $...$ для matplotlib

            try:
                # Створюємо фігуру matplotlib без відображення
                fig = plt.figure(figsize=(6, 1), dpi=100)
                fig.text(0.05, 0.5, eq_latex, fontsize=12)
                fig.tight_layout()

                # Зберігаємо фігуру в буфер пам'яті
                buf = io.BytesIO()
                fig.savefig(buf, format='png')
                buf.seek(0)
                plt.close(fig)

                # Завантажуємо зображення з буфера в QImage та QPixmap
                img = QImage.fromData(buf.read())
                pixmap = QPixmap.fromImage(img)

                equation_label = QLabel()
                equation_label.setPixmap(pixmap)
                self.equations_grid.addWidget(equation_label, i, 0)
                self.equation_widgets[i] = equation_label

            except Exception as e:
                equation_label_fallback = QLabel(f"Рівняння {i + 1}: {str(eq_sympy)}")
                self.equations_grid.addWidget(equation_label_fallback, i, 0)
                self.equation_widgets[i] = equation_label_fallback
                print(f"Помилка рендерингу LaTeX (крок 3): {e}")

    def _update_equation_choices(self):
        self.express_equation_combo.clear()
        self.substitution_target_combo.clear()
        for i in range(len(self.current_equations_sympy)):
            self.express_equation_combo.addItem(f"Рівняння {i + 1}")
            self.substitution_target_combo.addItem(f"Рівняння {i + 1}")
        self._update_variable_choices_for_expression()

        # Забороняємо підстановку рівняння в самого себе за замовчуванням
        if self.express_equation_combo.currentIndex() != -1:
            index_to_disable = self.express_equation_combo.currentIndex()
            self.substitution_target_combo.model().item(index_to_disable).setEnabled(False)

        self.express_equation_combo.currentIndexChanged.connect(self._update_variable_choices_for_expression)
        self.express_equation_combo.currentIndexChanged.connect(self._disable_substitution_target)
        self.substitution_target_combo.currentIndexChanged.connect(self._disable_substitution_source)

    def _disable_substitution_target(self, index):
        # for i in range(self.substitution_target_combo.count()):
        #     item = self.substitution_target_combo.model().item(i)
        #     if item is not None:
        #         item.setEnabled(True)
        # item = self.substitution_target_combo.model().item(index)
        # if item is not None:
        #     item.setEnabled(False)
            
        for i in range(self.substitution_target_combo.count()):
            self.substitution_target_combo.model().item(i).setEnabled(True)
        self.substitution_target_combo.model().item(index).setEnabled(False)

    def _disable_substitution_source(self, index):
        for i in range(self.express_equation_combo.count()):
            self.express_equation_combo.model().item(i).setEnabled(True)
        self.express_equation_combo.model().item(index).setEnabled(False)


    def _update_variable_choices_for_expression(self, index=0):
        self.express_variable_combo.clear()
        if index != -1 and index < len(self.current_equations_sympy):
            equation = self.current_equations_sympy[index]
            available_symbols = sorted(equation.free_symbols, key=str)
            self.express_variable_combo.addItems([str(sym) for sym in available_symbols])

    def perform_substitution(self):
        express_eq_index = self.express_equation_combo.currentIndex()
        express_var_str = self.express_variable_combo.currentText()
        target_eq_index = self.substitution_target_combo.currentIndex()

        if express_eq_index == -1 or not express_var_str or target_eq_index == -1 or express_eq_index == target_eq_index:
            self.feedback_label.setText("Будь ласка, виберіть рівняння, змінну для вираження та цільове рівняння.")
            return

        try:
            express_equation = self.current_equations_sympy[express_eq_index]
            variable_to_express = symbols(express_var_str)
            # Виражаємо змінну
            solution = solve(express_equation, variable_to_express)
            if solution:
                expression = solution[0] # Беремо перший розв'язок, якщо їх кілька

                # Виконуємо підстановку
                new_equations = list(self.current_equations_sympy)
                target_equation = new_equations[target_eq_index]
                new_equations[target_eq_index] = target_equation.subs(variable_to_express, expression)
                self.current_equations_sympy = new_equations
                self._display_equations()
                self.feedback_label.setText(f"{express_var_str} виражено з Рівняння {express_eq_index + 1} та підставлено в Рівняння {target_eq_index + 1}.")
            else:
                self.feedback_label.setText(f"Не вдалося виразити {express_var_str} з Рівняння {express_eq_index + 1}.")

        except Exception as e:
            self.feedback_label.setText(f"Помилка під час підстановки: {e}")
            import traceback
            traceback.print_exc()

    def _setup_solution_fields(self):
        # Очищення попередніх полів
        for i in reversed(range(self.solutions_grid_layout.count())):
            widget = self.solutions_grid_layout.itemAt(i).widget()
            if widget is not None:
                widget.deleteLater()
        self.solution_entries = {}

        row = 0
        all_symbols_str = sorted([str(v) for v in self.var_symbols] + [str(l) for l in self.lambda_syms])
        for symbol_str in all_symbols_str:
            label = QLabel(f"{symbol_str} = ")
            entry = QLineEdit()
            entry.setText(test_config_step3[row])

            self.solutions_grid_layout.addWidget(label, row, 0)
            self.solutions_grid_layout.addWidget(entry, row, 1)
            self.solution_entries[symbol_str] = entry
            row += 1

    def check_solution(self):
        entered_solutions = {}
        for symbol_str, entry in self.solution_entries.items():
            entered_solutions[symbol_str] = entry.text().strip()

        symbols_to_solve = self.var_symbols + list(self.lambda_syms)
        all_correct = True
        feedback_text = "Неправильний розв'язок: "
        incorrect_solutions = []

        try:
            solutions = solve(self.current_equations_sympy, symbols_to_solve)

            # solutions = self.precomputed_solutions
            print(f"Знайдені розв'язки: {solutions}") # Для налагодження
            print(f"Введені розв'язки: {entered_solutions}") # Для налагодження
            print(f"Символи для розв'язання: {symbols_to_solve}") # Для налагодження

            if solutions:
                solution_dict = {}
                if isinstance(solutions, dict):
                    solution_dict = solutions
                elif isinstance(solutions, list) and solutions:
                    if isinstance(solutions[0], dict):
                        solution_dict = solutions[0]
                    elif len(solutions[0]) == len(symbols_to_solve):
                        solution_dict = dict(zip(symbols_to_solve, solutions[0]))

                for symbol in symbols_to_solve:
                    symbol_str = str(symbol)
                    expected_solution_sympy = solution_dict.get(symbol)
                    entered_solution_str = entered_solutions.get(symbol_str, "").strip().lower()

                    if expected_solution_sympy is not None:
                        expected_solution_str = str(expected_solution_sympy).lower()
                        try:
                            expected_val_numeric = float(sympify(str(expected_solution_sympy)).evalf())
                            entered_val_numeric = float(sympify(entered_solution_str).evalf())
                            
                            if not sp.Abs(expected_val_numeric - entered_val_numeric) < 1e-6:
                                all_correct = False
                                incorrect_solutions.append(symbol_str)
                        except ValueError:
                            # Если не удалось преобразовать в float (например, одно из значений не числовое или ошибка sympify)
                            # Сравниваем как строки, предварительно обработанные sympify для канонической формы
                            print(f"Ошибка при числовом сравнении для {symbol_str}: {e}. Сравниваем как строки.")
                            expected_str_canon = str(sympify(str(expected_solution_sympy))).lower().replace(" ", "")
                            entered_str_canon = str(sympify(entered_solution_str)).lower().replace(" ", "")
                            if expected_str_canon != entered_str_canon:
                                all_correct = False
                                incorrect_solutions.append(symbol_str)
                    else:
                        all_correct = False
                        incorrect_solutions.append(symbol_str)

            else:
                if entered_solutions:
                    all_correct = False
                    incorrect_solutions.extend(entered_solutions.keys())
                else:
                    self.feedback_label.setText("Система рівнянь не має розв'язку.")
                    return

        except Exception as e:
            all_correct = False
            feedback_text = f"Помилка при перевірці розв'язку: {e}"
            print(f"Помилка при перевірці розв'язку: {e}")
            
            import traceback
            traceback.print_exc()

        if all_correct:
            self.feedback_label.setText("Розв'язок знайдено правильно!")
            # Кнопка "Далі" вже активна
        else:
            self.feedback_label.setText(feedback_text + ", ".join(incorrect_solutions))
            # За бажанням, можна тут блокувати кнопку "Далі":
            # self.next_button.setEnabled(False)

    def go_to_prev_step(self):
        self.switch_step(2)

    def go_to_next_step(self):
        print("Викликаю switch_step з 3-го етапу...")
        # Отримуємо введені розв'язки
        entered_solutions_by_user = {
            var: entry.text().strip() for var, entry in self.solution_entries.items()
        }

        # Вычисляем все возможные решения системы (если их несколько)
        symbols_to_solve = self.var_symbols + list(self.lambda_syms)
        # Используем dict=True для получения словарей
        raw_sympy_solutions = solve(self.current_equations_sympy, symbols_to_solve, dict=True)
        
        processed_solutions_list_basic_types = [] # Переименовано для ясности
        if raw_sympy_solutions:
            solution_list_of_sympy_dicts = []
            if isinstance(raw_sympy_solutions, dict): # Если solve вернул один словарь (одно решение)
                solution_list_of_sympy_dicts = [raw_sympy_solutions]
            elif isinstance(raw_sympy_solutions, list): # Если solve вернул список словарей
                solution_list_of_sympy_dicts = raw_sympy_solutions
            
            for sol_sympy_dict in solution_list_of_sympy_dicts:
                current_solution_basic_types_dict = {}
                for var_symbol, value_sympy in sol_sympy_dict.items():
                    current_solution_basic_types_dict[str(var_symbol)] = {
                        'fraction_str': str(value_sympy) ,
                        'float_val':  float(value_sympy.evalf())
                    }
                if current_solution_basic_types_dict: # Добавляем, только если словарь не пустой
                    processed_solutions_list_basic_types.append(current_solution_basic_types_dict)

        print("Все найденные решения (только базовые типы, JSON-like формат):")
        if not processed_solutions_list_basic_types:
            print("[]") 
        else:
            formatted_json_string = json.dumps(processed_solutions_list_basic_types, indent=2, ensure_ascii=False)
            print(formatted_json_string)
        
        self.main_window.solution_step3 = entered_solutions_by_user 
        self.main_window.all_solutions_step3 = processed_solutions_list_basic_types # Сохраняем список с базовыми типами

        self.switch_step(4)
        print("Повернення з switch_step у 3-му етапі.")
    
    def closeEvent(self, event):
        """Обработчик закрытия виджета"""
        print('Закрытие шага 3...')
        # Очищаем ресурсы
        plt.close('all')  # Закрываем все фигуры matplotlib
        event.accept()
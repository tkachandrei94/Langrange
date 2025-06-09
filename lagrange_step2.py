from PyQt6.QtWidgets import QWidget, QLabel, QVBoxLayout, QPushButton, QLineEdit, QHBoxLayout, QGridLayout
from sympy import symbols, sympify, diff, simplify
from PyQt6.QtCore import Qt
import sympy as sp
from test_config import test_config_step2

class LagrangeStep2(QWidget):
    def __init__(self, parent, switch_step_callback):
        super().__init__(parent)
        self.switch_step = switch_step_callback
        self.function_str = ""
        self.constraint_strs = []
        self.variables = []
        self.derivative_entries = {} # Словник для зберігання полів введення похідних
        self.calculated_derivatives = {}
        self.var_symbols_step2 = []
        self.lambda_syms_step2 = []
        self.lambda_symbols_internal = []
        self.feedback_label = None

        layout = QVBoxLayout(self)
        self.layout = layout

        instruction_label = QLabel("<b>Етап 2: Знаходження частинних похідних</b><br>"
                                   "Будь ласка, знайдіть та введіть частинні похідні функції Лагранжа:")
        layout.addWidget(instruction_label)

        self.lagrange_function_label = QLabel("Функція Лагранжа: ")
        layout.addWidget(self.lagrange_function_label)

        self.derivatives_grid_layout = QGridLayout()
        layout.addLayout(self.derivatives_grid_layout)

        self.check_button = QPushButton("Перевірити")
        self.check_button.clicked.connect(self.check_derivatives)
        layout.addWidget(self.check_button)

        self.feedback_label = QLabel("")
        layout.addWidget(self.feedback_label)

        navigation_layout = QHBoxLayout()
        self.prev_button = QPushButton("Назад")
        self.prev_button.clicked.connect(self.go_to_prev_step)
        navigation_layout.addWidget(self.prev_button)

        self.next_button = QPushButton("Далі")
        self.next_button.setEnabled(False)
        self.next_button.clicked.connect(self.go_to_next_step)
        navigation_layout.addWidget(self.next_button)

        layout.addLayout(navigation_layout)

        self.setLayout(layout)

    def set_function_constraints(self, function_str, constraint_strs, variables):
        self.function_str = function_str
        self.constraint_strs = constraint_strs
        self.variables = variables
        num_constraints = len(constraint_strs)
        self.lambda_symbols_internal = symbols([f'λ{i+1}' for i in range(num_constraints)]) # Використовуємо грецьку лямбду
        all_symbols = symbols(self.variables + [str(s) for s in self.lambda_symbols_internal])
        var_symbols = [s for s in all_symbols if str(s) in self.variables]
        lambda_syms = [s for s in all_symbols if s in self.lambda_symbols_internal]

        self.var_symbols_step2 = list(var_symbols)
        self.lambda_syms_step2 = list(self.lambda_symbols_internal)

        function_str_internal = function_str
        constraint_strs_internal = list(constraint_strs)

        try:
            symbol_map = {str(s): s for s in all_symbols}
            f = sympify(function_str_internal, locals=symbol_map)
            lagrange_expr = f
            for i, g_str in enumerate(constraint_strs_internal):
                g_minus_c = sympify(f"0 - ({g_str})", locals=symbol_map)
                lagrange_expr += self.lambda_symbols_internal[i] * g_minus_c
            self.lagrange_function_label.setText(f"Функція Лагранжа: {str(lagrange_expr)}")
            self.setup_derivative_fields(var_symbols, self.lambda_symbols_internal)

            # Оновлюємо примітку, роблячи символ лямбда частиною тексту
            note_label_text = "<br><b>Примітка:</b> Для введення символів лямбда (λ1, λ2, ...) використовуйте <b>λ1</b>, <b>λ2</b> і так далі."
            note_label = QLabel(note_label_text)
            note_label.setTextInteractionFlags(Qt.TextInteractionFlag.TextSelectableByMouse) # Додаємо можливість виділення тексту
            self.layout.addWidget(note_label)

        except Exception as e:
            self.lagrange_function_label.setText(f"Помилка при формуванні функції Лагранжа: {e}")

    def setup_derivative_fields(self, var_symbols, lambda_syms):
        # Очищення попередніх полів
        for i in reversed(range(self.derivatives_grid_layout.count())):
            widget = self.derivatives_grid_layout.itemAt(i).widget()
            if widget is not None:
                widget.deleteLater()
        self.derivative_entries = {}

        row = 0
        print("var_symbols:", var_symbols)
        print("lambda_syms:", lambda_syms)
        for var in var_symbols:
            label = QLabel(f"dL/d{var} = ")
            entry = QLineEdit()
            entry.setText(test_config_step2[row] if test_config_step2 else "")

            self.derivatives_grid_layout.addWidget(label, row, 0)
            self.derivatives_grid_layout.addWidget(entry, row, 1)
            self.derivative_entries[str(var)] = entry
            row += 1

        for lam in lambda_syms:
            label = QLabel(f"dL/d{lam} = ") # Використовуємо безпосередньо символ λ
            entry = QLineEdit()
            entry.setText(test_config_step2[row] if test_config_step2 else "")
            self.derivatives_grid_layout.addWidget(label, row, 0)
            self.derivatives_grid_layout.addWidget(entry, row, 1)
            self.derivative_entries[str(lam)] = entry
            row += 1

        # Видаляємо стару примітку, якщо вона була
        for i in reversed(range(self.derivatives_grid_layout.rowCount())):
            item = self.derivatives_grid_layout.itemAtPosition(i, 0)
            if item and isinstance(item.widget(), QLabel) and "Для введення символів лямбда" in item.widget().text():
                item.widget().deleteLater()
                self.derivatives_grid_layout.removeItem(item)
                break


    def check_derivatives(self):
        num_constraints = len(self.constraint_strs)
        self.lambda_symbols_internal = symbols([f'λ{i+1}' for i in range(num_constraints)]) # Перестворюємо символи
        all_symbols = symbols(self.variables + [str(s) for s in self.lambda_symbols_internal])
        var_symbols = [s for s in all_symbols if str(s) in self.variables]
        lambda_syms = [s for s in all_symbols if s in self.lambda_symbols_internal]

        try:
            symbol_map = {str(s): s for s in all_symbols}
            f = sympify(self.function_str, locals=symbol_map)
            lagrange_expr = f
            for i, g_str in enumerate(self.constraint_strs):
                g_minus_c = sympify(f"0 - ({g_str})", locals=symbol_map)
                lagrange_expr += self.lambda_symbols_internal[i] * g_minus_c

            expected_derivatives = {}
            for var in var_symbols:
                expected_derivatives[var] = diff(lagrange_expr, var)
            for lam in lambda_syms:
                expected_derivatives[lam] = diff(lagrange_expr, lam)

            all_correct = True
            feedback_text = "Неправильно введено похідні: "
            incorrect_derivatives = []

            for symbol_str, entry in self.derivative_entries.items():
                entered_derivative_str = entry.text()
                expected_symbol = symbols(symbol_str)
                expected_derivative = expected_derivatives.get(expected_symbol, "")

                try:
                    # Преобразуем оба выражения в sympy и упрощаем
                    entered_expr = simplify(sympify(entered_derivative_str))
                    expected_expr = simplify(sympify(str(expected_derivative)))
                    check_result = entered_expr.equals(expected_expr)
                except Exception as e:
                    print(f"SymPy parse error: {e}")
                    check_result = False

                print("entered:", entered_derivative_str, "| expected:", expected_derivative, "| check_result:", check_result)

                if not check_result:
                    all_correct = False
                    incorrect_derivatives.append(symbol_str)

            if all_correct:
                self.feedback_label.setText("Усі похідні введено правильно!")
                self.next_button.setEnabled(True)
                self.calculated_derivatives = {str(k): str(v) for k, v in expected_derivatives.items()}
            else:
                self.feedback_label.setText(feedback_text + ", ".join(incorrect_derivatives))
                print(f"Помилка при перевірці похідних: {feedback_text + ', '.join(incorrect_derivatives)}")

        except Exception as e:
            self.feedback_label.setText(f"Помилка при обчисленні похідних: {e}")

    def get_derivatives_data(self):
        derivatives_list = [self.calculated_derivatives.get(str(var), '') for var in self.var_symbols_step2] + \
                           [self.calculated_derivatives.get(str(lam), '') for lam in self.lambda_syms_step2]
        return derivatives_list, self.var_symbols_step2, self.lambda_syms_step2

    def get_derivatives_expressions(self):
        derivatives_expressions = {}
        num_constraints = len(self.constraint_strs)
        lambda_symbols_internal = symbols([f'λ{i+1}' for i in range(num_constraints)])
        all_symbols = symbols(self.variables + [str(s) for s in lambda_symbols_internal])
        var_symbols = [s for s in all_symbols if str(s) in self.variables]
        lambda_syms = [s for s in all_symbols if s in lambda_symbols_internal]

        try:
            symbol_map = {str(s): s for s in all_symbols}
            f = sympify(self.function_str, locals=symbol_map)
            lagrange_expr = f
            for i, g_str in enumerate(self.constraint_strs):
                g_minus_c = sympify(f"0 - ({g_str})", locals=symbol_map)
                lagrange_expr += lambda_symbols_internal[i] * g_minus_c

            for var in var_symbols:
                derivatives_expressions[str(var)] = str(diff(lagrange_expr, var))
            for lam in lambda_syms:
                derivatives_expressions[str(lam)] = str(diff(lagrange_expr, lam))

            return derivatives_expressions
        except Exception as e:
            print(f"Помилка при отриманні виразів похідних: {e}")
            return {}

    def go_to_prev_step(self):
        self.switch_step(1)

    def go_to_next_step(self):
        self.switch_step(3)

    def closeEvent(self, event):
        """Обработчик закрытия виджета"""
        print('Закрытие шага 2...')
        # Очищаем ресурсы
        event.accept()
import sys
from PyQt6.QtWidgets import QApplication, QMainWindow, QStackedWidget, QLineEdit, QWidget
from PyQt6.QtCore import Qt, QTimer
import sympy as sp
from sympy import symbols, sympify, diff
import signal
import os



def signal_handler(sig, frame):
    """Обработчик сигналов для корректного завершения приложения"""
    print('Получен сигнал завершения...')
    # Получаем экземпляр приложения
    app = QApplication.instance()
    if app:
        # Закрываем все окна
        for window in app.topLevelWidgets():
            window.close()
        # Завершаем приложение
        app.quit()
    sys.exit(0)

signal.signal(signal.SIGINT, signal_handler)  
signal.signal(signal.SIGTERM, signal_handler) 

from lagrange_step0 import LagrangeStep0
from lagrange_step1 import LagrangeStep1
from lagrange_step2 import LagrangeStep2
from lagrange_step3 import LagrangeStep3
from lagrange_step4 import LagrangeStep4
from lagrange_step5 import LagrangeStep5
from lagrange_step6 import LagrangeStep6


class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()

        self.setWindowTitle("Розв'язання методом множників Лагранжа")
        self.setGeometry(100, 100, 800, 600)

        self.stacked_widget = QStackedWidget()
        self.setCentralWidget(self.stacked_widget)

        self.step0_widget = LagrangeStep0(self, self.switch_step)
        self.step1_widget = LagrangeStep1(self, self.switch_step)
        self.step2_widget = LagrangeStep2(self, self.switch_step)
        self.step3_widget = LagrangeStep3(self, self.switch_step)
        self.step4_widget = LagrangeStep4(self, self.switch_step)
        self.step5_widget = LagrangeStep5(self, self.switch_step)
        self.step6_widget = LagrangeStep6(self, self.switch_step)

        self.stacked_widget.addWidget(self.step0_widget)
        self.stacked_widget.addWidget(self.step1_widget)
        self.stacked_widget.addWidget(self.step2_widget)
        self.stacked_widget.addWidget(self.step3_widget)
        self.stacked_widget.addWidget(self.step4_widget)
        self.stacked_widget.addWidget(self.step5_widget)
        self.stacked_widget.addWidget(self.step6_widget)

        self.current_step = 0
        self.function_str = None
        self.constraint_strs = None
        self.variables = None
        self.lambda_symbols_step3 = None
        self.solution_step3 = None  # Цей атрибут оновлюється з 3-го етапу і має бути числовим
        self.all_solutions_step3 = None  # или []
        self.solution_step3_solutionslagrange_function_str_step2 = None
        self.second_derivatives_step4 = None
        self.determinant_step5 = None
        self.extreme_point_step5 = None  # Додаємо для зберігання extreme_point з 5-го етапу
        
        self.stacked_widget.setCurrentIndex(self.current_step)

    def calculate_second_derivatives(self, lagrange_str, variables_with_lambda):
        # Спочатку перетворимо variables_with_lambda у символи sympy
        sym_vars = {v: symbols(v) for v in variables_with_lambda}

        # Перевіряємо, чи всі символи в variables_with_lambda є дійсними символами для sympy
        # Це допомагає уникнути проблем, якщо десь 'lambda1' було передано як 'λ₁'
        # і sympy не може його розпізнати як простий символ.
        # Для простоти, давайте використовувати `symbols(variables_with_lambda)` напряму,
        # якщо `variables_with_lambda` це список рядків

        # Перетворюємо unicode-символи лямбди на звичайні для sympy, якщо необхідно
        temp_vars_with_lambda_for_sympy = [v.replace('λ', 'lambda') for v in variables_with_lambda]

        # Створюємо словник символів для sympify
        symbol_map_for_sympify = {s_str: symbols(s_str) for s_str in temp_vars_with_lambda_for_sympy}

        # Оновлюємо sym_vars для використання в диференціюванні
        # Тут ми створюємо символи безпосередньо з variables_with_lambda,
        # але для функціональності diff, ми використовуємо `symbol_map_for_sympify`
        sym_vars_for_diff = {v: symbols(v.replace('λ', 'lambda')) for v in variables_with_lambda}

        lagrange_expr = sympify(lagrange_str, locals=symbol_map_for_sympify)
        second_derivatives = {}
        for var1_str in variables_with_lambda:
            for var2_str in variables_with_lambda:
                # Перетворюємо назви змінних на sympy-символи, які використовуються у виразі Лагранжа
                sym_var1 = sym_vars_for_diff[var1_str]
                sym_var2 = sym_vars_for_diff[var2_str]

                diff_expr = diff(lagrange_expr, sym_var1, sym_var2)
                second_derivatives[(var1_str, var2_str)] = str(diff_expr)
        print(f"Обчислені другі похідні: {second_derivatives}")
        return second_derivatives

    def switch_step(self, next_step, num_variables=2, num_constraints=1, function_str=None, constraint_strs=None,
                    variables=None, second_derivatives=None, determinant=None, extreme_point=None, all_solutions_step3=None):
        
        print(f"switch_step_extreme_point : {extreme_point}")
        print(
            f"Викликано switch_step з next_step = {next_step}, num_variables = {num_variables}, num_constraints = {num_constraints}, function_str={function_str}, constraint_strs={constraint_strs}, variables={variables}, second_derivatives={second_derivatives}, determinant={determinant}, extreme_point={extreme_point}")
        self.current_step = next_step
        print(f"Поточний крок встановлено на {self.current_step} (перед обробкою)")

        # Оновлюємо атрибути MainWindow, якщо дані передаються
        if function_str is not None:
            self.function_str = function_str
        if constraint_strs is not None:
            self.constraint_strs = constraint_strs
        if variables is not None:
            self.variables = variables
        if second_derivatives is not None:
            self.second_derivatives_step4 = second_derivatives
        if determinant is not None:
            self.determinant_step5 = determinant
        if extreme_point is not None:
            self.extreme_point_step5 = extreme_point

        if self.current_step == 1:
            print("\n--------------------------------")
            print("Перехід до 1-го етапу...")
            
            self.variables = ['x', 'y', 'z', 'q', 'w'][:num_variables]
            self.step1_widget.setup_input_fields(self.variables, num_constraints)

        elif self.current_step == 2:
            print("\n--------------------------------")
            print("Перехід до 2-го етапу...")
            
            if self.function_str is not None and self.constraint_strs is not None and self.variables is not None:
                self.step2_widget.set_function_constraints(self.function_str, self.constraint_strs, self.variables)

                num_constraints_step2 = len(self.constraint_strs)
                lambda_symbols_step2 = [sp.Symbol('λ₁') if i == 0 else sp.Symbol(f'λ{i + 1}') for i in
                                        range(num_constraints_step2)]

                # Створюємо словник символів для sympify, замінюючи 'λ' на 'lambda' для сумісності з sympy
                all_symbols_str = self.variables + [str(s).replace('λ', 'lambda') for s in lambda_symbols_step2]
                symbol_map = {s_str: symbols(s_str) for s_str in all_symbols_str}

                f = sympify(self.function_str, locals=symbol_map)
                lagrange_expr = f
                for i, g_str in enumerate(self.constraint_strs):
                    # Важливо: використовуємо символи лямбда з 'lambda' у назві для обчислень
                    lambda_sym_for_calc = symbols(str(lambda_symbols_step2[i]).replace('λ', 'lambda'))
                    g_expr = sympify(g_str, locals=symbol_map)
                    lagrange_expr += lambda_sym_for_calc * (0 - g_expr)
                self.lagrange_function_str_step2 = str(lagrange_expr)

            else:
                print("Помилка: Не отримано необхідні дані для другого етапу.")
                return

        elif self.current_step == 3:
            print("\n--------------------------------")
            print("Перехід до 3-го етапу...")
            
            derivatives, var_symbols, lambda_syms = self.step2_widget.get_derivatives_data()
            self.step3_widget.set_derivatives(derivatives, var_symbols, lambda_syms)
            self.lambda_symbols_step3 = lambda_syms
            # solution_step3 оновлюється безпосередньо з 3-го етапу через self.main_window.solution_step3

        elif self.current_step == 4:
            print("\n--------------------------------")
            print("Перехід до 4-го етапу...")
            
            QTimer.singleShot(0, self._initialize_step4)

        elif self.current_step == 5:
            print("\n--------------------------------")
            print("Перехід до 5-го етапу...")
            if self.second_derivatives_step4:
                # Передаємо extreme_point_step3 (solution_step3) на 5-й етап
                # Перевіряємо, чи self.solution_step3 дійсно містить числові значення,
                # і якщо ні, то намагаємося перетворити їх.
                processed_solution_step3 = {}
                if self.solution_step3:
                    for k, v in self.solution_step3.items():
                        try:
                            # Спроба перетворити на float, якщо це можливо
                            processed_solution_step3[k] = float(sympify(str(v)))
                        except (ValueError, TypeError, sp.SympifyError):
                            # Якщо не число, залишаємо як є (може бути символьний вираз, який sympy обробить)
                            processed_solution_step3[k] = v

                self.step5_widget.set_second_derivatives_calculated(
                    self.second_derivatives_step4,
                    self.variables,
                    extreme_point=processed_solution_step3  # Передаємо оброблену точку
                )
            else:
                print("Помилка: Обчислені другі похідні не отримано для 5-го етапу.")

        elif self.current_step == 6:
            print("\n--------------------------------")
            print("Перехід до 6-го етапу...")
            print(f"self.determinant_step5 (перед передачею): {self.determinant_step5}")
            print(
                f"self.extreme_point_step5 (перед передачею): {self.extreme_point_step5}")  # Використовуємо extreme_point_step5
            print(f"self.function_str (перед передачею): {self.function_str}")
            print(f"self.variables (перед передачею): {self.variables}")
            print(f"self.solution_step3 (перед передачею): {self.solution_step3}")

            if (self.determinant_step5 is not None and
                    self.extreme_point_step5 and  # Перевіряємо наявність extreme_point_step5
                    self.function_str and
                    self.variables):

                self.step6_widget.set_data(
                    self.determinant_step5,
                    self.extreme_point_step5,  # Передаємо extreme_point_step5 (solution_step3)
                    self.function_str,
                    self.variables
                )
            else:
                print("Помилка: Недостатньо даних для 6-го етапу.")

        self.stacked_widget.setCurrentIndex(self.current_step)
        print(f"Поточний крок встановлено на {self.current_step} (після обробки)")

    def _initialize_step4(self):
        print("Викликано _initialize_step4")
        if self.solution_step3 is None:
            # Отримуємо розв'язки з 3-го етапу
            self.solution_step3 = {}
            # Змінні з 3-го етапу можуть включати 'x', 'y', 'λ1' тощо
            all_symbols_step3_raw = self.step3_widget.var_symbols + self.step3_widget.lambda_syms

            for sym_obj in all_symbols_step3_raw:
                sym_str = str(sym_obj)  # Отримуємо строкове представлення символу
                # Якщо символ - це лямбда, то QLineEdit може використовувати 'λ1', а не 'lambda1'
                # Потрібно узгодити ключі
                if sym_str.startswith('λ'):
                    # Замінюємо 'λ' на 'lambda' для внутрішнього використання,
                    # щоб відповідати ключам, які sympy може згенерувати
                    key_for_entry = sym_str  # Це ключ, що використовується в solution_entries
                else:
                    key_for_entry = sym_str

                # Отримуємо текст з відповідного QLineEdit
                text_input = self.step3_widget.solution_entries.get(key_for_entry, QLineEdit()).text().strip()

                try:
                    # Симпліфікуємо та перетворюємо на float
                    self.solution_step3[sym_str] = float(sympify(text_input))
                except (ValueError, TypeError, sp.SympifyError):
                    # Якщо не вдалося перетворити на число (наприклад, порожній рядок або нечисловий вираз),
                    # зберігаємо як рядок. `lagrange_step5` буде обробляти це.
                    self.solution_step3[sym_str] = text_input

        # Створюємо список змінних, включаючи лямбди, для обчислення похідних
        # Важливо: для calculate_second_derivatives ми хочемо, щоб назви були такі,
        # які sympy може легко розпізнати (наприклад, 'x', 'y', 'lambda1').
        # Якщо в self.lambda_symbols_step3 є 'λ₁', то його потрібно перетворити на 'lambda1'.
        lambda_strs_for_calc = [str(s).replace('λ', 'lambda') for s in self.lambda_symbols_step3]
        variables_with_lambda_for_calc = self.variables + lambda_strs_for_calc

        # Перевіряємо, чи self.lagrange_function_str_step2 вже існує, якщо ні, створюємо його.
        # Це допомагає уникнути помилок, якщо користувач переходить між етапами не послідовно
        if not self.lagrange_function_str_step2:
            num_constraints_step2 = len(self.constraint_strs)
            lambda_symbols_step2_for_lagrange = [sp.Symbol(f'lambda{i + 1}') for i in range(num_constraints_step2)]

            # Створюємо словник символів для sympify
            all_symbols_str = self.variables + [str(s) for s in lambda_symbols_step2_for_lagrange]
            symbol_map = {s_str: symbols(s_str) for s_str in all_symbols_str}

            f = sympify(self.function_str, locals=symbol_map)
            lagrange_expr = f
            for i, g_str in enumerate(self.constraint_strs):
                lambda_sym_for_calc = lambda_symbols_step2_for_lagrange[i]
                g_expr = sympify(g_str, locals=symbol_map)
                lagrange_expr += lambda_sym_for_calc * (0 - g_expr)
            self.lagrange_function_str_step2 = str(lagrange_expr)

        second_derivatives = self.calculate_second_derivatives(self.lagrange_function_str_step2,
                                                               variables_with_lambda_for_calc)
        self.second_derivatives_step4 = second_derivatives

        # Перетворюємо ключі в solution_step3, щоб вони відповідали `variables_with_lambda` з `calculate_second_derivatives`,
        # якщо використовувались `λ` символи
        evaluated_solution_for_step4 = {}
        for k, v in self.solution_step3.items():
            new_k = k.replace('λ', 'lambda')
            evaluated_solution_for_step4[new_k] = v

        first_derivatives = self.step2_widget.get_derivatives_expressions()

        first_derivatives_unicode = {}
        for key, value in first_derivatives.items():
            new_key = key
            for i in range(1, 6):
                new_key = new_key.replace(f'lambda{i}', f'λ{i}')
            first_derivatives_unicode[new_key] = value

        print(
            f"Дані, що передаються на 4-й етап: evaluated_solution = {self.solution_step3}, lagrange_function_str_step2 = {self.lagrange_function_str_step2}, variables = {self.variables}, lambda_strs_step4 = {[str(s) for s in self.lambda_symbols_step3]}, second_derivatives = {second_derivatives}, variables_with_lambda = {variables_with_lambda_for_calc}, first_derivatives = {first_derivatives_unicode}")
        self.step4_widget.set_data(
            self.solution_step3,  # Передаємо оригінальний solution_step3, який може містити λ
            second_derivatives=second_derivatives,
            variables=self.variables,
            first_derivatives=first_derivatives_unicode
        )
        self.step4_widget.set_expected_second_derivatives(second_derivatives)
    
    def closeEvent(self, event):
        """Обработчик закрытия окна"""
        print('Закрытие приложения...')
        # Закрываем все дочерние виджеты
        for widget in self.findChildren(QWidget):
            widget.close()
        # Завершаем приложение
        QApplication.instance().quit()
        # Принимаем событие закрытия
        event.accept()

if __name__ == '__main__':
    app = QApplication(sys.argv)
    window = MainWindow()
    window.show()
    sys.exit(app.exec())
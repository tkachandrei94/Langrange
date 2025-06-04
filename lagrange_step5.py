from PyQt6.QtWidgets import QWidget, QLabel, QVBoxLayout, QPushButton, QLineEdit, QHBoxLayout
import matplotlib.pyplot as plt
from PyQt6.QtGui import QPixmap, QImage
import io
import numpy as np
from sympy import symbols, sympify  # Додаємо імпорти для роботи з символьними виразами
from test_config import test_config_step5

class LagrangeStep5(QWidget):
    def __init__(self, parent=None, switch_step_callback=None):
        super().__init__(parent)
        self.switch_step = switch_step_callback
        self.calculated_second_derivatives = {}
        self.variables = []
        self.extreme_point = {}  # Додаємо атрибут для зберігання екстремальної точки
        self.determinant_value_checked = None  # Додаємо атрибут для збереження перевіреного визначника
        layout = QVBoxLayout()

        instruction_label = QLabel("<b>Етап 5: Аналіз матриці Гессе</b><br>"
                                   "Перегляньте матрицю Гессе та обчисліть її визначник.")
        layout.addWidget(instruction_label)

        # Додаємо QLabel для виводу екстремальної точки
        self.extreme_point_label = QLabel("Знайдена екстремальна точка:")
        layout.addWidget(self.extreme_point_label)

        self.hessian_matrix_display_layout = QVBoxLayout()  # Новий макет для відображення матриці
        layout.addLayout(self.hessian_matrix_display_layout)

        # Ці елементи мають бути додані лише один раз у конструкторі
        determinant_label = QLabel("Визначник матриці Гессе (Δ = (∂²L/∂x²)(∂²L/∂y²) - (∂²L/∂x∂y)(∂²L/∂y∂x)):")
        layout.addWidget(determinant_label)  # Додаємо до основного макету

        self.determinant_entry = QLineEdit()
        self.determinant_entry.setText(str(test_config_step5[0]))
        
        layout.addWidget(self.determinant_entry)  # Додаємо до основного макету

        check_button = QPushButton("Перевірити")
        check_button.clicked.connect(self.check_determinant)
        layout.addWidget(check_button)

        self.result_label = QLabel("")
        layout.addWidget(self.result_label)

        navigation_layout = QHBoxLayout()
        prev_button = QPushButton("Назад")
        prev_button.clicked.connect(self.go_to_prev_step)
        navigation_layout.addWidget(prev_button)

        self.next_button = QPushButton("Далі")
        self.next_button.setEnabled(False)  # Кнопка "Далі" буде активована після перевірки
        self.next_button.clicked.connect(self.go_to_next_step)
        navigation_layout.addWidget(self.next_button)

        layout.addLayout(navigation_layout)
        self.setLayout(layout)

    def set_second_derivatives_calculated(self, calculated_second_derivatives, variables, extreme_point=None):
        self.calculated_second_derivatives = calculated_second_derivatives
        self.variables = variables
        if extreme_point:
            # Перетворюємо значення extreme_point в числові типи
            processed_point = {}
            for k, v in extreme_point.items():
                try:
                    processed_point[k] = float(sympify(str(v)))  # Спроба перетворити на float через sympify
                except (ValueError, TypeError, AttributeError):
                    # Якщо не вдалося перетворити на float (наприклад, це рядок 'x' або недійсний вираз),
                    # залишаємо його як є.
                    processed_point[k] = v
            self.extreme_point = processed_point
            self.extreme_point_label.setText(
                f"Знайдена екстремальна точка: {self.format_extreme_point(self.extreme_point)}")
        else:
            self.extreme_point = {}
            self.extreme_point_label.setText("Знайдена екстремальна точка: Не визначено")
        self._display_hessian_matrix()

    def format_extreme_point(self, point):
        # Форматує словник точки для зручного виводу
        formatted_parts = []
        # Спочатку обробляємо основні змінні (x, y, z...)
        for var in self.variables:
            if var in point:
                # Округляємо числові значення до 2 знаків після коми
                val_str = f"{point[var]:.2f}" if isinstance(point[var], (int, float)) else str(point[var])
                formatted_parts.append(f"{var}={val_str}")

        # Потім обробляємо лямбда-змінні (λ1, λ2...)
        lambda_parts = []
        for k, v in point.items():
            if k.startswith('λ') or k.startswith('lambda'):
                # Округляємо числові значення до 2 знаків після коми
                val_str = f"{v:.2f}" if isinstance(v, (int, float)) else str(v)
                # Перетворюємо 'lambda1' назад на 'λ1' для відображення
                display_key = k.replace('lambda', 'λ')
                lambda_parts.append(f"{display_key}={val_str}")

        # Об'єднуємо обидві частини
        all_parts = []
        if formatted_parts:
            all_parts.append(", ".join(formatted_parts))
        if lambda_parts:
            all_parts.append(", ".join(lambda_parts))

        if all_parts:
            return f"({'; '.join(all_parts)})"
        return "Не визначено"

    def _display_hessian_matrix(self):
        # Очищаємо попередній вміст макету для відображення матриці
        for i in reversed(range(self.hessian_matrix_display_layout.count())):
            item = self.hessian_matrix_display_layout.itemAt(i)
            if item.widget():
                item.widget().deleteLater()
            elif item.layout():
                self._clear_layout(item.layout())
                item.layout().deleteLater()

        if not self.calculated_second_derivatives or not self.variables:
            label = QLabel("Дані для матриці Гессе не отримано.")
            self.hessian_matrix_display_layout.addWidget(label)
            return

        # Створюємо символи для підстановки
        sym_vars = {v: symbols(v) for v in self.variables}
        # Додаємо лямбда символи, якщо вони є в extreme_point (з можливістю λ або lambda)
        for k in self.extreme_point.keys():
            # Намагаємося створити символ, використовуючи назву, яка очікується в sympy
            sym_name = k.replace('λ', 'lambda')  # Заміна 'λ' на 'lambda' для sympy
            sym_vars[k] = symbols(sym_name)  # Зберігаємо в sym_vars з оригінальним ключем (λ1)
            # Якщо вираз, що приходить від calculate_second_derivatives, використовує 'lambda1'
            # то `sympify` в `evaluate_expression_for_display` розпізнає його.

        # Функція для підстановки значень та обчислення
        def evaluate_expression_for_display(expr_str, point, all_sym_vars):
            try:
                # Перетворюємо рядок на символьний вираз sympy.
                expr = sympify(str(expr_str))

                if isinstance(expr, (int, float)):
                    return expr  # Якщо це вже число, повертаємо його
                else:  # Якщо це символьний вираз
                    subs_dict = {}
                    for var_name, var_sym in all_sym_vars.items():
                        # Перевіряємо, чи є чисельне значення для цього символу в точці
                        if var_name in point and isinstance(point[var_name], (int, float)):
                            # Використовуємо символ, який sympy розпізнає
                            subs_dict[all_sym_vars[var_name]] = point[var_name]

                    # Перевіряємо, чи всі символи у виразі мають відповідні значення у point
                    # Якщо ні, то повертаємо вираз як є (рядок)
                    # Або якщо після підстановки все ще залишилися вільні символи, повертаємо їх

                    # Спочатку підставляємо, що можемо
                    temp_expr = expr.subs(subs_dict)

                    # Перевіряємо, чи після підстановки вираз став числовим
                    if isinstance(temp_expr, (int, float)):
                        return temp_expr
                    elif temp_expr.is_Number:  # Якщо це число sympy
                        return float(temp_expr)
                    elif not temp_expr.free_symbols:  # Якщо всі символи зникли, але результат не число (наприклад, True/False)
                        return str(temp_expr)  # Повертаємо строкове представлення
                    else:  # Якщо після підстановки залишилися символи
                        return str(temp_expr)  # Повертаємо вираз як рядок з оновленими символами
            except Exception as e:
                print(f"Помилка в evaluate_expression_for_display для '{expr_str}': {e}")
                return str(expr_str)  # Повертаємо початковий рядок у випадку помилки

        if len(self.variables) == 2:
            var1, var2 = self.variables[0], self.variables[1]

            # Отримуємо значення похідних
            d2L_dx2_expr = self.calculated_second_derivatives.get((var1, var1), '0')
            d2L_dy2_expr = self.calculated_second_derivatives.get((var2, var2), '0')
            d2L_dxdy_expr = self.calculated_second_derivatives.get((var1, var2), '0')
            d2L_dydx_expr = self.calculated_second_derivatives.get((var2, var1), '0')

            # Обчислюємо числові значення для відображення, якщо extreme_point існує
            display_d2L_dx2 = evaluate_expression_for_display(d2L_dx2_expr, self.extreme_point, sym_vars)
            display_d2L_dy2 = evaluate_expression_for_display(d2L_dy2_expr, self.extreme_point, sym_vars)
            display_d2L_dxdy = evaluate_expression_for_display(d2L_dxdy_expr, self.extreme_point, sym_vars)
            display_d2L_dydx = evaluate_expression_for_display(d2L_dydx_expr, self.extreme_point, sym_vars)

            matrix_elements_latex = {
                (0, 0): r"\frac{{\partial^2 L}}{{\partial x^2}} = " + (
                    f"{display_d2L_dx2:.2f}" if isinstance(display_d2L_dx2, (int, float)) else str(display_d2L_dx2)),
                (0, 1): r"\frac{{\partial^2 L}}{{\partial x \partial y}} = " + (
                    f"{display_d2L_dxdy:.2f}" if isinstance(display_d2L_dxdy, (int, float)) else str(display_d2L_dxdy)),
                (1, 0): r"\frac{{\partial^2 L}}{{\partial y \partial x}} = " + (
                    f"{display_d2L_dydx:.2f}" if isinstance(display_d2L_dydx, (int, float)) else str(display_d2L_dydx)),
                (1, 1): r"\frac{{\partial^2 L}}{{\partial y^2}} = " + (
                    f"{display_d2L_dy2:.2f}" if isinstance(display_d2L_dy2, (int, float)) else str(display_d2L_dy2)),
            }

            try:
                fig, ax = plt.subplots(figsize=(4, 2), dpi=100)
                ax.axis('off')  # Вимикаємо осі

                cell_width = 0.4
                cell_height = 0.4
                y_positions = [0.7, 0.2]  # Вертикальні позиції рядків
                x_positions = [0.1, 0.5]  # Горизонтальні позиції стовпців
                fontsize = 12

                for (row, col), latex_label in matrix_elements_latex.items():
                    ax.text(x_positions[col], y_positions[row], f"${latex_label}$", fontsize=fontsize, ha='center',
                            va='center')

                ax.set_xlim(0, 1)
                ax.set_ylim(0, 1)

                buf = io.BytesIO()
                fig.savefig(buf, format='png')
                buf.seek(0)
                plt.close(fig)

                img = QImage.fromData(buf.read())
                pixmap = QPixmap.fromImage(img)

                matrix_label = QLabel()
                matrix_label.setPixmap(pixmap)
                self.hessian_matrix_display_layout.addWidget(matrix_label)  # Додаємо до нового макету

            except Exception as e:
                fallback_text = "Матриця Гессе:\n"
                fallback_text += f"∂²L/∂x² = {display_d2L_dx2}, ∂²L/∂x∂y = {display_d2L_dxdy}\n"
                fallback_text += f"∂²L/∂y∂x = {display_d2L_dydx}, ∂²L/∂y² = {display_d2L_dy2}\n"
                fallback_label = QLabel(fallback_text)
                self.hessian_matrix_display_layout.addWidget(fallback_label)  # Додаємо до нового макету
                print(f"Помилка рендерингу матриці Гессе: {e}")

    def check_determinant(self):
        entered_determinant_str = self.determinant_entry.text().strip()
        try:
            entered_determinant = float(entered_determinant_str)

            if len(self.variables) == 2:
                var1, var2 = self.variables[0], self.variables[1]

                # Отримуємо вирази для похідних
                d2L_dx2_expr = self.calculated_second_derivatives.get((var1, var1), '0')
                d2L_dy2_expr = self.calculated_second_derivatives.get((var2, var2), '0')
                d2L_dxdy_expr = self.calculated_second_derivatives.get((var1, var2), '0')
                d2L_dydx_expr = self.calculated_second_derivatives.get((var2, var1), '0')

                # Створюємо символи для підстановки
                sym_vars = {v: symbols(v) for v in self.variables}
                for k in self.extreme_point.keys():
                    if k.startswith('λ') or k.startswith('lambda'):
                        sym_name = k.replace('λ', 'lambda')
                        sym_vars[k] = symbols(sym_name)

                # Функція для обчислення значення виразу з підстановкою
                def evaluate_expression_for_determinant(expr_str, point, all_sym_vars):
                    try:
                        expr = sympify(str(expr_str))
                        if isinstance(expr, (int, float)):
                            return expr
                        else:
                            subs_dict = {}
                            for var_name, var_sym_obj in all_sym_vars.items():
                                if var_name in point and isinstance(point[var_name], (int, float)):
                                    # Важливо: використовувати символ, який sympy розпізнає для підстановки
                                    subs_dict[var_sym_obj] = point[var_name]

                            temp_expr = expr.subs(subs_dict)
                            if temp_expr.is_Number:  # Якщо результат - число sympy
                                return float(temp_expr)
                            else:  # Якщо результат не число (наприклад, залишилися символи)
                                print(
                                    f"Помилка: Після підстановки '{expr_str}' залишилися символи: {temp_expr.free_symbols}")
                                return 0.0  # Повертаємо 0.0, якщо не можемо обчислити числове значення
                    except Exception as e:
                        print(f"Помилка обчислення виразу '{expr_str}' для визначника: {e}")
                        return 0.0  # Повертаємо 0.0 у випадку помилки

                # Обчислюємо числові значення похідних, підставляючи точку екстремуму, якщо вона є
                d2L_dx2_val = evaluate_expression_for_determinant(d2L_dx2_expr, self.extreme_point, sym_vars)
                d2L_dy2_val = evaluate_expression_for_determinant(d2L_dy2_expr, self.extreme_point, sym_vars)
                d2L_dxdy_val = evaluate_expression_for_determinant(d2L_dxdy_expr, self.extreme_point, sym_vars)
                d2L_dydx_val = evaluate_expression_for_determinant(d2L_dydx_expr, self.extreme_point, sym_vars)

                expected_determinant = (d2L_dx2_val * d2L_dy2_val) - (d2L_dxdy_val * d2L_dydx_val)

                if abs(entered_determinant - expected_determinant) < 1e-6:
                    self.result_label.setText("Визначник введено правильно!")
                    self.next_button.setEnabled(True)
                    self.determinant_value_checked = expected_determinant  # Зберігаємо обчислений визначник
                else:
                    self.result_label.setText(f"Неправильний визначник. Очікуване значення: {expected_determinant:.2f}")
                    self.next_button.setEnabled(False)
                    self.determinant_value_checked = None
            else:
                self.result_label.setText("Перевірка визначника для цієї кількості змінних не реалізована.")
                self.next_button.setEnabled(False)
                self.determinant_value_checked = None

        except ValueError:
            self.result_label.setText("Будь ласка, введіть числове значення визначника.")
            self.next_button.setEnabled(False)
            self.determinant_value_checked = None

    def go_to_prev_step(self):
        self.switch_step(4)

    def go_to_next_step(self):
        print(f"З 5-го етапу передається визначник: {self.determinant_value_checked}")
        self.switch_step(6, determinant=self.determinant_value_checked, extreme_point=self.extreme_point)

    def _clear_layout(self, layout):
        while layout.count():
            item = layout.takeAt(0)
            if item.widget():
                item.widget().deleteLater()
            elif item.layout():
                self._clear_layout(item.layout())
                item.layout().deleteLater()

    def closeEvent(self, event):
        """Обработчик закрытия виджета"""
        print('Закрытие шага 5...')
        # Очищаем ресурсы
        plt.close('all')  # Закрываем все фигуры matplotlib
        event.accept()
from PyQt6.QtWidgets import QWidget, QLabel, QVBoxLayout, QGridLayout, QLineEdit, QHBoxLayout, QPushButton
import sympy as sp
import matplotlib.pyplot as plt
import io
from PyQt6.QtGui import QPixmap, QImage
from test_config import test_config_step4


class LagrangeStep4(QWidget):
    def __init__(self, parent=None, switch_step_callback=None):
        super().__init__(parent)
        self.switch_step = switch_step_callback
        self.variables = []
        self.first_derivatives_str = {}
        self.expected_second_derivatives = {}
        layout = QVBoxLayout()

        instruction_label = QLabel("<b>Етап 4: Введіть другі часткові похідні функції Лагранжа за змінними</b>")
        layout.addWidget(instruction_label)

        self.first_derivatives_labels_layout = QVBoxLayout()
        layout.addLayout(self.first_derivatives_labels_layout)

        derivatives_input_label = QLabel("Введіть другі часткові похідні:")
        layout.addWidget(derivatives_input_label)

        self.derivatives_grid = QGridLayout()
        layout.addLayout(self.derivatives_grid)

        self.check_button = QPushButton("Перевірити")
        self.check_button.clicked.connect(self.check_second_derivatives)
        layout.addWidget(self.check_button)

        self.feedback_label = QLabel("")
        layout.addWidget(self.feedback_label)

        navigation_layout = QHBoxLayout()
        prev_button = QPushButton("Назад")
        prev_button.clicked.connect(self.go_to_prev_step)
        navigation_layout.addWidget(prev_button)

        next_button = QPushButton("Далі")
        next_button.clicked.connect(self.go_to_next_step)
        navigation_layout.addWidget(next_button)

        layout.addLayout(navigation_layout)
        self.setLayout(layout)

    def set_expected_second_derivatives(self, expected_second_derivatives):
        self.expected_second_derivatives = expected_second_derivatives

    def set_data(self, solution=None, second_derivatives=None, variables=None, first_derivatives=None):
        print("Метод set_data викликано на 4-му етапі.")
        print(f"Отримані розв'язки: {solution}")
        print(f"Отримані другі похідні (для довідки): {second_derivatives}")
        print(f"Отримані перші похідні: {first_derivatives}")
        self.variables = variables if variables else []
        self.first_derivatives_str = first_derivatives if first_derivatives else {}
        self._display_first_derivatives()
        self._setup_input_fields()

    def _display_first_derivatives(self):
        # Очищаємо попередні лейбли
        for i in reversed(range(self.first_derivatives_labels_layout.count())):
            widget = self.first_derivatives_labels_layout.itemAt(i).widget()
            if widget is not None:
                widget.deleteLater()

        if self.first_derivatives_str:
            first_derivatives_header = QLabel("<b>Перші часткові похідні (для довідки):</b>")
            self.first_derivatives_labels_layout.addWidget(first_derivatives_header)
            for var, derivative in self.first_derivatives_str.items():
                derivative_latex = f"$\\frac{{\\partial L}}{{\\partial {var}}} = {sp.latex(sp.sympify(derivative))}$"

                try:
                    fig = plt.figure(figsize=(6, 1), dpi=100)
                    fig.text(0.05, 0.5, derivative_latex, fontsize=12)
                    fig.tight_layout()

                    buf = io.BytesIO()
                    fig.savefig(buf, format='png')
                    buf.seek(0)
                    plt.close(fig)

                    img = QImage.fromData(buf.read())
                    pixmap = QPixmap.fromImage(img)

                    derivative_label = QLabel()
                    derivative_label.setPixmap(pixmap)
                    self.first_derivatives_labels_layout.addWidget(derivative_label)

                except Exception as e:
                    derivative_label_fallback = QLabel(f"∂L/∂{var} = {derivative}")
                    self.first_derivatives_labels_layout.addWidget(derivative_label_fallback)
                    print(f"Помилка рендерингу LaTeX (крок 4): {e}")
        else:
            no_derivatives_label = QLabel("Перші часткові похідні не знайдено.")
            self.first_derivatives_labels_layout.addWidget(no_derivatives_label)

    def _setup_input_fields(self):
        # Очищаємо попередні поля
        for i in reversed(range(self.derivatives_grid.count())):
            widget = self.derivatives_grid.itemAt(i).widget()
            if widget is not None:
                widget.deleteLater()
        self.second_derivative_entries = {}

        if len(self.variables) == 2:
            var1, var2 = self.variables[0], self.variables[1]

            labels_data = [
                (f"$\\frac{{\\partial^2 L}}{{\\partial {var1}^2}}$ = ", (0, 0), (var1, var1), 0),
                (f"$\\frac{{\\partial^2 L}}{{\\partial {var1} \\partial {var2}}}$ = ", (0, 2), (var1, var2), 1),
                (f"$\\frac{{\\partial^2 L}}{{\\partial {var2} \\partial {var1}}}$ = ", (1, 0), (var2, var1), 2),
                (f"$\\frac{{\\partial^2 L}}{{\\partial {var2}^2}}$ = ", (1, 2), (var2, var2), 3),
            ]

            for text_latex, (row, col), derivative_vars, index in labels_data:
                try:
                    fig = plt.figure(figsize=(3, 1), dpi=100)
                    fig.text(0.05, 0.5, text_latex, fontsize=12)
                    fig.tight_layout()

                    buf = io.BytesIO()
                    fig.savefig(buf, format='png')
                    buf.seek(0)
                    plt.close(fig)

                    img = QImage.fromData(buf.read())
                    pixmap = QPixmap.fromImage(img)

                    label = QLabel()
                    label.setPixmap(pixmap)
                    self.derivatives_grid.addWidget(label, row, col)

                    entry = QLineEdit()
                    entry.setText(str(test_config_step4[index]))

                    self.derivatives_grid.addWidget(entry, row, col + 1)
                    self.second_derivative_entries[derivative_vars] = entry

                except Exception as e:
                    label_fallback = QLabel(text_latex.replace('$', ''))
                    self.derivatives_grid.addWidget(label_fallback, row, col)
                    entry = QLineEdit()
                    self.derivatives_grid.addWidget(entry, row, col + 1)
                    self.second_derivative_entries[derivative_vars] = entry
                    print(f"Помилка рендерингу LaTeX (другі похідні): {e}")

    def get_second_derivatives_input(self):
        second_derivatives_input = {}
        for (var1, var2), entry in self.second_derivative_entries.items():
            text = entry.text().strip()
            try:
                second_derivatives_input[(var1, var2)] = float(text)
            except ValueError:
                second_derivatives_input[(var1, var2)] = text # Зберігаємо як текст, якщо не вдалося перетворити на число
        return second_derivatives_input

    def check_second_derivatives(self):
        entered_derivatives = self.get_second_derivatives_input()
        all_correct = True
        feedback_text = "Неправильно введені другі похідні: "
        incorrect_derivatives = []

        def normalize_lambda(s):
            return (
                s.replace('lambda₁', 'λ1')
                 .replace('lambda1', 'λ1')
                 .replace('λ₁', 'λ1')
            )

        for (var1, var2), entered_value in entered_derivatives.items():
            expected_value_str = self.expected_second_derivatives.get((var1, var2), "").lower().replace(" ", "")
            entered_value_str = str(entered_value).lower().replace(" ", "")

            expected_value_str = normalize_lambda(expected_value_str)
            entered_value_str = normalize_lambda(entered_value_str)

            try:
                expected_expr = sp.simplify(sp.sympify(expected_value_str))
                entered_expr = sp.simplify(sp.sympify(entered_value_str))
                if not expected_expr.equals(entered_expr):
                    all_correct = False
                    incorrect_derivatives.append(f"∂²L/∂{var1}∂{var2}")
            except Exception as e:
                if expected_value_str != entered_value_str:
                    all_correct = False
                    incorrect_derivatives.append(f"∂²L/∂{var1}∂{var2}")

        if all_correct:
            self.feedback_label.setText("Другі похідні введено правильно!")
            print("Другі похідні введено правильно!")
        else:
            self.feedback_label.setText(feedback_text + ", ".join(incorrect_derivatives))
            print(f"Другі похідні введено неправильно! {feedback_text + ', '.join(incorrect_derivatives)}")

    def go_to_prev_step(self):
        self.switch_step(3)

    def go_to_next_step(self):
        second_derivatives = self.get_second_derivatives_input()
        print(f"Введені другі похідні (для матриці Гессе): {second_derivatives}")
        self.switch_step(5, second_derivatives=second_derivatives) # Перехід на наступний етап

    def closeEvent(self, event):
        """Обработчик закрытия виджета"""
        print('Закрытие шага 4...')
        # Очищаем ресурсы
        plt.close('all')  # Закрываем все фигуры matplotlib
        event.accept()
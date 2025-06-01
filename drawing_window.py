# drawing_window.py
from PyQt6.QtWidgets import QWidget, QVBoxLayout, QHBoxLayout, QPushButton, QApplication, QLabel, QSlider, QColorDialog, \
    QSizePolicy
from PyQt6.QtGui import QPainter, QPen, QColor, QPixmap
from PyQt6.QtCore import Qt, QPoint, QSize


class DrawingWindow(QWidget):
    def __init__(self, parent=None, equations_to_display=None):
        super().__init__(parent)
        self.setWindowTitle("Полотно для обчислень (чернетка)")
        self.setGeometry(200, 200, 800, 600)

        self.equations_to_display = equations_to_display if equations_to_display else []

        self.image = QPixmap(self.size())
        self.image.fill(QColor("white"))

        self.drawing = False
        self.lastPoint = QPoint()

        self.current_pen_color = QColor("black")
        self.current_pen_width = 3
        self.is_eraser_mode = False

        main_layout = QVBoxLayout()

        # ------------------ Панель інструментів та відображення рівнянь ------------------
        top_panel_layout = QHBoxLayout()

        # Макет для відображення рівнянь
        equations_display_layout = QVBoxLayout()
        equations_label = QLabel("<b>Система рівнянь або інформація:</b>")
        equations_display_layout.addWidget(equations_label)

        if self.equations_to_display:
            eq_text = ""
            for i, eq_str in enumerate(self.equations_to_display):
                if isinstance(eq_str, tuple) and len(eq_str) == 2:
                    eq_text += f"{eq_str[0]}: {eq_str[1]}<br>"
                else:
                    eq_text += f"• {eq_str}<br>"
            self.equations_text_label = QLabel(eq_text)
            self.equations_text_label.setTextFormat(Qt.TextFormat.RichText)
        else:
            self.equations_text_label = QLabel("Інформація не надана.")
        self.equations_text_label.setWordWrap(True)
        equations_display_layout.addWidget(self.equations_text_label)
        equations_display_layout.addStretch()

        top_panel_layout.addLayout(equations_display_layout, 2)

        # Макет для кнопок інструментів
        tool_buttons_layout = QVBoxLayout()

        clear_button = QPushButton("Очистити полотно")
        clear_button.clicked.connect(self.clear_canvas)
        tool_buttons_layout.addWidget(clear_button)

        color_button = QPushButton("Вибрати колір")
        color_button.clicked.connect(self.choose_color)
        tool_buttons_layout.addWidget(color_button)

        width_label = QLabel("Товщина олівця:")
        self.width_slider = QSlider(Qt.Orientation.Horizontal)
        self.width_slider.setRange(1, 15)
        self.width_slider.setValue(self.current_pen_width)
        self.width_slider.valueChanged.connect(self.set_pen_width)
        tool_buttons_layout.addWidget(width_label)
        tool_buttons_layout.addWidget(self.width_slider)

        eraser_button = QPushButton("Ластик")
        eraser_button.clicked.connect(self.toggle_eraser)
        tool_buttons_layout.addWidget(eraser_button)

        tool_buttons_layout.addStretch()
        top_panel_layout.addLayout(tool_buttons_layout, 1)

        main_layout.addLayout(top_panel_layout)

        # ------------------ Власне полотно для малювання ------------------
        self.canvas_widget = QWidget(self)
        self.canvas_widget.setStyleSheet("border: 1px solid gray; background-color: white;")
        self.canvas_widget.setMinimumSize(900, 600)

        self.canvas_widget.setSizePolicy(
            QSizePolicy.Policy.Preferred, QSizePolicy.Policy.Expanding
        )

        self.canvas_widget.paintEvent = self.paintEvent_canvas
        self.canvas_widget.mousePressEvent = self.mousePressEvent_canvas
        self.canvas_widget.mouseMoveEvent = self.mouseMoveEvent_canvas
        self.canvas_widget.mouseReleaseEvent = self.mouseReleaseEvent_canvas

        main_layout.addWidget(self.canvas_widget)

        self.setLayout(main_layout)

    def paintEvent(self, event):
        pass  # Цей метод не використовується для малювання на вікні напряму

    def paintEvent_canvas(self, event):
        painter = QPainter(self.canvas_widget)
        painter.drawPixmap(self.canvas_widget.rect(), self.image)

    def mousePressEvent_canvas(self, event):
        if event.button() == Qt.MouseButton.LeftButton:
            self.drawing = True
            self.lastPoint = event.pos()

    def mouseMoveEvent_canvas(self, event):
        if event.buttons() & Qt.MouseButton.LeftButton and self.drawing:
            painter = QPainter(self.image)

            if self.is_eraser_mode:
                painter.setPen(QPen(QColor("white"), self.current_pen_width * 2,
                                    Qt.PenStyle.SolidLine, Qt.PenCapStyle.RoundCap, Qt.PenJoinStyle.RoundJoin))
            else:
                painter.setPen(QPen(self.current_pen_color, self.current_pen_width,
                                    Qt.PenStyle.SolidLine, Qt.PenCapStyle.RoundCap, Qt.PenJoinStyle.RoundJoin))

            painter.drawLine(self.lastPoint, event.pos())
            self.lastPoint = event.pos()
            self.canvas_widget.update()

    def mouseReleaseEvent_canvas(self, event):
        if event.button() == Qt.MouseButton.LeftButton:
            self.drawing = False

    def resizeEvent(self, event):
        new_canvas_size = self.canvas_widget.size()

        if self.image.size() != new_canvas_size and new_canvas_size.isValid():
            new_image = QPixmap(new_canvas_size)
            new_image.fill(QColor("white"))
            painter = QPainter(new_image)
            painter.drawPixmap(new_image.rect(), self.image)
            self.image = new_image

        super().resizeEvent(event)

    def clear_canvas(self):
        self.image.fill(QColor("white"))
        self.canvas_widget.update()

    def choose_color(self):
        color = QColorDialog.getColor(self.current_pen_color, self, "Виберіть колір олівця")
        if color.isValid():
            self.current_pen_color = color
            self.is_eraser_mode = False
            print(f"Колір олівця змінено на {self.current_pen_color.name()}")

    def set_pen_width(self, value):
        self.current_pen_width = value
        print(f"Товщина олівця змінено на {self.current_pen_width}")

    def toggle_eraser(self):
        self.is_eraser_mode = not self.is_eraser_mode
        if self.is_eraser_mode:
            self.set_pen_width(10)
            self.width_slider.setValue(10)
            print("Режим ластика увімкнено.")
        else:
            self.set_pen_width(3)
            self.width_slider.setValue(3)
            print("Режим ластика вимкнено.")


# Для тестування окремо
if __name__ == '__main__':
    app = QApplication([])
    equations_example = [
        "Це приклад рівнянь для чернетки:",
        "∂L/∂x = 3x^2 - 2λ = 0",
        "∂L/∂y = 4y - λ = 0",
        "∂L/∂λ = -2x - y = 0"
    ]
    window = DrawingWindow(equations_to_display=equations_example)
    window.show()
    app.exec()
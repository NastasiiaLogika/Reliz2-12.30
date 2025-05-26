import sys
from PyQt5.QtWidgets import (
    QWidget, QVBoxLayout, QHBoxLayout, QLabel, QComboBox,
    QLineEdit, QPushButton, QApplication, QSizePolicy, QMessageBox
)
from PyQt5.QtGui import QFont
from PyQt5.QtCore import Qt

# Масштаби конвертації відносно м/с
SPEED_UNITS = {
    "метр/секунда (m/s)": 1,
    "кілометр/година (km/h)": 0.277778,
    "миля/година (mph)": 0.44704,
    "вузол (knots)": 0.514444,
    "фут/секунда (ft/s)": 0.3048,
    "кілометр/секунда (km/s)": 1000,
    "миля/секунда (mi/s)": 1609.34
}

class SpeedConverter(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Конвертер швидкості")
        self.setFixedSize(700, 450)
        self.units = list(SPEED_UNITS.keys())
        self.init_ui()

    def init_ui(self):
        layout = QVBoxLayout()
        layout.setContentsMargins(20, 20, 20, 20)
        layout.setSpacing(15)

        title = QLabel("Конвертер швидкості")
        title.setFont(QFont("Arial", 20, QFont.Bold))
        title.setAlignment(Qt.AlignCenter)
        layout.addWidget(title)

        # Вхідна сума
        self.input_amount = QLineEdit()
        self.input_amount.setPlaceholderText("Введіть значення")
        self.input_amount.setFont(QFont("Arial", 14))
        self.input_amount.setFixedHeight(40)
        self.input_amount.setAlignment(Qt.AlignRight)
        layout.addWidget(self.input_amount)

        # Вибір одиниць
        h_layout = QHBoxLayout()

        self.combo_from = QComboBox()
        self.combo_from.setFont(QFont("Arial", 14))
        self.combo_from.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Fixed)
        self.combo_from.addItems(self.units)
        h_layout.addWidget(self.combo_from)

        arrow_label = QLabel("→")
        arrow_label.setFont(QFont("Arial", 18, QFont.Bold))
        arrow_label.setAlignment(Qt.AlignCenter)
        h_layout.addWidget(arrow_label)

        self.combo_to = QComboBox()
        self.combo_to.setFont(QFont("Arial", 14))
        self.combo_to.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Fixed)
        self.combo_to.addItems(self.units)
        h_layout.addWidget(self.combo_to)

        layout.addLayout(h_layout)

        # Кнопка конвертації
        btn_convert = QPushButton("Конвертувати")
        btn_convert.setFont(QFont("Arial", 14))
        btn_convert.setFixedHeight(45)
        btn_convert.clicked.connect(self.convert_speed)
        layout.addWidget(btn_convert)

        # Результат
        self.label_result = QLabel("")
        self.label_result.setFont(QFont("Arial", 16))
        self.label_result.setAlignment(Qt.AlignCenter)
        layout.addWidget(self.label_result)

        self.setLayout(layout)

    def convert_speed(self):
        amount_text = self.input_amount.text()
        if not amount_text:
            self.show_error("Будь ласка, введіть значення")
            return
        try:
            amount = float(amount_text.replace(",", "."))
        except ValueError:
            self.show_error("Введіть коректне числове значення")
            return

        from_unit = self.combo_from.currentText()
        to_unit = self.combo_to.currentText()

        if from_unit == to_unit:
            self.label_result.setText(f"Результат: {amount:.4f} {to_unit}")
            return

        try:
            # Конвертація через m/s
            amount_in_mps = amount * SPEED_UNITS[from_unit]
            converted_amount = amount_in_mps / SPEED_UNITS[to_unit]
            self.label_result.setText(f"Результат: {converted_amount:.4f} {to_unit}")
        except Exception as e:
            self.show_error(f"Помилка конвертації: {e}")

    def show_error(self, message):
        QMessageBox.critical(self, "Помилка", message)

if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = SpeedConverter()
    window.show()
    sys.exit(app.exec_())

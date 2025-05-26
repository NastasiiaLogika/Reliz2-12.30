# main.py
import sys
from PyQt5.QtWidgets import QApplication, QWidget, QVBoxLayout, QPushButton, QLabel, QSizePolicy
from PyQt5.QtCore import Qt

# Імпортуй твої вікна (поки що калькулятор)
from ui import Calculator
from  red import CurrencyConverter
from convent_kg import WeightConverter
from convent_km import SpeedConverter
# from converter import CurrencyConverter
# from unit_converter import UnitConverter

class MainMenu(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Головне меню")
        self.setFixedSize(300, 400)
        self.init_ui()

    def init_ui(self):
        layout = QVBoxLayout()
        layout.setSpacing(20)
        layout.setContentsMargins(30, 30, 30, 30)

        title = QLabel("Виберіть функцію")
        title.setAlignment(Qt.AlignCenter)
        title.setStyleSheet("font-size: 20px; font-weight: bold;")
        layout.addWidget(title)

        # Кнопки меню
        btn_calc = QPushButton("Калькулятор")
        btn_calc.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)
        btn_calc.clicked.connect(self.open_calculator)
        layout.addWidget(btn_calc)

        btn_currency = QPushButton("Конвертер валют")
        btn_currency.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)
        btn_currency.clicked.connect(self.open_currency_converter)
        layout.addWidget(btn_currency)

        btn_grams_kg = QPushButton("Грами ↔ Кілограми")
        btn_grams_kg.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)
        btn_grams_kg.clicked.connect(self.open_unit_converter_grams_kg)
        layout.addWidget(btn_grams_kg)

        btn_speed = QPushButton("Конвертер швидкості")
        btn_speed.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)
        btn_speed.clicked.connect(self.open_unit_converter_speed)
        layout.addWidget(btn_speed)

        self.setLayout(layout)

    def open_calculator(self):
        self.calculator_window = Calculator()
        self.calculator_window.show()
        self.close()

    def open_currency_converter(self):
        self.calculator_window = CurrencyConverter()
        self.calculator_window.show()
        self.close()
        print("Відкрити конвертер валют - тут буде логіка")

    def open_unit_converter_grams_kg(self):
        self.calculator_window = WeightConverter()
        self.calculator_window.show()
        self.close()
        print("Відкрити конвертер грам ↔ кг - тут буде логіка")

    def open_unit_converter_speed(self):
        self.calculator_window = SpeedConverter()
        self.calculator_window.show()
        self.close()
        print("Відкрити конвертер швидкості - тут буде логіка")

if __name__ == "__main__":
    app = QApplication(sys.argv)
    main_menu = MainMenu()
    main_menu.show()
    sys.exit(app.exec_())

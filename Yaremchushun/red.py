import sys
from PyQt5.QtWidgets import (
    QWidget, QVBoxLayout, QHBoxLayout, QLabel, QComboBox,
    QLineEdit, QPushButton, QApplication, QSizePolicy, QMessageBox
)
from PyQt5.QtGui import QFont
from PyQt5.QtCore import Qt
import requests

API_URL = "https://open.er-api.com/v6/latest/{}"  # без API ключа, безкоштовна версія

class CurrencyConverter(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Конвертер валют")
        self.setFixedSize(600, 450)
        self.currencies = []
        self.rates = {}
        self.init_ui()
        self.fetch_currencies()

    def init_ui(self):
        layout = QVBoxLayout()
        layout.setContentsMargins(20, 20, 20, 20)
        layout.setSpacing(15)

        title = QLabel("Конвертер валют")
        title.setFont(QFont("Arial", 20, QFont.Bold))
        title.setAlignment(Qt.AlignCenter)
        layout.addWidget(title)

        # Вхідна сума
        self.input_amount = QLineEdit()
        self.input_amount.setPlaceholderText("Введіть суму")
        self.input_amount.setFont(QFont("Arial", 14))
        self.input_amount.setFixedHeight(40)
        self.input_amount.setAlignment(Qt.AlignRight)
        layout.addWidget(self.input_amount)

        # Вибір валюти від і до
        h_layout = QHBoxLayout()

        self.combo_from = QComboBox()
        self.combo_from.setFont(QFont("Arial", 14))
        self.combo_from.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Fixed)
        h_layout.addWidget(self.combo_from)

        arrow_label = QLabel("→")
        arrow_label.setFont(QFont("Arial", 18, QFont.Bold))
        arrow_label.setAlignment(Qt.AlignCenter)
        h_layout.addWidget(arrow_label)

        self.combo_to = QComboBox()
        self.combo_to.setFont(QFont("Arial", 14))
        self.combo_to.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Fixed)
        h_layout.addWidget(self.combo_to)

        layout.addLayout(h_layout)

        # Кнопка конвертації
        btn_convert = QPushButton("Конвертувати")
        btn_convert.setFont(QFont("Arial", 14))
        btn_convert.setFixedHeight(45)
        btn_convert.clicked.connect(self.convert_currency)
        layout.addWidget(btn_convert)

        # Результат
        self.label_result = QLabel("")
        self.label_result.setFont(QFont("Arial", 16))
        self.label_result.setAlignment(Qt.AlignCenter)
        layout.addWidget(self.label_result)

        self.setLayout(layout)

    def fetch_currencies(self):
        # Отримуємо список валют та курси відносно USD
        try:
            response = requests.get(API_URL.format("USD"))
            data = response.json()
            if data["result"] == "success":
                self.rates = data["rates"]
                self.currencies = sorted(self.rates.keys())
                self.combo_from.addItems(self.currencies)
                self.combo_to.addItems(self.currencies)
                # Встановлюємо USD та EUR за замовчуванням
                self.combo_from.setCurrentText("USD")
                self.combo_to.setCurrentText("EUR")
            else:
                self.show_error("Не вдалося отримати курси валют")
        except Exception as e:
            self.show_error(f"Помилка при отриманні курсів: {e}")

    def convert_currency(self):
        amount_text = self.input_amount.text()
        if not amount_text:
            self.show_error("Будь ласка, введіть суму")
            return
        try:
            amount = float(amount_text.replace(",", "."))
        except ValueError:
            self.show_error("Введіть коректне числове значення")
            return

        from_currency = self.combo_from.currentText()
        to_currency = self.combo_to.currentText()

        if from_currency == to_currency:
            self.label_result.setText(f"Результат: {amount:.2f} {to_currency}")
            return

        try:
            # Конвертуємо через USD
            if from_currency != "USD":
                amount_in_usd = amount / self.rates[from_currency]
            else:
                amount_in_usd = amount
            converted_amount = amount_in_usd * self.rates[to_currency]
            self.label_result.setText(f"Результат: {converted_amount:.2f} {to_currency}")
        except Exception as e:
            self.show_error(f"Помилка конвертації: {e}")

    def show_error(self, message):
        QMessageBox.critical(self, "Помилка", message)

if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = CurrencyConverter()
    window.show()
    sys.exit(app.exec_())

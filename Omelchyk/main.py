import random
import string
from PyQt5.QtWidgets import (
    QApplication, QWidget, QLabel, QPushButton, QVBoxLayout,
    QLineEdit, QMessageBox, QCheckBox, QProgressBar, QListWidget
)
from PyQt5.QtGui import QClipboard
import sys


class PasswordGeneratorApp(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Генератор паролів")
        self.setFixedSize(800, 900)


        self.password_history = []  # Історія паролів


        # Заголовок
        self.label = QLabel("Введіть параметри і натисніть кнопку для генерації паролю:")
        self.label.setStyleSheet("font-size: 18px;")


        # Поле вводу довжини
        self.length_input = QLineEdit()
        self.length_input.setPlaceholderText("Довжина паролю (наприклад, 12)")
        self.length_input.setStyleSheet("font-size: 16px; padding: 6px;")


        # Чекбокси для символів
        self.uppercase_checkbox = QCheckBox("Великі літери (A-Z)")
        self.lowercase_checkbox = QCheckBox("Малі літери (a-z)")
        self.digits_checkbox = QCheckBox("Цифри (0-9)")
        self.symbols_checkbox = QCheckBox("Спецсимволи (!@#...)")
        for checkbox in [self.uppercase_checkbox, self.lowercase_checkbox, self.digits_checkbox, self.symbols_checkbox]:
            checkbox.setChecked(True)


        # Кнопка генерації
        self.generate_button = QPushButton("🔐 Згенерувати пароль")
        self.generate_button.setStyleSheet("font-size: 16px; padding: 10px;")
        self.generate_button.clicked.connect(self.generate_password)


        # Вивід паролю
        self.password_label = QLabel("")
        self.password_label.setWordWrap(True)
        self.password_label.setStyleSheet("font-size: 20px; font-weight: bold;")


        # Кнопка копіювання
        self.copy_button = QPushButton("📋 Скопіювати в буфер")
        self.copy_button.setStyleSheet("font-size: 16px; padding: 8px;")
        self.copy_button.clicked.connect(self.copy_to_clipboard)


        # Прогрес-бар складності
        self.strength_bar = QProgressBar()
        self.strength_bar.setMaximum(100)
        self.strength_bar.setTextVisible(True)
        self.strength_bar.setStyleSheet("font-size: 14px;")


        # Історія паролів
        self.history_label = QLabel("Історія згенерованих паролів:")
        self.history_label.setStyleSheet("font-size: 16px; font-weight: bold;")
        self.history_list = QListWidget()
        self.history_list.setStyleSheet("font-size: 14px;")


        # Макет
        layout = QVBoxLayout()
        layout.addWidget(self.label)
        layout.addWidget(self.length_input)
        layout.addWidget(self.uppercase_checkbox)
        layout.addWidget(self.lowercase_checkbox)
        layout.addWidget(self.digits_checkbox)
        layout.addWidget(self.symbols_checkbox)
        layout.addWidget(self.generate_button)
        layout.addWidget(self.password_label)
        layout.addWidget(self.copy_button)
        layout.addWidget(QLabel("Стійкість паролю:"))
        layout.addWidget(self.strength_bar)
        layout.addWidget(self.history_label)
        layout.addWidget(self.history_list)
        self.setLayout(layout)


    def get_selected_characters(self):
        characters = ""
        if self.uppercase_checkbox.isChecked():
            characters += string.ascii_uppercase
        if self.lowercase_checkbox.isChecked():
            characters += string.ascii_lowercase
        if self.digits_checkbox.isChecked():
            characters += string.digits
        if self.symbols_checkbox.isChecked():
            characters += string.punctuation
        return characters


    def evaluate_strength(self, password):
        score = 0
        if any(c.islower() for c in password): score += 1
        if any(c.isupper() for c in password): score += 1
        if any(c.isdigit() for c in password): score += 1
        if any(c in string.punctuation for c in password): score += 1
        length = len(password)
        if length >= 12: score += 1
        elif length >= 8: score += 0.5


        percent = int((score / 5) * 100)
        self.strength_bar.setValue(percent)
        if percent < 40:
            self.strength_bar.setFormat("Слабкий")
        elif percent < 70:
            self.strength_bar.setFormat("Середній")
        else:
            self.strength_bar.setFormat("Надійний")


    def generate_password(self):
        characters = self.get_selected_characters()
        if not characters:
            QMessageBox.warning(self, "Увага", "Оберіть хоча б один тип символів.")
            return


        try:
            length = int(self.length_input.text())
            if length < 4:
                raise ValueError
        except ValueError:
            QMessageBox.warning(self, "Помилка", "Введіть коректну довжину (ціле число від 4).")
            return


        password = ''.join(random.choice(characters) for _ in range(length))
        self.password_label.setText(password)
        self.evaluate_strength(password)


        # Оновлення історії
        self.password_history.insert(0, password)
        self.history_list.insertItem(0, password)
        if len(self.password_history) > 10:
            self.password_history = self.password_history[:10]
            self.history_list.takeItem(10)


    def copy_to_clipboard(self):
        clipboard = QApplication.clipboard()
        clipboard.setText(self.password_label.text())
        QMessageBox.information(self, "Скопійовано", "Пароль скопійовано в буфер обміну.")


if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = PasswordGeneratorApp()
    window.show()
    sys.exit(app.exec_())



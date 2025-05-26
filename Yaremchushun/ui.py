from PyQt5.QtWidgets import (
    QWidget, QVBoxLayout, QHBoxLayout, QPushButton, QLabel,
    QStackedWidget, QSizePolicy, QMenu, QAction, QLineEdit
)
from PyQt5.QtGui import QFont, QPainter, QColor
from PyQt5.QtCore import Qt, QRect
from logik import safe_eval
from therm import apply_theme
from red import*

translations = {
    "uk": {
        "title": "Калькулятор",
        "placeholder": "Введіть математичну задачу…",
        "theme": "Перемкнути тему",
        "tabs": ["Стандарт", "Функції", "Тригонометрія", "Символи"]
    },
    "en": {
        "title": "Calculator",
        "placeholder": "Enter a math expression…",
        "theme": "Toggle Theme",
        "tabs": ["Standard", "Functions", "Trigonometry", "Symbols"]
    },
    "ar": {
        "title": "آلة حاسبة",
        "placeholder": "أدخل مسألة رياضية…",
        "theme": "تبديل الوضع",
        "tabs": ["قياسي", "دوال", "مثلثات", "رموز"]
    },
    "zh": {
        "title": "计算器",
        "placeholder": "输入数学表达式…",
        "theme": "切换主题",
        "tabs": ["标准", "函数", "三角", "符号"]
    },
    "de": {
        "title": "Rechner",
        "placeholder": "Mathematischen Ausdruck eingeben…",
        "theme": "Thema wechseln",
        "tabs": ["Standard", "Funktionen", "Trigonometrie", "Symbole"]
    }
}

class SquareLineEdit(QLineEdit):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setMaxLength(100)
        self.setAlignment(Qt.AlignLeft)
        self.setFont(QFont("Arial", 18))
        self.setStyleSheet("background: white; color: black; border: none; padding: 10px;")
        self.cursor_pos = 0
        self.textChanged.connect(self.update_cursor_position)

    def update_cursor_position(self):
        self.cursor_pos = len(self.text())

    def paintEvent(self, event):
        super().paintEvent(event)
        painter = QPainter(self)
        painter.setRenderHint(QPainter.Antialiasing)
        width = self.width()
        height = self.height()
        text = self.text()
        max_cols = 10
        box_width = width / max_cols
        box_height = height / 2 if len(text) > max_cols else height
        for i in range(max(len(text), max_cols)):
            row = i // max_cols
            col = i % max_cols
            rect = QRect(int(col * box_width), int(row * box_height), int(box_width), int(box_height))
            painter.setBrush(QColor(220, 220, 255) if i == self.cursor_pos else Qt.white)
            painter.setPen(QColor(180, 180, 180))
            painter.drawRect(rect)
        for i, ch in enumerate(text):
            row = i // max_cols
            col = i % max_cols
            rect = QRect(int(col * box_width), int(row * box_height), int(box_width), int(box_height))
            painter.setPen(Qt.black)
            painter.setFont(QFont("Arial", 24))
            painter.drawText(rect, Qt.AlignCenter, ch)

class Calculator(QWidget):
    def __init__(self):
        super().__init__()
        self.setFixedSize(400, 700)
        self.is_dark_theme = False
        self.current_input = ""
        self.current_lang = "uk"

        self.main_layout = QVBoxLayout(self)
        self.main_layout.setContentsMargins(0, 0, 0, 0)
        self.main_layout.setSpacing(0)

        self.build_top_bar()

        self.input_field = SquareLineEdit()
        self.main_layout.addWidget(self.input_field)

        self.build_tabs()
        apply_theme(self, self.input_field, self.is_dark_theme)
        self.update_language_ui()

    def build_top_bar(self):
        top_bar = QWidget()
        top_bar.setFixedHeight(50)
        top_layout = QHBoxLayout(top_bar)
        top_layout.setContentsMargins(10, 0, 10, 0)

        settings_button = QPushButton("⚙️")
        settings_button.setFixedSize(40, 40)
        settings_button.setStyleSheet("border: none; font-size: 18px;")
        settings_button.clicked.connect(self.show_settings_menu)

        self.title_label = QLabel()
        self.title_label.setFont(QFont("Arial", 16))
        self.title_label.setAlignment(Qt.AlignCenter)
        self.title_label.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Preferred)

        top_layout.addWidget(settings_button)
        top_layout.addWidget(self.title_label)
        top_layout.addStretch()
        self.main_layout.addWidget(top_bar)

    def show_settings_menu(self):
        menu = QMenu(self)

        toggle_theme_action = QAction(translations[self.current_lang]["theme"], self)
        toggle_theme_action.triggered.connect(self.toggle_theme)
        menu.addAction(toggle_theme_action)

        lang_menu = QMenu("🌐 Мова", self)
        for lang_code, lang_name in [("uk", "Українська"), ("en", "English"), ("ar", "العربية"), ("zh", "中文"), ("de", "Deutsch")]:
            action = QAction(lang_name, self)
            action.triggered.connect(lambda checked, code=lang_code: self.set_language(code))
            lang_menu.addAction(action)
        menu.addMenu(lang_menu)

        menu.exec_(self.mapToGlobal(self.sender().pos() + self.sender().rect().bottomRight()))

    def set_language(self, lang_code):
        self.current_lang = lang_code
        self.update_language_ui()

    def update_language_ui(self):
        t = translations[self.current_lang]
        self.setWindowTitle(t["title"])
        self.title_label.setText(t["title"])
        self.input_field.setPlaceholderText(t["placeholder"])

        tab_labels = t["tabs"]
        for i, label in enumerate(tab_labels):
            if i < len(self.tabs):
                self.tabs[i].setText(label)

    def toggle_theme(self):
        self.is_dark_theme = not self.is_dark_theme
        apply_theme(self, self.input_field, self.is_dark_theme)

    def build_tabs(self):
        tab_widget = QWidget()
        tab_layout = QHBoxLayout(tab_widget)
        tab_layout.setContentsMargins(5, 5, 5, 5)
        tab_layout.setSpacing(5)

        self.tabs = []
        self.stacked_keyboards = QStackedWidget()

        tab_data = [
            ("", self.create_keyboard),
            ("", lambda: self.create_keyboard([
                ["|x|", "log10", "ln", "√x"],
                ["e", "exp", "x^2", "x^3"]
            ])),
            ("", lambda: self.create_keyboard([
                ["sin", "cos", "tan", "cot"],
                ["arcsin", "arccos", "arctan", "arccot"]
            ])),
            ("", lambda: self.create_keyboard([
                ["π", "%", "∞", "∑"],
                ["∈", "∉", "∀", "∃"]
            ]))
        ]

        for index, (_, builder) in enumerate(tab_data):
            btn = QPushButton("")
            btn.setCheckable(True)
            btn.setFont(QFont("Arial", 10))
            btn.clicked.connect(lambda _, i=index: self.switch_tab(i))
            self.tabs.append(btn)
            tab_layout.addWidget(btn)
            self.stacked_keyboards.addWidget(builder())

        self.tabs[0].setChecked(True)
        tab_widget.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Fixed)
        self.main_layout.addWidget(tab_widget)
        self.main_layout.addWidget(self.stacked_keyboards)

    def switch_tab(self, index):
        for i, tab in enumerate(self.tabs):
            tab.setChecked(i == index)
        self.stacked_keyboards.setCurrentIndex(index)

    def create_keyboard(self, layout=None):
        if layout is None:
            layout = [
                ["7", "8", "9", "/"],
                ["4", "5", "6", "*"],
                ["1", "2", "3", "-"],
                ["0", ".", "=", "+"],
                ["C"]
            ]
        widget = QWidget()
        v_layout = QVBoxLayout(widget)
        for row in layout:
            h_layout = QHBoxLayout()
            for label in row:
                btn = QPushButton(label)
                btn.setFont(QFont("Arial", 16))
                btn.setFixedHeight(60)
                btn.clicked.connect(lambda _, text=label: self.on_button_click(text))
                h_layout.addWidget(btn)
            v_layout.addLayout(h_layout)
        return widget

    def on_button_click(self, text):
        if text == "=":
            self.calculate_result()
        elif text == "C":
            self.clear_input()
        else:
            self.current_input += text
            self.input_field.setText(self.current_input)

    def calculate_result(self):
        result = safe_eval(self.current_input)
        self.input_field.setText(str(result))
        self.current_input = str(result)

    def clear_input(self):
        self.current_input = ""
        self.input_field.clear()

    def update_input(self):
        self.current_input = self.input_field.text()

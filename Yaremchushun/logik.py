import math
import json
import os

# Шлях до файлу збереження
SAVE_FILE = "saved_expression.json"

# Дозволені функції
safe_dict = {
    "abs": abs,
    "log10": math.log10,
    "ln": math.log,  # натур. логарифм
    "sqrt": math.sqrt,
    "e": math.e,
    "exp": math.exp,
    "pi": math.pi,
    "sin": math.sin,
    "cos": math.cos,
    "tan": math.tan,
    "cot": lambda x: 1 / math.tan(x),
    "arcsin": math.asin,
    "arccos": math.acos,
    "arctan": math.atan,
    "arccot": lambda x: math.atan(1 / x) if x != 0 else float('inf'),
    "x": None  # підставляється автоматично
}

def safe_eval(expr: str):
    try:
        # Деякі заміни для зручності
        expr = expr.replace("^", "**").replace("√", "sqrt")
        expr = expr.replace("π", "pi").replace("∞", "float('inf')")

        # eval із обмеженням простору імен
        return eval(expr, {"__builtins__": None}, safe_dict)
    except Exception as e:
        return f"Помилка: {e}"

def save_expression(expr: str):
    try:
        with open(SAVE_FILE, "w", encoding="utf-8") as f:
            json.dump({"expression": expr}, f)
    except Exception as e:
        print(f"Не вдалося зберегти: {e}")

def load_expression():
    if not os.path.exists(SAVE_FILE):
        return ""
    try:
        with open(SAVE_FILE, "r", encoding="utf-8") as f:
            data = json.load(f)
            return data.get("expression", "")
    except Exception as e:
        print(f"Не вдалося завантажити: {e}")
        return ""

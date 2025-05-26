import tkinter as tk

# Функція для виконання конвертації одиниць
def convert():
    try:
        value = float(amount_entry.get())  # Отримуємо введене значення
        from_unit = from_unit_var.get()  # Одиниця, з якої конвертуємо
        to_unit = to_unit_var.get()  # Одиниця, в яку конвертуємо

        # Визначаємо коефіцієнти для конвертації
        conversion_factors = {
            # Маса
            'gram': 1, 'kilogram': 1000, 'ton': 1000000, 'milligram': 0.001,

            # Енергія
            'joule': 1, 'kilojoule': 1000,

            # Довжина
            'meter': 1, 'kilometer': 1000, 'mile': 1609.34, 'yard': 0.9144,

            # Час
            'second': 1, 'minute': 60, 'hour': 3600, 'day': 86400, 'year': 31536000,

            # Швидкість
            'm/s': 1, 'km/h': 1000 / 3600, 'mph': 1609.34 / 3600,

            # Площа
            'square_meter': 1, 'hectar': 10000, 'acre': 4046.86,

            # Об'єм
            'liter': 1, 'cubic_meter': 1000, 'gallon': 3.78541, 'quart': 0.946353,

            # Температура (конвертується лише між Цельсієм, Фаренгейтом і Кельвіном)
            'celsius': 1, 'fahrenheit': 1, 'kelvin': 1,
        }

        # Якщо конвертація температури
        if from_unit == 'celsius' and to_unit == 'fahrenheit':
            result = (value * 9/5) + 32
        elif from_unit == 'celsius' and to_unit == 'kelvin':
            result = value + 273.15
        elif from_unit == 'fahrenheit' and to_unit == 'celsius':
            result = (value - 32) * 5/9
        elif from_unit == 'fahrenheit' and to_unit == 'kelvin':
            result = (value - 32) * 5/9 + 273.15
        elif from_unit == 'kelvin' and to_unit == 'celsius':
            result = value - 273.15
        elif from_unit == 'kelvin' and to_unit == 'fahrenheit':
            result = (value - 273.15) * 9/5 + 32
        else:
            # Для всіх інших одиниць
            result = (value * conversion_factors[from_unit]) / conversion_factors[to_unit]

        result_var.set(f"{value} {from_unit} = {result:.2f} {to_unit}")
    except ValueError:
        result_var.set("Помилка: Введіть правильне значення")

# Основне вікно
root = tk.Tk()
root.title("Конвертер одиниць вимірювання")
root.geometry("500x600")
root.config(bg="#333333")

# Оновлення результату
result_var = tk.StringVar()

# Титульна мітка
title_label = tk.Label(root, text="Конвертер одиниць", font=("Helvetica", 16, "bold"), fg="#ffffff", bg="#333333")
title_label.pack(pady=15)

# Поле для кількості значення
amount_label = tk.Label(root, text="Кількість:", font=("Helvetica", 12), fg="#ffffff", bg="#333333")
amount_label.pack(pady=5)
amount_entry = tk.Entry(root, font=("Helvetica", 14), bg="#f1f1f1", bd=2)
amount_entry.pack(pady=10)

# Меню для вибору одиниці, з якої конвертуємо
from_unit_var = tk.StringVar()
from_unit_var.set("gram")
from_unit_menu = tk.OptionMenu(root, from_unit_var,
                               'gram', 'kilogram', 'ton', 'milligram',
                               'joule', 'kilojoule',
                               'meter', 'kilometer', 'mile', 'yard',
                               'second', 'minute', 'hour', 'day', 'year',
                               'm/s', 'km/h', 'mph',
                               'square_meter', 'hectar', 'acre',
                               'liter', 'cubic_meter', 'gallon', 'quart',
                               'celsius', 'fahrenheit', 'kelvin')
from_unit_menu.config(font=("Helvetica", 12), fg="#333333", bg="#f1f1f1")
from_unit_menu.pack(pady=10)

# Меню для вибору одиниці, в яку конвертуємо
to_unit_var = tk.StringVar()
to_unit_var.set("kilogram")
to_unit_menu = tk.OptionMenu(root, to_unit_var,
                             'gram', 'kilogram', 'ton', 'milligram',
                             'joule', 'kilojoule',
                             'meter', 'kilometer', 'mile', 'yard',
                             'second', 'minute', 'hour', 'day', 'year',
                             'm/s', 'km/h', 'mph',
                             'square_meter', 'hectar', 'acre',
                             'liter', 'cubic_meter', 'gallon', 'quart',
                             'celsius', 'fahrenheit', 'kelvin')
to_unit_menu.config(font=("Helvetica", 12), fg="#333333", bg="#f1f1f1")
to_unit_menu.pack(pady=10)

# Кнопка для конвертації
convert_button = tk.Button(root, text="Конвертувати", command=convert, font=("Helvetica", 14, "bold"), fg="#ffffff", bg="#4caf50", bd=0, relief="flat")
convert_button.pack(pady=15)

# Мітка для результату
result_label = tk.Label(root, textvariable=result_var, font=("Helvetica", 14), fg="#ffffff", bg="#333333")
result_label.pack(pady=10)

# Запуск основного циклу
root.mainloop()


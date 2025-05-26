import tkinter as tk

# Функція для відкриття вікна конвертера валют
def open_currency_converter():
    # Вікно для конвертації валют
    converter_window = tk.Toplevel(root)
    converter_window.title("Конвертер валют")
    converter_window.geometry("500x500")

    # Курс валют (прикладні значення)
    exchange_rates = {
        'USD': 1,
        'UAH': 41,
        'EUR': 0.92,
        'GBP': 0.81,
        'JPY': 136.58,
        'AUD': 1.47,
        'CAD': 1.35,
        'CHF': 0.92,
        'CNY': 7.05,
        'INR': 82.58,
    }

    # Оновлення результату
    result_var = tk.StringVar()

    # Титульна мітка
    title_label = tk.Label(converter_window, text="Конвертер валют", font=("Helvetica", 16, "bold"), fg="#ffffff", bg="#333333")
    title_label.pack(pady=15)

    # Поле для кількості грошей
    amount_label = tk.Label(converter_window, text="Кількість:", font=("Helvetica", 12), fg="#ffffff", bg="#333333")
    amount_label.pack(pady=5)
    amount_entry = tk.Entry(converter_window, font=("Helvetica", 14), bg="#f1f1f1", bd=2)
    amount_entry.pack(pady=10)

    # Меню для вибору валюти з якої конвертуємо
    from_currency_var = tk.StringVar()
    from_currency_var.set("USD")
    from_currency_menu = tk.OptionMenu(converter_window, from_currency_var, *exchange_rates.keys())
    from_currency_menu.config(font=("Helvetica", 12), fg="#333333", bg="#f1f1f1")
    from_currency_menu.pack(pady=10)

    # Меню для вибору валюти в яку конвертуємо
    to_currency_var = tk.StringVar()
    to_currency_var.set("UAH")
    to_currency_menu = tk.OptionMenu(converter_window, to_currency_var, *exchange_rates.keys())
    to_currency_menu.config(font=("Helvetica", 12), fg="#333333", bg="#f1f1f1")
    to_currency_menu.pack(pady=10)

    # Функція для виконання конвертації
    def convert():
        try:
            amount = float(amount_entry.get())  # кількість грошей
            from_currency = from_currency_var.get()  # валюта з якої
            to_currency = to_currency_var.get()  # валюта в яку

            # Отримання курсів валют з словника
            from_rate = exchange_rates[from_currency]
            to_rate = exchange_rates[to_currency]

            # Обчислення суми в іншій валюті
            result = (amount / from_rate) * to_rate
            result_var.set(f"{amount} {from_currency} = {result:.2f} {to_currency}")
        except ValueError:
            result_var.set("Помилка: Введіть правильну кількість")

    # Кнопка для конвертації
    convert_button = tk.Button(converter_window, text="Конвертувати", command=convert, font=("Helvetica", 14, "bold"), fg="#ffffff", bg="#4caf50", bd=0, relief="flat")
    convert_button.pack(pady=15)

    # Мітка для результату
    result_label = tk.Label(converter_window, textvariable=result_var, font=("Helvetica", 14), fg="#ffffff", bg="#333333")
    result_label.pack(pady=10)

# Головне вікно для калькулятора
root = tk.Tk()
root.title("Конвертер валют")
root.geometry("480x700")  # Розмір вікна
root.config(bg="#333333")  # Темний фон
root.resizable(False, False)

# Кнопка для відкриття конвертера валют
currency_converter_button = tk.Button(
    root,
    text="Відкрити конвертер валют",
    font=("Helvetica", 14, "bold"),
    bg="#ff8c00",
    fg="#333333",
    command=open_currency_converter,
    relief="flat",
)
currency_converter_button.pack(pady=50)

root.mainloop()


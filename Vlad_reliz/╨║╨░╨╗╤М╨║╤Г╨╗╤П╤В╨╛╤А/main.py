import tkinter as tk

# Основне вікно калькулятора
def press(symbol):
    entry_var.set(entry_var.get() + str(symbol))

def evaluate():
    try:
        result = str(eval(entry_var.get()))
        entry_var.set(result)
    except ZeroDivisionError:
        entry_var.set("Помилка: Ділення на 0")
    except:
        entry_var.set("Помилка")

def clear():
    entry_var.set("")

def on_press(event):
    widget = event.widget
    widget.config(bg="#aaaaaa")

def on_release(event):
    widget = event.widget
    widget.config(bg=widget.original_bg)

# Функція для відкриття конвертера валют
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
    title_label = tk.Label(converter_window, text="Вибір валюти", font=("Helvetica", 16, "bold"), fg="#ffffff", bg="#333333")
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

# Функція для повернення до калькулятора
def open_calculator():
    calculator_frame.pack(fill="both", expand=True)
    currency_converter_button.pack_forget()

# Функція для відкриття конвертера з калькулятора
def open_currency_converter_from_calculator():
    calculator_frame.pack_forget()
    currency_converter_button.pack()

# Головне вікно для калькулятора
root = tk.Tk()
root.title("Калькулятор")
root.geometry("480x700")  # Розмір вікна
root.config(bg="#333333")  # Темний фон
root.resizable(False, False)

entry_var = tk.StringVar()

# Фрейм для калькулятора
calculator_frame = tk.Frame(root, bg="#333333")
calculator_frame.pack(fill="both", expand=True)

entry = tk.Entry(calculator_frame, textvariable=entry_var, font=("Helvetica", 30, "bold"), bg="#f1f1f1", fg="#333333", bd=0, justify="right")
entry.pack(fill="both", ipadx=8, ipady=30, pady=(10, 0))

buttons = [
    ["C", "(", ")", "%"],
    ["7", "8", "9", "/"],
    ["4", "5", "6", "*"],
    ["1", "2", "3", "-"],
    ["0", ".", "=", "+"],
]

# Функція для кнопок калькулятора
for row in buttons:
    frame = tk.Frame(calculator_frame, bg="#333333")
    frame.pack(expand=True, fill="both")
    for btn in row:
        if btn == "":
            tk.Label(frame, text="", bg="#333333").pack(side="left", expand=True, fill="both", padx=3, pady=3)
            continue

        if btn == "C":
            action = clear
        elif btn == "=":
            action = evaluate
        elif btn == "(" or btn == ")":
            action = lambda x=btn: press(x)
        elif btn == "%":
            action = lambda: entry_var.set(str(float(entry_var.get()) / 100))
        else:
            action = lambda x=btn: press(x)

        # Оформлення кнопок
        button = tk.Button(
            frame,
            text=btn,
            font=("Helvetica", 14, "bold"),
            fg="#333333",
            bg="#f1f1f1",
            activebackground="#d4d4d4",
            bd=2,
            relief="solid",
            width=5,
            height=2,
            command=action
        )

        button.original_bg = "#f1f1f1"
        button.bind("<ButtonPress>", on_press)
        button.bind("<ButtonRelease>", on_release)
        button.pack(side="left", expand=True, fill="both", padx=4, pady=4)

# Кнопка для відкриття конвертера валют
currency_converter_button = tk.Button(
    root,
    text="Конвертер валют",
    font=("Helvetica", 14, "bold"),
    bg="#ff8c00",
    fg="#333333",
    command=open_currency_converter_from_calculator,
    relief="flat",
)
currency_converter_button.pack(pady=10)

# Додаємо кнопку для повернення до калькулятора
switch_to_calculator_button = tk.Button(
    root,
    text="Калькулятор",
    font=("Helvetica", 14, "bold"),
    bg="#4caf50",
    fg="#fff",
    command=open_calculator,
    relief="flat",
)
switch_to_calculator_button.pack()

root.mainloop()


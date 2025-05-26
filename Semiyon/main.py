import tkinter as tk
from tkinter import ttk, messagebox
import requests

# Словник валют з їх назвами на українській мові
currency_names_uk = {
    "AUD": "Австралійський долар",
    "BGN": "Болгарський лев",
    "BRL": "Бразильський реал",
    "CAD": "Канадський долар",
    "CHF": "Швейцарський франк",
    "CNY": "Китайський юань",
    "CZK": "Чеська крона",
    "DKK": "Данська крона",
    "EUR": "Євро",
    "GBP": "Британський фунт",
    "HKD": "Гонконгський долар",
    "HRK": "Хорватська куна",
    "HUF": "Угорський форінт",
    "IDR": "Індонезійська рупія",
    "ILS": "Ізраїльський шекель",
    "INR": "Індійська рупія",
    "ISK": "Ісландська крона",
    "JPY": "Японська єна",
    "KRW": "Південнокорейська вона",
    "MXN": "Мексиканське песо",
    "MYR": "Малайзійський ринггіт",
    "NOK": "Норвезька крона",
    "NZD": "Новозеландський долар",
    "PHP": "Філіппінське песо",
    "PLN": "Польський злотий",
    "RON": "Румунський лей",
    "RUB": "Російський рубль",
    "SEK": "Шведська крона",
    "SGD": "Сінгапурський долар",
    "THB": "Тайський бат",
    "TRY": "Турецька ліра",
    "UAH": "Українська гривня",
    "USD": "Долар США",
    "ZAR": "Південноафриканський ренд"
}

# Зберігання історії
history = []

def get_currency_list():
    try:
        response = requests.get("https://api.frankfurter.app/currencies")
        response.raise_for_status()
        currencies = response.json()
        
        # Створюємо список у форматі "код валюти (назва українською)"
        currency_names = [f"{code} ({currency_names_uk.get(code, 'Невідома валюта')})" for code in currencies.keys()]
        return sorted(currency_names)  # Сортуємо за назвою
    except Exception as e:
        messagebox.showerror("Помилка", f"Не вдалося завантажити список валют.\n{e}")
        return []

def convert():
    try:
        amount = float(entry_amount.get())
    except ValueError:
        messagebox.showerror("Помилка", "Введіть правильну числову суму.")
        return

    from_curr_code = combo_from.get().split(" ")[0]  # Отримуємо тільки код валюти
    to_curr_code = combo_to.get().split(" ")[0]  # Отримуємо тільки код валюти

    if from_curr_code == to_curr_code:
        label_result.config(text=f"{amount} {from_curr_code} = {amount:.2f} {to_curr_code}")
        return

    url = f"https://api.frankfurter.app/latest?amount={amount}&from={from_curr_code}&to={to_curr_code}"

    try:
        response = requests.get(url)
        data = response.json()
        result = data['rates'][to_curr_code]
        
        # Зберігаємо історію конвертації
        history.append(f"{amount} {from_curr_code} = {result:.2f} {to_curr_code}")
        update_history()

        label_result.config(text=f"{amount} {from_curr_code} = {result:.2f} {to_curr_code}")
    except Exception as e:
        messagebox.showerror("Помилка", f"Помилка під час конвертації:\n{e}")

def update_history():
    # Оновлення списку історії на екран
    history_list.delete(0, tk.END)
    for item in history[-5:]:  # Покажемо останні 5 записів
        history_list.insert(tk.END, item)

# --- GUI ---
root = tk.Tk()
root.title("Конвертер валют (Frankfurter API)")
root.geometry("400x350")

tk.Label(root, text="Сума:").pack(pady=5)
entry_amount = tk.Entry(root)
entry_amount.pack()

tk.Label(root, text="З валюти:").pack()
combo_from = ttk.Combobox(root, state="readonly")
combo_from.pack()

tk.Label(root, text="У валюту:").pack()
combo_to = ttk.Combobox(root, state="readonly")
combo_to.pack()

tk.Button(root, text="Конвертувати", command=convert).pack(pady=10)
label_result = tk.Label(root, text="", font=("Arial", 12, "bold"))
label_result.pack()

# --- Завантаження валют ---
currency_list = get_currency_list()
combo_from['values'] = currency_list
combo_to['values'] = currency_list
combo_from.set("USD (Долар США)")
combo_to.set("EUR (Євро)")

# --- Історія конвертацій ---
history_label = tk.Label(root, text="Історія конвертацій:")
history_label.pack(pady=10)
history_list = tk.Listbox(root, height=5, width=50, border=0)
history_list.pack()
# Функція для показу пунктів обміну валют (фіксовані дані для прикладу)
def get_exchange_location(from_curr_code):
    # Для прикладу, можемо просто використовувати фіксовані пункти
    exchange_locations = {
        "USD": [("Київ, вул. Хрещатик, 10", "Обмін валют 24/7"),
                ("Львів, вул. Галицька, 45", "Кращий курс по місту")],
        "EUR": [("Одеса, вул. Дерибасівська, 12", "Обмін валют з вигідними курсами")],
        "UAH": [("Харків, вул. Сумська, 21", "Обмінний пункт біля метро")],
        # Додати інші валюти за потребою
    }
    
    # Повертаємо пункти обміну для конкретної валюти
    return exchange_locations.get(from_curr_code, [])

# Оновлюємо функцію конвертації, щоб показати місце для обміну
def convert():
    try:
        amount = float(entry_amount.get())
    except ValueError:
        messagebox.showerror("Помилка", "Введіть правильну числову суму.")
        return

    from_curr_code = combo_from.get().split(" ")[0]  # Отримуємо тільки код валюти
    to_curr_code = combo_to.get().split(" ")[0]  # Отримуємо тільки код валюти

    if from_curr_code == to_curr_code:
        label_result.config(text=f"{amount} {from_curr_code} = {amount:.2f} {to_curr_code}")
        return

    url = f"https://api.frankfurter.app/latest?amount={amount}&from={from_curr_code}&to={to_curr_code}"

    try:
        response = requests.get(url)
        data = response.json()
        result = data['rates'][to_curr_code]
        
        # Зберігаємо історію конвертації
        history.append(f"{amount} {from_curr_code} = {result:.2f} {to_curr_code}")
        update_history()

        # Показуємо результат
        label_result.config(text=f"{amount} {from_curr_code} = {result:.2f} {to_curr_code}")
        
        # Показуємо найближчий курс валют (приклад)
        show_best_exchange_rate(from_curr_code, to_curr_code)

        # Показуємо місце для обміну валют
        exchange_locations = get_exchange_location(from_curr_code)
        if exchange_locations:
            exchange_info = "\n".join([f"{loc[0]} - {loc[1]}" for loc in exchange_locations])
            exchange_location_label.config(text=f"Де обміняти валюту:\n{exchange_info}")
        else:
            exchange_location_label.config(text="Інформація про обмінні пункти відсутня.")

    except Exception as e:
        messagebox.showerror("Помилка", f"Помилка під час конвертації:\n{e}")

root.mainloop()

import tkinter as tk
import random

# Глобальні змінні
attempts = 0
max_attempts = None
player_wins = 0
computer_wins = 0
rounds_played = 0
secret_number = None
hint_count = 0
range_min = 1
range_max = 100
history_log = []
difficulty_label = "Легкий"

def generate_number():
    return random.randint(range_min, range_max)

def check_guess():
    global attempts, player_wins, computer_wins
    try:
        user_guess = int(guess_entry.get())
        attempts += 1

        if user_guess < secret_number:
            result_label.config(text="Занадто низько!", fg="#FF6347")
        elif user_guess > secret_number:
            result_label.config(text="Занадто високо!", fg="#FF6347")
        else:
            player_wins += 1
            result_label.config(text=f"Ви вгадали число {secret_number} за {attempts} спроб!", fg="#32CD32")
            log_history(True)
            increment_round()
            update_score()
            root.after(1000, reset_game)
            return

        if max_attempts is not None and attempts >= max_attempts:
            computer_wins += 1
            result_label.config(text=f"Спроби вичерпано! Це було {secret_number}", fg="#DC143C")
            log_history(False)
            increment_round()
            update_score()
            root.after(1500, reset_game)
    except ValueError:
        result_label.config(text="Введіть ціле число!", fg="#FF6347")

def set_difficulty(level):
    global max_attempts, difficulty_label
    if level == "easy":
        max_attempts = None
        difficulty_label = "Легкий"
    elif level == "medium":
        max_attempts = 10
        difficulty_label = "Середній"
    elif level == "hard":
        max_attempts = 5
        difficulty_label = "Важкий"
    reset_game()
    result_label.config(text=f"Обрано рівень: {difficulty_label}", fg="#1E90FF")

def reset_game():
    global secret_number, attempts, hint_count
    try:
        set_range = int(min_entry.get()), int(max_entry.get())
        if set_range[0] >= set_range[1]:
            result_label.config(text="Мінімум має бути менше за максимум!", fg="red")
            return
        global range_min, range_max
        range_min, range_max = set_range
    except ValueError:
        result_label.config(text="Невірний діапазон!", fg="red")
        return

    secret_number = generate_number()
    attempts = 0
    hint_count = 0
    guess_entry.delete(0, tk.END)
    hint_label.config(text="Підказка: —")
    guess_button.config(bg="#FFD700")

def update_score():
    score_label.config(text=f"Гравець: {player_wins} | Комп’ютер: {computer_wins}")

def increment_round():
    global rounds_played
    rounds_played += 1
    round_label.config(text=f"Раунд: {rounds_played}")

def animate_button():
    guess_button.config(bg="#FF4500")
    guess_button.after(300, lambda: guess_button.config(bg="#FFD700"))

def show_hint():
    global hint_count
    if hint_count >= 3 or secret_number is None:
        hint_label.config(text="Підказок більше немає.")
        return

    hint = ""
    if hint_count == 0:
        hint = "Парне" if secret_number % 2 == 0 else "Непарне"
    elif hint_count == 1:
        middle = (range_min + range_max) // 2
        hint = f"{'Менше' if secret_number < middle else 'Більше'} за середину ({middle})"
    elif hint_count == 2:
        if secret_number % 10 == 0:
            hint = "Ділиться на 10"
        elif secret_number % 5 == 0:
            hint = "Ділиться на 5"
        elif secret_number % 3 == 0:
            hint = "Ділиться на 3"
        else:
            hint = "Не ділиться на 3, 5 або 10"

    hint_count += 1
    hint_label.config(text=f"Підказка: {hint}")

def log_history(win):
    status = "Вгадано" if win else "Програш"
    entry = f"Раунд {rounds_played + 1}: {status} | Число: {secret_number} | Спроб: {attempts} | Рівень: {difficulty_label}"
    history_log.append(entry)

def show_history():
    history_window = tk.Toplevel(root)
    history_window.title("Історія ігор")
    history_window.geometry("500x400")
    history_window.config(bg="#1e1e1e")
    tk.Label(history_window, text="Історія раундів", font=("Arial", 16), fg="white", bg="#1e1e1e").pack(pady=10)

    history_text = tk.Text(history_window, font=("Arial", 12), bg="#f0f0f0", wrap=tk.WORD)
    history_text.pack(expand=True, fill=tk.BOTH, padx=10, pady=10)

    for entry in history_log:
        history_text.insert(tk.END, entry + "\n")

    history_text.config(state=tk.DISABLED)

# Вікно
root = tk.Tk()
root.title("Вгадай число")
root.geometry("640x700")
root.config(bg="#282828")

tk.Label(root, text="Вгадай число", font=("Arial", 22), fg="white", bg="#282828").pack(pady=10)

# Діапазон
range_frame = tk.Frame(root, bg="#282828")
tk.Label(range_frame, text="Діапазон від:", font=("Arial", 14), fg="white", bg="#282828").pack(side="left")
min_entry = tk.Entry(range_frame, width=5, font=("Arial", 14))
min_entry.insert(0, "1")
min_entry.pack(side="left", padx=5)

tk.Label(range_frame, text="до:", font=("Arial", 14), fg="white", bg="#282828").pack(side="left")
max_entry = tk.Entry(range_frame, width=5, font=("Arial", 14))
max_entry.insert(0, "100")
max_entry.pack(side="left", padx=5)
range_frame.pack(pady=5)

# Складність
difficulty_frame = tk.Frame(root, bg="#282828")
tk.Label(difficulty_frame, text="Рівень:", font=("Arial", 14), fg="white", bg="#282828").pack(side="left")

tk.Button(difficulty_frame, text="Легкий", font=("Arial", 12), bg="#7CFC00", command=lambda: set_difficulty("easy")).pack(side="left", padx=5)
tk.Button(difficulty_frame, text="Середній", font=("Arial", 12), bg="#FFD700", command=lambda: set_difficulty("medium")).pack(side="left", padx=5)
tk.Button(difficulty_frame, text="Важкий", font=("Arial", 12), bg="#FF6347", command=lambda: set_difficulty("hard")).pack(side="left", padx=5)
difficulty_frame.pack(pady=5)

# Ввід
guess_entry = tk.Entry(root, font=("Arial", 16), width=10)
guess_entry.pack(pady=10)

# Кнопки
guess_button = tk.Button(root, text="Перевірити", width=20, height=2, font=("Arial", 14),
                         bg="#FFD700", activebackground="#FF4500", command=lambda: [check_guess(), animate_button()])
guess_button.pack(pady=5)

tk.Button(root, text="Підказка", width=20, height=2, font=("Arial", 14),
          bg="#87CEEB", command=show_hint).pack(pady=5)

# Підказка
hint_label = tk.Label(root, text="Підказка: —", font=("Arial", 14), fg="#FFFFFF", bg="#282828")
hint_label.pack(pady=5)

# Результат
result_label = tk.Label(root, text="", font=("Arial", 16), fg="#FFFFFF", bg="#282828")
result_label.pack(pady=10)

# Статистика
score_label = tk.Label(root, text="Гравець: 0 | Комп’ютер: 0", font=("Arial", 14), fg="white", bg="#282828")
score_label.pack()

round_label = tk.Label(root, text="Раунд: 0", font=("Arial", 14), fg="white", bg="#282828")
round_label.pack()

# Кнопки управління
tk.Button(root, text="Скинути гру", width=20, height=2, font=("Arial", 14),
          bg="#FFD700", command=reset_game).pack(pady=5)

tk.Button(root, text="Показати історію", width=20, height=2, font=("Arial", 14),
          bg="#ADFF2F", command=show_history).pack(pady=5)

root.mainloop()
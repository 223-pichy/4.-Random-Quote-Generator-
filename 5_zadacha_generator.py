import tkinter as tk
from tkinter import ttk, messagebox
import random
import string
import json
from datetime import datetime

HISTORY_FILE = "history.json"

#  Функции работы с историей 
def load_history():
    try:
        with open(HISTORY_FILE, "r", encoding="utf-8") as f:
            return json.load(f)
    except (FileNotFoundError, json.JSONDecodeError):
        return []

def save_history(history):
    with open(HISTORY_FILE, "w", encoding="utf-8") as f:
        json.dump(history, f, ensure_ascii=False, indent=4)

def add_to_history(password, length, used_charsets):
    history = load_history()
    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    history.insert(0, {
        "timestamp": timestamp,
        "password": password,
        "length": length,
        "charsets": used_charsets
    })
    # Ограничим историю 50 записями
    if len(history) > 50:
        history = history[:50]
    save_history(history)
    refresh_history_table()

def refresh_history_table():
    for row in tree.get_children():
        tree.delete(row)
    history = load_history()
    for entry in history:
        tree.insert("", "end", values=(
            entry["timestamp"],
            entry["password"],
            entry["length"],
            entry["charsets"]
        ))

def clear_history():
    if messagebox.askyesno("Очистка истории", "Удалить всю историю паролей?"):
        save_history([])
        refresh_history_table()

#  Генерация пароля 
def generate_password():
    try:
        length = int(scale_length.get())
    except ValueError:
        length = 12

    password_type = []
    if var_letters.get():
        password_type.append(string.ascii_letters)
    if var_digits.get():
        password_type.append(string.digits)
    if var_symbols.get():
        password_type.append(string.punctuation)

    if not password_type:
        messagebox.showwarning("Внимание", "Выберите хотя бы один тип символов")
        return

    all_chars = ''.join(password_type)
    password = ''.join(random.choice(all_chars) for _ in range(length))
    entry_password.delete(0, tk.END)
    entry_password.insert(0, password)

    # Сохраняем в историю
    selected = []
    if var_letters.get():
        selected.append("буквы")
    if var_digits.get():
        selected.append("цифры")
    if var_symbols.get():
        selected.append("спецсимволы")
    charsets_str = ", ".join(selected)
    add_to_history(password, length, charsets_str)

def copy_to_clipboard():
    password = entry_password.get()
    if password:
        root.clipboard_clear()
        root.clipboard_append(password)
        messagebox.showinfo("Копирование", "Пароль скопирован в буфер обмена!")
    else:
        messagebox.showwarning("Нет пароля", "Сначала сгенерируйте пароль.")

#  Создание GUI 
root = tk.Tk()
root.title("Генератор паролей")
root.configure(bg="#f0f0f0")
root.geometry("650x550")
root.resizable(False, False)

# Ползунок длины пароля
tk.Label(root, text="Длина пароля:", bg="#f0f0f0").grid(row=0, column=0, padx=5, pady=5, sticky='w')
scale_length = tk.Scale(root, from_=4, to=32, orient=tk.HORIZONTAL, length=300)
scale_length.set(12)
scale_length.grid(row=0, column=1, columnspan=2, padx=5, pady=5, sticky='w')
label_length_value = tk.Label(root, text="12", bg="#f0f0f0")
label_length_value.grid(row=0, column=3, padx=5, pady=5)
scale_length.config(command=lambda v: label_length_value.config(text=str(int(float(v)))))

# Чекбоксы
var_letters = tk.BooleanVar(value=True)
var_digits = tk.BooleanVar(value=True)
var_symbols = tk.BooleanVar()

tk.Checkbutton(root, text="Буквы", variable=var_letters, bg="#f0f0f0").grid(row=1, column=0, sticky='w', padx=5, pady=5)
tk.Checkbutton(root, text="Цифры", variable=var_digits, bg="#f0f0f0").grid(row=1, column=1, sticky='w', padx=5, pady=5)
tk.Checkbutton(root, text="Символы", variable=var_symbols, bg="#f0f0f0").grid(row=1, column=2, sticky='w', padx=5, pady=5)

# Кнопка генерации
btn_generate = tk.Button(root, text="Сгенерировать", command=generate_password, bg="#4CAF50", fg="white", relief="raised")
btn_generate.grid(row=2, column=0, columnspan=4, pady=10)

# Поле для пароля и кнопка копирования
tk.Label(root, text="Пароль:", bg="#f0f0f0").grid(row=3, column=0, padx=5, pady=5, sticky='w')
entry_password = tk.Entry(root, width=35)
entry_password.grid(row=3, column=1, columnspan=2, padx=5, pady=5, sticky='w')
btn_copy = tk.Button(root, text="Копировать", command=copy_to_clipboard, bg="#05059A", fg="white")  
btn_copy.grid(row=3, column=3, padx=5, pady=5)

# Таблица истории (используем ttk.Treeview, т.к. это стандарт для таблиц)
tk.Label(root, text="История паролей:", bg="#f0f0f0", font=("Arial", 10, "bold")).grid(row=4, column=0, columnspan=4, sticky='w', padx=5, pady=(10,0))

columns = ("timestamp", "password", "length", "charsets")
tree = ttk.Treeview(root, columns=columns, show="headings", height=10)
tree.heading("timestamp", text="Дата и время")
tree.heading("password", text="Пароль")
tree.heading("length", text="Длина")
tree.heading("charsets", text="Использованные наборы")

tree.column("timestamp", width=140)
tree.column("password", width=200)
tree.column("length", width=60)
tree.column("charsets", width=150)

tree.grid(row=5, column=0, columnspan=4, padx=5, pady=5, sticky='nsew')

# Скроллбар для таблицы
scrollbar = ttk.Scrollbar(root, orient="vertical", command=tree.yview)
scrollbar.grid(row=5, column=4, sticky='ns')
tree.configure(yscrollcommand=scrollbar.set)

# Кнопка очистки истории
btn_clear = tk.Button(root, text="Очистить историю", command=clear_history, bg="#f44336", fg="white")
btn_clear.grid(row=6, column=0, columnspan=4, pady=10)

# Загружаем историю при старте
refresh_history_table()

root.mainloop()
import json
import random
import tkinter as tk
from tkinter import ttk, messagebox

DATA_FILE = "quotes_history.json"

#  База предопределённых цитат 
DEFAULT_QUOTES = [
    {"text": "Жиза, братан...", "author": "Пацанский мудрец", "theme": "Жиза"},
    {"text": "Лучше быть богатым и здоровым, чем бедным и больным", "author": "Народная", "theme": "Жизнь"},
    {"text": "Не ссы — прорвёмся!", "author": "Дворовый философ", "theme": "Мотивация"},
    {"text": "Деньги не главное, но без них никак", "author": "Реальный пацан", "theme": "Деньги"},
    {"text": "Кто не рискует, тот не пьёт шампанское", "author": "Автор неизвестен", "theme": "Риск"},
    {"text": "Базара нет — ты красавчик!", "author": "Братан", "theme": "Комплимент"},
    {"text": "Жизнь — как зебра: полоса белая, полоса чёрная", "author": "Мудрый двор", "theme": "Жизнь"},
    {"text": "Сила есть — ума не надо? Не, так не пойдёт", "author": "Пацанский учитель", "theme": "Учёба"},
    {"text": "Своих не бросаем", "author": "Братва", "theme": "Дружба"},
    {"text": "Тише едешь — дальше будешь", "author": "Классика", "theme": "Терпение"},
]

# Глобальные переменные
quotes = []              # список всех доступных цитат
history = []             # история сгенерированных цитат

#  Работа с JSON  
def load_history():
    global history
    try:
        with open(DATA_FILE, "r", encoding="utf-8") as f:
            history = json.load(f)
    except FileNotFoundError:
        history = []  # файла нет — пустая история
    except Exception as e:
        messagebox.showerror("Ошибка", f"Не удалось загрузить историю: {e}")
        history = []

def save_history():
    try:
        with open(DATA_FILE, "w", encoding="utf-8") as f:
            json.dump(history, f, ensure_ascii=False, indent=4)
    except Exception as e:
        messagebox.showerror("Ошибка", f"Не удалось сохранить историю: {e}")

#  Обновление фильтров 
def update_filter_authors():
    authors = sorted(set(q["author"] for q in quotes))
    authors.insert(0, "Все")
    author_filter_combo['values'] = authors
    if var_author.get() not in authors:
        var_author.set("Все")

def update_filter_themes():
    themes = sorted(set(q["theme"] for q in quotes))
    themes.insert(0, "Все")
    theme_filter_combo['values'] = themes
    if var_theme.get() not in themes:
        var_theme.set("Все")

#  Отображение истории 
def update_history_list():
    for row in history_tree.get_children():
        history_tree.delete(row)

    author_filter = var_author.get()
    theme_filter = var_theme.get()

    filtered = history[:]
    if author_filter != "Все":
        filtered = [h for h in filtered if h["author"] == author_filter]
    if theme_filter != "Все":
        filtered = [h for h in filtered if h["theme"] == theme_filter]

    for item in reversed(filtered):  # новые сверху
        history_tree.insert("", tk.END, values=(
            item["timestamp"],
            item["text"][:50] + ("..." if len(item["text"]) > 50 else ""),
            item["author"],
            item["theme"]
        ))

#  Генерация случайной цитаты 
def generate_quote():
    if not quotes:
        messagebox.showerror("Ошибка", "Нет доступных цитат")
        return

    quote = random.choice(quotes)

    # Отображение
    quote_label.config(text=f"📖 {quote['text']}\n\n— {quote['author']}")

    # Добавление в историю
    from datetime import datetime
    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    history.insert(0, {
        "text": quote["text"],
        "author": quote["author"],
        "theme": quote["theme"],
        "timestamp": timestamp
    })
    save_history()
    update_history_list()

#  Добавление новой цитаты 
def add_quote():
    text = new_text_entry.get().strip()
    author = new_author_entry.get().strip()
    theme = new_theme_entry.get().strip()

    if not text or not author or not theme:
        messagebox.showerror("Ошибка", "Заполните все поля (текст, автор, тема)")
        return

    quotes.append({"text": text, "author": author, "theme": theme})
    update_filter_authors()
    update_filter_themes()
    
    # Очистка полей
    new_text_entry.delete(0, tk.END)
    new_author_entry.delete(0, tk.END)
    new_theme_entry.delete(0, tk.END)
    
    messagebox.showinfo("Успех", "Цитата добавлена в библиотеку")

#  Применение фильтров 
def apply_filters():
    update_history_list()

def reset_filters():
    var_author.set("Все")
    var_theme.set("Все")
    update_history_list()

#  Очистка истории 
def clear_history():
    if messagebox.askyesno("Подтверждение", "Очистить всю историю?"):
        global history
        history = []
        save_history()
        update_history_list()
        messagebox.showinfo("Готово", "История очищена")

#  GUI 
root = tk.Tk()
root.title("Random Quote Generator — Пацанские цитаты")
root.geometry("850x650")
root.configure(bg="#f0f0f0")

# Загрузка данных
load_history()
quotes = DEFAULT_QUOTES.copy()  # копируем предопределённые цитаты

#  Верхняя панель: генерация 
frame_gen = ttk.LabelFrame(root, text=" Случайная цитата", padding=10)
frame_gen.pack(fill="x", padx=10, pady=5)

quote_label = tk.Label(frame_gen, text="Нажми «Сгенерировать»", font=("Arial", 12, "italic"),
                       bg="#f9f9f9", relief="groove", wraplength=700, justify="center")
quote_label.pack(fill="x", pady=5)

btn_gen = ttk.Button(frame_gen, text="Сгенерировать цитату", command=generate_quote)
btn_gen.pack(pady=5)

#  Добавление новой цитаты 
frame_add = ttk.LabelFrame(root, text=" Добавить свою цитату", padding=10)
frame_add.pack(fill="x", padx=10, pady=5)

ttk.Label(frame_add, text="Текст:").grid(row=0, column=0, sticky="e", padx=5)
new_text_entry = ttk.Entry(frame_add, width=50)
new_text_entry.grid(row=0, column=1, padx=5)

ttk.Label(frame_add, text="Автор:").grid(row=0, column=2, sticky="e", padx=5)
new_author_entry = ttk.Entry(frame_add, width=20)
new_author_entry.grid(row=0, column=3, padx=5)

ttk.Label(frame_add, text="Тема:").grid(row=0, column=4, sticky="e", padx=5)
new_theme_entry = ttk.Entry(frame_add, width=15)
new_theme_entry.grid(row=0, column=5, padx=5)

btn_add = ttk.Button(frame_add, text="Добавить цитату", command=add_quote)
btn_add.grid(row=0, column=6, padx=10)

#  Фильтры 
frame_filter = ttk.LabelFrame(root, text=" Фильтрация истории", padding=10)
frame_filter.pack(fill="x", padx=10, pady=5)

ttk.Label(frame_filter, text="Автор:").grid(row=0, column=0, padx=5)
var_author = tk.StringVar(value="Все")
author_filter_combo = ttk.Combobox(frame_filter, textvariable=var_author, width=20)
author_filter_combo.grid(row=0, column=1, padx=5)

ttk.Label(frame_filter, text="Тема:").grid(row=0, column=2, padx=5)
var_theme = tk.StringVar(value="Все")
theme_filter_combo = ttk.Combobox(frame_filter, textvariable=var_theme, width=15)
theme_filter_combo.grid(row=0, column=3, padx=5)

btn_filter = ttk.Button(frame_filter, text="Применить", command=apply_filters)
btn_filter.grid(row=0, column=4, padx=5)

btn_reset = ttk.Button(frame_filter, text="Сбросить", command=reset_filters)
btn_reset.grid(row=0, column=5, padx=5)

btn_clear = ttk.Button(frame_filter, text="Очистить историю", command=clear_history)
btn_clear.grid(row=0, column=6, padx=5)

#  История 
frame_history = ttk.LabelFrame(root, text=" История цитат", padding=5)
frame_history.pack(fill="both", expand=True, padx=10, pady=5)

columns = ("Время", "Цитата", "Автор", "Тема")
history_tree = ttk.Treeview(frame_history, columns=columns, show="headings", height=12)
history_tree.heading("Время", text="Время")
history_tree.heading("Цитата", text="Цитата")
history_tree.heading("Автор", text="Автор")
history_tree.heading("Тема", text="Тема")
history_tree.column("Время", width=130)
history_tree.column("Цитата", width=400)
history_tree.column("Автор", width=150)
history_tree.column("Тема", width=100)

scroll = ttk.Scrollbar(frame_history, orient="vertical", command=history_tree.yview)
history_tree.configure(yscrollcommand=scroll.set)
history_tree.pack(side="left", fill="both", expand=True)
scroll.pack(side="right", fill="y")

# Обновление фильтров и истории
update_filter_authors()
update_filter_themes()
update_history_list()

root.mainloop()
import json
import os
import tkinter as tk
from tkinter import ttk, messagebox

DATA_FILE = "movies.json"

#  Загрузка и сохранение 
def load_movies():
    if os.path.exists(DATA_FILE):
        with open(DATA_FILE, "r", encoding="utf-8") as f:
            return json.load(f)
    return []  # пустой список при первом запуске

def save_movies(movies):
    with open(DATA_FILE, "w", encoding="utf-8") as f:
        json.dump(movies, f, ensure_ascii=False, indent=4)

#  Основная логика 
def add_movie():
    title = entry_title.get().strip()
    genre = combo_genre.get().strip()
    year = entry_year.get().strip()
    rating = entry_rating.get().strip()

    if not title or not genre:
        messagebox.showerror("Ошибка", "Название и жанр обязательны")
        return

    try:
        year = int(year)
        if year < 1888 or year > 2100:
            raise ValueError
    except:
        messagebox.showerror("Ошибка", "Год должен быть целым числом (например, 1994)")
        return

    try:
        rating = float(rating)
        if not (0 <= rating <= 10):
            raise ValueError
    except:
        messagebox.showerror("Ошибка", "Рейтинг должен быть числом от 0 до 10")
        return

    # Добавление
    movies.append({"title": title, "genre": genre, "year": year, "rating": rating})
    save_movies(movies)
    update_display()
    clear_inputs()
    messagebox.showinfo("Успех", "Фильм добавлен")

def update_display():
    # Очистка таблицы
    for row in tree.get_children():
        tree.delete(row)

    # Получение фильтров
    filter_genre = var_genre.get()
    filter_year = entry_filter_year.get().strip()

    filtered = movies[:]
    if filter_genre != "Все":
        filtered = [m for m in filtered if m["genre"] == filter_genre]
    if filter_year:
        try:
            fy = int(filter_year)
            filtered = [m for m in filtered if m["year"] == fy]
        except:
            pass

    for m in filtered:
        tree.insert("", tk.END, values=(m["title"], m["genre"], m["year"], f"{m['rating']:.1f}"))

def update_genre_filter():
    genres = sorted(set(m["genre"] for m in movies))
    var_genre.set("Все")
    combo_filter['values'] = ["Все"] + genres

def clear_inputs():
    entry_title.delete(0, tk.END)
    combo_genre.set(combo_genre['values'][0] if combo_genre['values'] else "")
    entry_year.delete(0, tk.END)
    entry_rating.delete(0, tk.END)

def reset_filter():
    entry_filter_year.delete(0, tk.END)
    var_genre.set("Все")
    update_display()

#  GUI 
root = tk.Tk()
root.title("Movie Library (упрощённая)")
root.geometry("750x450")

# Данные
movies = load_movies()

# === Верхняя панель: добавление ===
frame_add = ttk.LabelFrame(root, text="Добавить фильм", padding=5)
frame_add.pack(fill="x", padx=10, pady=5)

ttk.Label(frame_add, text="Название:").grid(row=0, column=0, padx=5, pady=5)
entry_title = ttk.Entry(frame_add, width=25)
entry_title.grid(row=0, column=1, padx=5, pady=5)

ttk.Label(frame_add, text="Жанр:").grid(row=0, column=2, padx=5, pady=5)
combo_genre = ttk.Combobox(frame_add, values=["Драма", "Комедия", "Боевик", "Фантастика"], width=12)
combo_genre.grid(row=0, column=3, padx=5, pady=5)
combo_genre.current(0)

ttk.Label(frame_add, text="Год:").grid(row=0, column=4, padx=5, pady=5)
entry_year = ttk.Entry(frame_add, width=6)
entry_year.grid(row=0, column=5, padx=5, pady=5)

ttk.Label(frame_add, text="Рейтинг (0-10):").grid(row=0, column=6, padx=5, pady=5)
entry_rating = ttk.Entry(frame_add, width=5)
entry_rating.grid(row=0, column=7, padx=5, pady=5)

btn_add = ttk.Button(frame_add, text="Добавить", command=add_movie)
btn_add.grid(row=0, column=8, padx=10, pady=5)

# === Панель фильтрации ===
frame_filter = ttk.LabelFrame(root, text="Фильтрация", padding=5)
frame_filter.pack(fill="x", padx=10, pady=5)

ttk.Label(frame_filter, text="Жанр:").grid(row=0, column=0, padx=5)
var_genre = tk.StringVar(value="Все")
combo_filter = ttk.Combobox(frame_filter, textvariable=var_genre, width=12)
combo_filter.grid(row=0, column=1, padx=5)
ttk.Label(frame_filter, text="Год:").grid(row=0, column=2, padx=5)
entry_filter_year = ttk.Entry(frame_filter, width=6)
entry_filter_year.grid(row=0, column=3, padx=5)
btn_filter = ttk.Button(frame_filter, text="Применить", command=update_display)
btn_filter.grid(row=0, column=4, padx=5)
btn_reset = ttk.Button(frame_filter, text="Сброс", command=reset_filter)
btn_reset.grid(row=0, column=5, padx=5)

# === Таблица ===
columns = ("Название", "Жанр", "Год", "Рейтинг")
tree = ttk.Treeview(root, columns=columns, show="headings", height=12)
tree.heading("Название", text="Название")
tree.heading("Жанр", text="Жанр")
tree.heading("Год", text="Год")
tree.heading("Рейтинг", text="Рейтинг")
tree.column("Название", width=250)
tree.column("Жанр", width=120)
tree.column("Год", width=80, anchor="center")
tree.column("Рейтинг", width=80, anchor="center")
tree.pack(fill="both", expand=True, padx=10, pady=5)

# === Обновление фильтров и отображения ===
update_genre_filter()
update_display()

root.mainloop()
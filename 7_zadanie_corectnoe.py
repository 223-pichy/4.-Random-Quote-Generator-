from tkinter import *
import json
from datetime import datetime

window = Tk()
window.title("Weather Diary")
window.geometry("1200x950")
window.configure(bg="#f0f0f0")

all_entries = []  # Список словарей с записями


def add_item():
    #Добавление новой записи с проверками
    date_str = date_entry.get().strip()
    temp_str = temp_entry.get().strip()
    desc = desk_entry.get().strip()
    precip_str = osadki_entry.get().strip().lower()

    if not date_str or not temp_str or not desc or not precip_str:
        res.config(text="Заполните все поля!", fg="red")
        return

    try:
        datetime.strptime(date_str, "%d.%m.%Y")
    except ValueError:
        res.config(text="Неверный формат даты! Используйте ДД.ММ.ГГГГ", fg="red")
        return

    try:
        temp = int(temp_str)
    except ValueError:
        res.config(text="Температура должна быть целым числом!", fg="red")
        return

    if precip_str not in ("да", "нет"):
        res.config(text="Осадки: введите 'да' или 'нет'", fg="red")
        return

    entry = {
        "date": date_str,
        "temp": temp,
        "description": desc,
        "precipitation": precip_str
    }
    all_entries.append(entry)
    show_all()
    # Очистка полей
    date_entry.delete(0, END)
    temp_entry.delete(0, END)
    desk_entry.delete(0, END)
    osadki_entry.delete(0, END)
    res.config(text="Запись добавлена!", fg="green")

def display_entries(entries):
    #Отображение списка записей в Listbox
    lb.delete(0, END)
    for e in entries:
        line = f"{e['date']} | {e['temp']}°C | {e['description']} | {e['precipitation']}"
        lb.insert(END, line)

def show_all():
    #Показать все записи (сброс фильтров)
    display_entries(all_entries)
    res.config(text="Показаны все записи", fg="green")

def filter_temp_above():
    #Фильтр: температура >= заданного значения
    try:
        threshold = int(filter_entry.get())
        filtered = [e for e in all_entries if e['temp'] >= threshold]
        display_entries(filtered)
        res.config(text=f"Найдено {len(filtered)} записей с температурой >= {threshold}°C", 
                   fg="green" if filtered else "red")
    except ValueError:
        res.config(text="Введите число для фильтрации!", fg="red")

def filter_temp_below():
    #Фильтр: температура <= заданного значения
    try:
        threshold = int(filter_entry.get())
        filtered = [e for e in all_entries if e['temp'] <= threshold]
        display_entries(filtered)
        res.config(text=f"Найдено {len(filtered)} записей с температурой <= {threshold}°C", 
                   fg="green" if filtered else "red")
    except ValueError:
        res.config(text="Введите число для фильтрации!", fg="red")

def filter_by_date():
    #Фильтр по дате (точное совпадение)"
    date_str = date_filter_entry.get().strip()
    if not date_str:
        res.config(text="Введите дату для фильтрации", fg="red")
        return
    try:
        datetime.strptime(date_str, "%d.%m.%Y")
    except ValueError:
        res.config(text="Неверный формат даты! Используйте ДД.ММ.ГГГГ", fg="red")
        return
    filtered = [e for e in all_entries if e['date'] == date_str]
    display_entries(filtered)
    res.config(text=f"Найдено {len(filtered)} записей за {date_str}", 
               fg="green" if filtered else "red")

def save_to_json():
    #Сохранить все записи в JSON-файл
    try:
        with open("weather_diary.json", "w", encoding="utf-8") as f:
            json.dump(all_entries, f, ensure_ascii=False, indent=4)
        res.config(text="Сохранено в weather_diary.json", fg="green")
    except Exception as e:
        res.config(text=f"Ошибка сохранения: {e}", fg="red")

def load_from_json():
   # Загрузить записи из JSON-файла
    global all_entries
    try:
        with open("weather_diary.json", "r", encoding="utf-8") as f:
            all_entries = json.load(f)
        show_all()
        res.config(text="Загружено из weather_diary.json", fg="green")
    except FileNotFoundError:
        res.config(text="Файл weather_diary.json не найден", fg="red")
    except Exception as e:
        res.config(text=f"Ошибка загрузки: {e}", fg="red")


# Заголовок
Label(window, text="Weather Diary", font="Arial 24 bold", bg="#f0f0f0", fg="#333333").place(x=500, y=20)

# Поля ввода
Label(window, text="Дата (ДД.ММ.ГГГГ)", font="Arial 14", bg="#f0f0f0").place(x=50, y=100)
date_entry = Entry(window, font="Arial 14", width=25, bg="white", relief="solid")
date_entry.place(x=50, y=130)

Label(window, text="Температура (°C)", font="Arial 14", bg="#f0f0f0").place(x=50, y=180)
temp_entry = Entry(window, font="Arial 14", width=25, bg="white", relief="solid")
temp_entry.place(x=50, y=210)

Label(window, text="Описание", font="Arial 14", bg="#f0f0f0").place(x=50, y=260)
desk_entry = Entry(window, font="Arial 14", width=25, bg="white", relief="solid")
desk_entry.place(x=50, y=290)

Label(window, text="Осадки (да/нет)", font="Arial 14", bg="#f0f0f0").place(x=50, y=340)
osadki_entry = Entry(window, font="Arial 14", width=25, bg="white", relief="solid")
osadki_entry.place(x=50, y=370)

Button(window, text="Добавить запись", font="Arial 14", command=add_item, bg="#4CAF50", fg="white", relief="raised", padx=10, pady=5).place(x=50, y=430)

res = Label(window, font="Arial 10", fg="red", text="", bg="#f0f0f0")
res.place(x=50, y=490)

# Фильтр по температуре
Label(window, text="Фильтр по температуре", font="Arial 16 bold", bg="#f0f0f0", fg="#333333").place(x=50, y=540)
filter_entry = Entry(window, font="Arial 14", width=15, bg="white", relief="solid")
filter_entry.place(x=50, y=580)
Button(window, text="ВЫШЕ", font="Arial 12", command=filter_temp_above, bg="#2196F3", fg="white", width=10).place(x=50, y=620)
Button(window, text="НИЖЕ", font="Arial 12", command=filter_temp_below, bg="#2196F3", fg="white", width=10).place(x=160, y=620)
Button(window, text="ПОКАЗАТЬ ВСЕ", font="Arial 12", command=show_all, bg="#FF9800", fg="white", width=12).place(x=50, y=660)

# Фильтр по дате
Label(window, text="Фильтр по дате", font="Arial 16 bold", bg="#f0f0f0", fg="#333333").place(x=50, y=710)
date_filter_entry = Entry(window, font="Arial 14", width=25, bg="white", relief="solid")
date_filter_entry.place(x=50, y=740)
Button(window, text="Фильтр по дате", font="Arial 12", command=filter_by_date,
       bg="#BDB76B", fg="white", width=15).place(x=50, y=780)

# Сохранение / загрузка
Button(window, text="Сохранить в JSON", font="Arial 12", command=save_to_json,
       bg="#607D8B", fg="white", width=15).place(x=50, y=830)
Button(window, text="Загрузить из JSON", font="Arial 12", command=load_from_json,
       bg="#607D8B", fg="white", width=15).place(x=50, y=870)

# Список записей
lb = Listbox(window, font="Arial 12", width=70, height=30, bg="white", relief="solid", selectbackground="#4CAF50")
lb.place(x=400, y=80)

window.mainloop()
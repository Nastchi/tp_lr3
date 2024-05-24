import tkinter as tk
from tkinter import simpledialog
import pandas as pd
from matplotlib import pyplot as plt

filename = 'running_data.xlsx'
data = pd.read_excel(filename, header=0)


# Функция для открытия и отображения файла с данными о пробежках
def select_file():
    global data
    info_window = tk.Toplevel(root)
    info_window.title("Информация о пробежках")
    info_window.geometry("1300x500")
    info_table = tk.Text(info_window, height=30, width=200)
    info_table.insert(tk.END, data.to_string(index=False))
    info_table.pack()


# Функция для построения графиков зависимости расстояния и длительности пробежки от дня
def plot_data():
    global data
    data['День'] = range(1, len(data) + 1)
    plt.figure(figsize=(14, 8))

    plt.subplot(2, 1, 1)
    plt.plot(data['День'], data['Пройденное расстояние (км)'], marker='o', color='green')
    plt.title('Пройденное расстояние от дня')
    plt.xlabel('День')
    plt.ylabel('Расстояние (км)')

    plt.subplot(2, 1, 2)
    plt.plot(data['День'], data['Длительность бега (мин)'], marker='o', color='purple')
    plt.title('Длительность бега от дня')
    plt.xlabel('День')
    plt.ylabel('Длительность (мин)')

    plt.tight_layout()
    plt.show()


# Функция для вычисления суммы пройденных км за все выходные дни
def calculate_weekend_distance():
    global data
    data['Дата'] = pd.to_datetime(data['Дата'])
    weekend_data = data[data['Дата'].dt.dayofweek >= 5]
    total_weekend_distance = weekend_data['Пройденное расстояние (км)'].sum()

    result_window = tk.Toplevel(root)
    result_window.title("Сумма пройденных км за выходные")
    result_window.geometry("300x100")
    result_label = tk.Label(result_window, text=f"Сумма пройденных км за выходные: {total_weekend_distance:.2f} км")
    result_label.pack()


# Функция для прогнозирования расстояния методом скользящей средней
def forecast_distance():
    global data
    N = simpledialog.askinteger("Ввод", "Введите количество дней, на которые нужно сделать прогноз:", minvalue=1)
    M = simpledialog.askinteger("Ввод", "Введите количество дней для нахождения средней:", minvalue=2)
    if N is None:
        return

    data['День'] = range(1, len(data) + 1)
    plt.figure(figsize=(14, 8))

    plt.plot(data['День'], data['Пройденное расстояние (км)'], marker='o', label='Фактические данные', color='green')

    forecast_days = range(len(data) + 1, len(data) + N + 1)
    forecast_values = []

    for i in range(N):
        forecast_value = data['Пройденное расстояние (км)'].rolling(window=M).mean().iloc[-1]
        forecast_values.append(forecast_value)
        new_row = pd.DataFrame({'Дата': [data['Дата'].iloc[-1] + pd.Timedelta(days=i + 1)],
                                'Пройденное расстояние (км)': [forecast_value]})
        data = pd.concat([data, new_row], ignore_index=True)

    plt.plot(forecast_days, forecast_values, label='Прогноз', marker='o', color='purple')

    plt.xlabel('День')
    plt.ylabel('Расстояние (км)')
    plt.title('Прогноз расстояния на следующие N дней')
    plt.legend()
    plt.show()

# Графический интерфейс
root = tk.Tk()
root.title("Данные о пробежках")
root.geometry("300x350")
root.configure(bg='#98befa')

title_label = tk.Label(root, text="Данные о пробежках", font=("Arial", 16, "bold"), fg='#03142e', bg='#98befa')
title_label.pack(pady=20)

file_button = tk.Button(root, text="Открыть таблицу", command=select_file, font=("Arial", 10, "bold"), fg='#03142e',
                        bg='#E6E6FA', width=29, height=2)
diagram_button = tk.Button(root, text='Показать графики', command=plot_data, font=("Arial", 10, "bold"), fg='#03142e',
                           bg='#E6E6FA', width=30, height=2)
weekend_button = tk.Button(root, text='Сумма км за выходные', command=calculate_weekend_distance,
                           font=("Arial", 10, "bold"), fg='#03142e', bg='#E6E6FA', width=29, height=2)
forecast_button = tk.Button(root, text='Прогноз', command=forecast_distance,
                            font=("Arial", 10, "bold"), fg='#03142e', bg='#E6E6FA', width=29, height=2)

file_button.pack(padx=10, pady=10)
diagram_button.pack(padx=30, pady=10)
weekend_button.pack(padx=20, pady=10)
forecast_button.pack(padx=20, pady=10)

root.mainloop()

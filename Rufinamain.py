from tkinter import simpledialog
import pandas as pd
from matplotlib import pyplot as plt
import tkinter as tk

filename = 'infections.xlsx'
data = pd.read_excel(filename, header=0)


# Функция для открытия и отображения файла с данными об инфекциях
def select_file():
    global data
    info_window = tk.Toplevel(root)
    info_window.title("Информация об инфекциях")
    info_window.geometry("1300x500")
    info_table = tk.Text(info_window, height=30, width=600)
    info_table.insert(tk.END, data.to_string(index=False))
    info_table.pack()


# Функция для построения графиков заболеваемости
def plot_data():
    global data
    data['Год'] = data['Дата'].dt.year
    plt.figure(figsize=(14, 16))

    plt.subplot(3, 2, 1)
    plt.plot(data['Год'], data['Бешенство'], marker='o')
    plt.title('Заболевшие от бешенства')
    plt.xlabel('Год')
    plt.ylabel('Количество заболевших в год')

    plt.subplot(3, 2, 3)
    plt.plot(data['Год'], data['Клещевой энцефалит'], marker='o', color='pink')
    plt.title('Заболевшие от клещей')
    plt.xlabel('Год')
    plt.ylabel('Количество заболевших в год')

    plt.subplot(3, 2, 2)
    plt.plot(data['Год'], data['Туберкулёз'], marker='o', color='yellow')
    plt.title('Заболевшие от туберы')
    plt.xlabel('Год')
    plt.ylabel('Количество заболевших в год')

    plt.subplot(3, 2, 5)
    plt.plot(data['Год'], data['СПИД'], marker='o', color='purple')
    plt.title('Заболевшие от ужасных половых отношений')
    plt.xlabel('Год')
    plt.ylabel('Количество заболевших в год')

    plt.subplot(3, 2, 6)
    plt.plot(data['Год'], data['Сифилис'], marker='o', color='blue')
    plt.title('Заболевшие от сифака')
    plt.xlabel('Год')
    plt.ylabel('Количество заболевших в год')

    plt.tight_layout()
    plt.show()


# Функция для вычисления с наибольшими и наименьшими снижениями заболеваемости
def calculate_infection_decrease():
    global data
    # Вычисляем суммарное количество заболевших каждой инфекцией за все годы
    infections = data.iloc[:, 1:]  # Выбираем все столбцы с данными о заболеваниях (кроме столбца с годами)
    total_infections = infections.sum()

    # Считаем изменение заболеваемости каждой инфекции за 15 лет
    initial_year_infections = infections.iloc[0]  # Заболеваемость каждой инфекции в начальном году
    final_year_infections = infections.iloc[-1]  # Заболеваемость каждой инфекции в последнем году

    infection_change = final_year_infections - initial_year_infections

    # Находим инфекцию, снижение заболеваемости которой было наибольшим и наименьшим
    max_decrease_infection = infection_change.idxmin()  # Инфекция с наибольшим снижением заболеваемости
    min_decrease_infection = infection_change.idxmax()  # Инфекция с наименьшим снижением заболеваемости

    # Выводим результаты
    result_window = tk.Toplevel(root)
    result_window.title("Изменение заболеваемости за 15 лет")
    result_window.geometry("400x150")
    result_label1 = tk.Label(result_window,
    text=f"Инфекция с наибольшим снижением заболеваемости: {max_decrease_infection}")
    result_label1.pack()
    result_label2 = tk.Label(result_window,
    text=f"Инфекция с наименьшим снижением заболеваемости: {min_decrease_infection}")
    result_label2.pack()

# Функция для прогнозирования расстояния методом скользящей средней
def forecast_distance():
    global data
    N = simpledialog.askinteger("Ввод", "Введите количество лет для прогнозирования:", minvalue=1)
    if N is None:
        return

    last_date = data['Дата'].iloc[-1]
    plt.figure(figsize=(8, 8))

    plt.plot(data['Дата'], data['СПИД'], marker='o', label='Фактические данные')

    forecast_dates = pd.date_range(start=last_date, periods=N * 365, freq='D')
    forecast_values = []

    for i in range(N* 365):
        forecast_value = data['СПИД'].rolling(window=5).mean().iloc[-1]
        forecast_values.append(forecast_value)
        new_row = pd.DataFrame({'Год': [data['Дата'].iloc[-1] + pd.Timedelta(days=i + 1)],
                                'СПИД': [forecast_value]})
        data = pd.concat([data, new_row], ignore_index=True)

    plt.plot(forecast_dates, forecast_values, 'r--', label='Прогноз')

    plt.xlabel('Год')
    plt.ylabel('Заболевших от СПИДа')
    plt.title('Прогноз инфекции на следующие N лет')
    plt.legend()
    plt.show()

# Графический интерфейс
root = tk.Tk()
root.title("Информация об инфекциях")
root.geometry("300x350")
root.configure(bg='#e8b3ee')

title_label = tk.Label(root, text="Информация об инфекциях", font=("Arial", 15, "bold"), fg='#80005b', bg='#e8b3ee')
title_label.pack(pady=20)

file_button = tk.Button(root, text="Открыть таблицу", command=select_file, font=("Arial", 10, "bold"), fg='#80005b',
                        bg='#f9ebf7', width=20, height=2)
diagram_button = tk.Button(root, text='Показать графики', command=plot_data, font=("Arial", 10, "bold"), fg='#80005b',
                           bg='#f9ebf7', width=20, height=2)
weekend_button = tk.Button(root, text='Самые жесткие и не оч инфекции', command=calculate_infection_decrease,
                           font=("Arial", 10, "bold"), fg='#80005b', bg='#f9ebf7', width=30, height=2)
forecast_button = tk.Button(root, text='Прогноз на следующие N лет', command=forecast_distance,
                            font=("Arial", 10, "bold"), fg='#80005b', bg='#f9ebf7', width=30, height=2)

file_button.pack(padx=10, pady=10)
diagram_button.pack(padx=30, pady=10)
weekend_button.pack(padx=20, pady=10)
forecast_button.pack(padx=20, pady=10)

root.mainloop()
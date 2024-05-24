import tkinter as tk
import pandas as pd
from matplotlib import pyplot as plt

filename = 'populationshort.xlsx'
sheetname = 'Население по субъектам'
data = pd.read_excel(filename, sheet_name=sheetname, header=0)


# Загрузка данных из файла Excel и вывод в окно
def select_file():
    info_window = tk.Toplevel(root)
    info_window.title("Информация из файла")
    info_window.geometry("1300x500")
    info_table = tk.Text(info_window, height=30, width=200)
    info_table.insert(tk.END, data.to_string(index=False))
    info_table.pack()


# Построение графиков для каждого субъекта
def DiagramData():
    plt.figure(figsize=(14, 8))
    for index, row in data.iterrows():
        years = row.index[1:]
        populations = row[1:]
        plt.plot(years, populations, label=row[0])
    plt.legend(loc='upper left', bbox_to_anchor=(1, 1))
    plt.xlabel('Год')
    plt.ylabel('Численность населения')
    plt.title('Динамика численности населения по субъектам РФ')
    plt.show()


# Поиск субъекта с наибольшим снижением численности населения
def PopulationData():
    data['Разница'] = data['2022 г.'] - data['2008 г.']
    data_sorted = data.sort_values(by='Разница', ascending=True)
    max_difference_subject = data_sorted.iloc[0]['Субъекты РФ/Год']
    difference_2008_2022 = data_sorted.iloc[0]['Разница']
    result_window = tk.Toplevel(root)
    result_window.title("Результаты")
    result_window.geometry("500x100")
    result_label = tk.Label(result_window,
                            text=f"Субъект РФ с наибольшим снижением численности населения: {max_difference_subject}\nРазница населения между 2008 и 2022 годами: {difference_2008_2022}")
    result_label.pack()


# Прогнозирование методом скользящей средней и построение графиков
def ForecastData():
    N = 5  # Количество лет для прогнозирования
    plt.figure(figsize=(14, 8))

    for index, row in data.iterrows():
        years = list(row.index[1:])
        populations = list(row.iloc[1:])  # Используем .iloc для правильного доступа по позиции
        plt.plot(years, populations, label=row[0])

        # Прогнозирование
        forecast_years = [str(int(years[-1][:4]) + i) + " г." for i in range(1, N + 1)]
        forecast_values = []
        for i in range(N):
            forecast_values.append(sum(populations[-5:]) / 5)
            populations.append(forecast_values[-1])

        plt.plot(forecast_years, forecast_values, '--', label=f'{row[0]} (прогноз)')

    plt.legend(loc='upper left', bbox_to_anchor=(1, 1))
    plt.xlabel('Год')
    plt.ylabel('Численность населения')
    plt.title('Прогноз численности населения по субъектам РФ')
    plt.show()


# Графический интерфейс
root = tk.Tk()
root.title("Data about population")
root.geometry("300x350")
root.configure(bg='#b68cf5')  # Задаем цвет фона

title_label = tk.Label(root, text="Население России", font=("Arial", 16, "bold"), fg='#120121', bg='#b68cf5')
title_label.pack(pady=20)



file_button = tk.Button(root, text="Открыть таблицу", command=select_file, font=("Arial", 10, "bold"),fg='#120121', bg='#E6E6FA',width=20,height=2)
diagram_button = tk.Button(root, text='Показать диаграмму', command=DiagramData,font=("Arial", 10, "bold"),fg='#120121', bg='#E6E6FA',width=20,height=2)
result_button = tk.Button(root, text='Наибольшее снижение численности', command=PopulationData,font=("Arial", 10, "bold"),fg='#120121', bg='#E6E6FA',width=30,height=2)
forecast_button = tk.Button(root, text='Прогноз на следующие N лет', command=ForecastData,font=("Arial", 10, "bold"),fg='#120121', bg='#E6E6FA',width=30,height=2)


file_button.pack(padx=10, pady=10)
diagram_button.pack(padx=30, pady=10)
result_button.pack(padx=20, pady=10)
forecast_button.pack(padx=20, pady=10)


root.mainloop()
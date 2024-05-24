import tkinter as tk
import pandas as pd
from matplotlib import pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
filename = 'populationshort.xlsx'
sheetname = 'Население по субъектам'
data = pd.read_excel(filename, sheet_name=sheetname, header=0)


# вывод данных
def select_file():
    info_window = tk.Toplevel(root)
    info_window.title("Data from file")
    info_window.geometry("1300x200")
    info_window.configure(bg='#D3D3D3')
    info_table = tk.Text(info_window, height=30, width=200, bg='#E6E6FA')
    info_table.insert(tk.END, data.to_string(index=False))
    info_table.pack()

# Построение графиков для каждого субъекта
def DiagramData():
    fig = plt.figure(figsize=(10, 6))  # Уменьшаем размер окна для графика
    fig.patch.set_facecolor('#E6E6FA')  # Установка цвета фона для всего окна
    for index, row in data.iterrows():
        years = row.index[1:]
        populations = row[1:]
        plt.plot(years, populations, label=row[0])
    plt.legend(loc='lower left')
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
    result_window.title("Results")
    result_window.geometry("800x100")  # Изменение размеров окна на 600x150 пикселей
    result_window.configure(bg='#E6E6FA')  # Установка цвета фона окна
    result_label = tk.Label(result_window,
                            text=f"Субъект РФ с наибольшим снижением численности населения: {max_difference_subject}\nРазница населения между 2008 и 2022 годами: {difference_2008_2022}",
                            bg='#E6E6FA',  # Установка цвета фона для метки
                            font=("Arial", 12),  # Изменение размера шрифта
                            fg='#120121')  # Установка цвета текста
    result_label.pack()

# Прогнозирование методом скользящей средней и построение графиков
def ForecastData():
    def calculate_forecast():
        years = int(years_var.get())

        forecast_window = tk.Toplevel(root)
        forecast_window.title(f"Прогноз на {years} лет")
        forecast_window.geometry("800x600")
        forecast_window.configure(bg='#E6E6FA')

        fig = plt.figure(figsize=(10, 6))
        fig.patch.set_facecolor('#E6E6FA')
        for index, row in data.iterrows():
            population_values = row.iloc[1:].values.astype(float)
            years_list = list(row.index[1:])

            if len(population_values) >= years:
                forecast_values = []
                for i in range(len(population_values) - years + 1):
                    forecast = sum(population_values[i:i + years]) / years
                    forecast_values.append(forecast)

                forecast_years = years_list[-len(forecast_values):]
                plt.plot(forecast_years, forecast_values, '--', label=f'{row[0]} (прогноз)')

        plt.legend(loc='lower left')
        plt.xlabel('Год')
        plt.ylabel('Численность населения')
        plt.title(f'Прогноз численности населения по субъектам РФ на {years} лет')

        canvas = FigureCanvasTkAgg(fig, master=forecast_window)
        canvas.draw()
        canvas.get_tk_widget().pack(fill=tk.BOTH, expand=True)

        year_selection_window.destroy()

    year_selection_window = tk.Toplevel(root)
    year_selection_window.title("Выберите количество лет для прогноза")
    year_selection_window.geometry("400x300")
    year_selection_window.configure(bg='#E6E6FA')

    years_var = tk.StringVar(value="5")

    tk.Label(year_selection_window, text="Выберите количество лет для прогноза:", bg='#E6E6FA',
             font=("Arial", 12)).pack(pady=10)
    for val in [3, 5, 7, 10]:
        tk.Radiobutton(year_selection_window, text=f"{val} лет", variable=years_var, value=str(val), bg='#E6E6FA',
                       font=("Arial", 12)).pack(anchor=tk.W)

    ok_button = tk.Button(year_selection_window, text="OK", command=calculate_forecast, font=("Arial", 10, "bold"),
                          fg='#120121', bg='#E6E6FA', width=20, height=2)
    ok_button.pack(pady=20)

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
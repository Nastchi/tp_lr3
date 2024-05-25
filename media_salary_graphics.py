# -*- coding: utf-8 -*-

import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

def load_data(file_path):
    return pd.read_csv(file_path)

def display_data(data):
    print(data)

def plot_data(data, forecast_years):
    plt.figure(figsize=(14, 7))

    plt.subplot(2, 1, 1)
    plt.plot(data['Year'], data['Male_Salary'], label='Male Salary')
    plt.title('Median Salary for Men in Russia')
    plt.xlabel('Year')
    plt.ylabel('Salary')
    plt.legend()

    plt.subplot(2, 1, 2)
    plt.plot(data['Year'], data['Female_Salary'], label='Female Salary')
    plt.title('Median Salary for Women in Russia')
    plt.xlabel('Year')
    plt.ylabel('Salary')
    plt.legend()

    plt.tight_layout()
    plt.show()

    forecast_data(data, forecast_years)

def calculate_max_changes(data):
    data['Male_Salary_Change'] = data['Male_Salary'].pct_change() * 100
    data['Female_Salary_Change'] = data['Female_Salary'].pct_change() * 100

    max_gain_male = data['Male_Salary_Change'].max()
    max_loss_male = data['Male_Salary_Change'].min()
    max_gain_year_male = data.loc[data['Male_Salary_Change'].idxmax(), 'Year']
    max_loss_year_male = data.loc[data['Male_Salary_Change'].idxmin(), 'Year']

    max_gain_female = data['Female_Salary_Change'].max()
    max_loss_female = data['Female_Salary_Change'].min()
    max_gain_year_female = data.loc[data['Female_Salary_Change'].idxmax(), 'Year']
    max_loss_year_female = data.loc[data['Female_Salary_Change'].idxmin(), 'Year']

    print(f"Maximum Male Salary Increase: {max_gain_male}% in {max_gain_year_male}")
    print(f"Maximum Male Salary Decrease: {max_loss_male}% in {max_loss_year_male}")
    print(f"Maximum Female Salary Increase: {max_gain_female}% in {max_gain_year_female}")
    print(f"Maximum Female Salary Decrease: {max_loss_female}% in {max_loss_year_female}")

def forecast_data(data, forecast_years):
    data['Male_Salary_SMA'] = data['Male_Salary'].rolling(window=3).mean()
    data['Female_Salary_SMA'] = data['Female_Salary'].rolling(window=3).mean()

    last_year = data['Year'].iloc[-1]
    forecast_years = [last_year + i for i in range(1, forecast_years + 1)]
    forecast_male_salary = [data['Male_Salary_SMA'].iloc[-1]] * len(forecast_years)
    forecast_female_salary = [data['Female_Salary_SMA'].iloc[-1]] * len(forecast_years)

    plt.figure(figsize=(14, 7))

    plt.subplot(2, 1, 1)
    plt.plot(data['Year'], data['Male_Salary'], label='Male Salary')
    plt.plot(data['Year'], data['Male_Salary_SMA'], label='SMA (Male Salary)', linestyle='--')
    plt.plot(forecast_years, forecast_male_salary, label='Forecast (Male Salary)', linestyle=':', color='red')
    plt.title('Median Salary for Men in Russia with Forecast')
    plt.xlabel('Year')
    plt.ylabel('Salary')
    plt.legend()

    plt.subplot(2, 1, 2)
    plt.plot(data['Year'], data['Female_Salary'], label='Female Salary')
    plt.plot(data['Year'], data['Female_Salary_SMA'], label='SMA (Female Salary)', linestyle='--')
    plt.plot(forecast_years, forecast_female_salary, label='Forecast (Female Salary)', linestyle=':', color='red')
    plt.title('Median Salary for Women in Russia with Forecast')
    plt.xlabel('Year')
    plt.ylabel('Salary')
    plt.legend()

    plt.tight_layout()
    plt.show()

def main():
    file_path = '3_tp_tab.csv'
    data = load_data(file_path)
    display_data(data)
    calculate_max_changes(data)
    forecast_years = 5
    plot_data(data, forecast_years)

if __name__ == "__main__":
    main()

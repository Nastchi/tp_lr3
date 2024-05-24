import tkinter as tk

def on_button1_click():
    #вызов кода насти
    print("Button 1 clicked")

def on_button2_click():
    #вызов кода руфины
    print("Button 2 clicked")

def on_button3_click():
    # вызов кода алеси
    print("Button 3 clicked")

def on_button4_click():
    # вызов кода ани
    print("Button 4 clicked")
# Создаем главное окно
root = tk.Tk()
root.title("Our Form")

# Задаем размер окна
root.geometry("400x400")

# Устанавливаем цвет фона окна в фиолетовый
root.configure(bg='#efdeff')

# Создаем надпись "Выбор кнопки" с темно-фиолетовым цветом текста
label = tk.Label(root, text="Выбор кнопки", fg='#310957', bg='#efdeff', font=("Arial", 20, "bold"))
label.pack(pady=20)

# Создаем три кнопки и добавляем их в окно
button_Nastya = tk.Button(root, text="Насья", command=on_button1_click,font=("Arial", 10, "bold"),fg='#120121', bg='#b68cf5',width=10,height=2)
button_Nastya.pack(pady=10)

button_Rufina = tk.Button(root, text="Руфима", command=on_button2_click,font=("Arial", 10, "bold"),fg='#21011c', bg='#f08cf5',width=10,height=2)
button_Rufina.pack(pady=10)

button_Alesya = tk.Button(root, text="Алеля", command=on_button3_click,font=("Arial", 10, "bold"),fg='#020121', bg='#8cb8f5',width=10,height=2)
button_Alesya.pack(pady=10)

button_Alesya = tk.Button(root, text="Аня", command=on_button4_click,font=("Arial", 10, "bold"),fg='#352900', bg='#fee27e',width=10,height=2)
button_Alesya.pack(pady=10)
# Запускаем главный цикл обработки событий
root.mainloop()
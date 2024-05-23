import tkinter as tk

def on_button_click():
    print("Button clicked")

# Создаем главное окно
root = tk.Tk()
root.title("Simple Form with One Button")

# Создаем кнопку и добавляем ее в окно
button = tk.Button(root, text="Click Me", command=on_button_click, font=("Arial", 12, "bold"), fg="white", bg="blue")
button.pack(pady=20)

# Запускаем главный цикл обработки событий
root.mainloop()

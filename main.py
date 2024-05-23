import tkinter as tk

def show():
    # Создаем главное окно для побочной формы
    side_root = tk.Tk()
    side_root.title("Simple Form with One Button")

    # Создаем кнопку и добавляем ее в окно
    button = tk.Button(side_root, text="Click Me", command=on_button_click, font=("Arial", 12, "bold"), fg="white", bg="blue")
    button.pack(pady=20)

    # Запускаем главный цикл обработки событий
    side_root.mainloop()

def on_button_click():
    print("Button clicked")
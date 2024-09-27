import tkinter as tk

# Функция для обработки нажатия клавиши Enter
def on_submit(event=None):
    # Получаем введённую команду
    user_input = text.get("insert linestart", "insert lineend").strip()
    if user_input:
        # Выводим команду в текстовом виджете
        text.insert("end", f"\nВы ввели: {user_input}")
        # Пример обработки команды, можно добавить свои команды
        if user_input == "exit":
            root.quit()
        elif user_input == "clear":
            text.delete("1.0", "end")
        else:
            # Добавляем результат выполнения команды в текстовое поле
            text.insert("end", f"\nРезультат выполнения команды: {user_input}")

    # Прокручиваем текст до конца
    text.see("end")

# Создаем основное окно
root = tk.Tk()
root.title("Командная строка")

# Делаем окно полноэкранным
root.attributes("-fullscreen", True)

# Позволяем выйти из полноэкранного режима по нажатию клавиши "Esc"
root.bind("<Escape>", lambda event: root.attributes("-fullscreen", False))

# Создаем многострочное текстовое поле для командной строки
text = tk.Text(root, font=("Helvetica", 24), wrap='word')
text.pack(expand=True, fill='both', padx=10, pady=10)

# Добавляем приветствие или приглашение к вводу команды
text.insert("end", "Введите команду:\n")

# Устанавливаем курсор в конец текста для ввода
text.mark_set("insert", "end")

# Позволяем нажать Enter для отправки текста
text.bind("<Return>", on_submit)

# Запуск основного цикла
root.mainloop()

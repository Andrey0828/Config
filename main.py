import os
import tkinter as tk


# Функция для раскрытия переменных в аргументах командной строки
def expand_arg(s):
    # Заменяем $HOME на домашнюю директорию
    if "$HOME" in s:
        s = s.replace("$HOME", os.path.expanduser("~"))
    # Заменяем другие переменные окружения
    for k, v in os.environ.items():
        s = s.replace("$" + k, v)
    return s


# Основная функция выполнения команд
def run_cmd():
    # Проверяем, существует ли еще поле ввода (на случай закрытия приложения)
    if not entry.winfo_exists():
        return
    user_input = entry.get()
    append_text(f"vfs> {user_input}\n")
    # Если введена пустая строка, просто очищаем поле ввода
    if not user_input.strip():
        entry.delete(0, tk.END)
        return
    parts = user_input.split()
    cmd, *args = parts
    args = [expand_arg(a) for a in args]  # Обрабатываем аргументы, раскрывая переменные окружения
    # Обработка команд
    if cmd == "exit":
        append_text("Exiting...\n")
        root.destroy()
        return
    elif cmd == "ls":
        append_text(f"ls {' '.join(args)}\n")
    elif cmd == "cd":
        append_text(f"cd {' '.join(args)}\n")
    else:
        append_text(f"Command not found: {cmd}\n")
    entry.delete(0, tk.END)  # Очищаем поле ввода после выполнения команды


# Функция для добавления текста в текстовое поле
def append_text(msg):
    text.configure(state="normal")
    text.insert(tk.END, msg)
    text.see(tk.END)
    text.configure(state="disabled")


root = tk.Tk()  # Создаем главное окно приложения
root.title("VFS Эмулятор - [username@hostname]")
text = tk.Text(root,
               height=15,
               width=70,
               font=("Consolas", 11),
               state="disabled")  # Создаем текстовое поле для вывода результатов
text.pack(padx=5, pady=5)
entry = tk.Entry(root, width=70, font=("Consolas", 11)) # Создаем поле для ввода команд
entry.pack(padx=5, pady=5)
entry.bind("<Return>", lambda e: run_cmd()) # Привязываем нажатие Enter к выполнению команды
tk.Button(root, text="Run", command=run_cmd).pack(pady=5) # Создаем кнопку "Run" для выполнения команды
root.mainloop() # Запускаем главный цикл обработки событий

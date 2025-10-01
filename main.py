import argparse
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


# Функция выполнения команды
def execute_command(cmd, args):
    if cmd == "exit":
        append_text("Exiting...\n")
        root.after(100, root.destroy)
        return False
    elif cmd == "ls":
        append_text(f"ls {' '.join(args)}\n")
        return True
    elif cmd == "cd":
        append_text(f"cd {' '.join(args)}\n")
        return True
    elif cmd == "pwd":
        append_text(f"pwd\n")
        return True
    elif cmd == "echo":
        append_text(f"echo {' '.join(args)}\n")
        return True
    else:
        append_text(f"Command not found: {cmd}\n")
        return False


# Функция выполнения команд из скрипта
def run_script(script_path):
    try:
        # Пробуем разные кодировки для чтения файла
        encodings = ['utf-8', 'cp1251']
        script_content = None

        for encoding in encodings:
            try:
                with open(script_path, 'r', encoding=encoding) as f:
                    script_content = f.read()
                break
            except UnicodeDecodeError:
                continue

        lines = script_content.splitlines()

    except Exception as e:
        append_text(f"Error reading script: {e}\n")
        return False

    # Обработка каждой строки скрипта
    for line_num, line in enumerate(lines, 1):
        line = line.strip()
        # Пропускаем пустые строки и комментарии
        if not line or line.startswith('#'):
            continue

        append_text(f"{prompt} {line}\n")
        parts = line.split()
        cmd, *args = parts
        args = [expand_arg(a) for a in args]

        # Выполняем команду и проверяем результат
        success = execute_command(cmd, args)
        if not success:
            if cmd == "exit":
                return True
            append_text(f"Script stopped at line {line_num}\n")
            return False

    return True

# Основная функция выполнения команд из интерфейса
def run_cmd(event=None):
    user_input = entry.get()
    append_text(f"{prompt} {user_input}\n")
    # Если введена пустая строка, просто очищаем поле ввода
    if not user_input.strip():
        entry.delete(0, tk.END)
        return

    parts = user_input.split()
    cmd, *args = parts
    args = [expand_arg(a) for a in args]  # Обрабатываем аргументы, раскрывая переменные окружения

    # Выполняем команду и очищаем поле ввода только если команда не exit
    success = execute_command(cmd, args)
    if success and cmd != "exit":
        entry.delete(0, tk.END)  # Очищаем поле ввода после выполнения команды


# Функция для добавления текста в текстовое поле
def append_text(msg):
    text.configure(state="normal")
    text.insert(tk.END, msg)
    text.see(tk.END)
    text.configure(state="disabled")


# Парсинг аргументов командной строки
parser = argparse.ArgumentParser(description='VFS Emulator')
parser.add_argument('--vfs-path', type=str, help='Path to VFS physical location')
parser.add_argument('--prompt', type=str, default='vfs>', help='Custom input prompt')
parser.add_argument('--script', type=str, help='Path to startup script')
args = parser.parse_args()
vfs_path = args.vfs_path
prompt = args.prompt

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
entry.bind("<Return>", run_cmd) # Привязываем нажатие Enter к выполнению команды
tk.Button(root, text="Run", command=run_cmd).pack(pady=5)  # Создаем кнопку "Run" для выполнения команды

# Выполнение стартового скрипта если указан
if args.script:
    script_path = expand_arg(args.script)
    append_text(f"Executing startup script: {script_path}\n")
    # Запуск скрипта с небольшой задержкой для инициализации интерфейса
    root.after(100, lambda: run_script(script_path))

root.mainloop()
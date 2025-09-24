import os
import tkinter as tk


def expand_arg(s: str):
    if "$HOME" in s:
        s = s.replace("$HOME", os.path.expanduser("~"))
    for k, v in os.environ.items():
        s = s.replace("$" + k, v)
    return s


def run_cmd():
    if not entry.winfo_exists():
        return
    user_input = entry.get()
    append_text(f"vfs> {user_input}\n")
    if not user_input.strip():
        entry.delete(0, tk.END)
        return
    parts = user_input.split()
    cmd, *args = parts
    args = [expand_arg(a) for a in args]
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
    entry.delete(0, tk.END)


def append_text(msg: str):
    text.configure(state="normal")
    text.insert(tk.END, msg)
    text.see(tk.END)
    text.configure(state="disabled")


root = tk.Tk()
root.title("Эмулятор - [username@hostname]")
text = tk.Text(root, height=15, width=70, font=("Consolas", 11), state="disabled")
text.pack(padx=5, pady=5)
entry = tk.Entry(root, width=70, font=("Consolas", 11))
entry.pack(padx=5, pady=5)
entry.bind("<Return>", lambda e: run_cmd())
tk.Button(root, text="Run", command=run_cmd).pack(pady=5)
root.mainloop()

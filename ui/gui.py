import tkinter as tk

from commands.basic_commands import cd, ls, rename, move, copy
from fs.unpack_fs import load_virtual_fs

class ShellEmulator:
    def __init__(self, root, config):
        self.root = root
        self.USER = config['username']
        self.COMPUTER = config['computer']
        self.fs = load_virtual_fs(config['fs_path'])
        self.curDir = []
        self.zip_path = config['fs_path']
        self.root.title("Командная строка")
        self.root.configure(bg="black")
        self.root.attributes("-fullscreen", True)
        self.root.bind("<Escape>", self.exit_fullscreen)
        self.text = tk.Text(root, font=("Helvetica", 18), wrap='word', bg="black", fg="green", insertbackground="white")
        self.text.pack(expand=True, fill='both', padx=10, pady=10)

        self.prompt()

        self.text.bind("<Return>", self.on_submit)

        self.text.mark_set("insert", "end")

    def prompt(self):
        current_dir_str = '/' + '/'.join(self.curDir) if self.curDir else '~'
        self.text.insert("end", f"{self.USER}@{self.COMPUTER}:{current_dir_str}$ ")
        self.text.see("end")

    def exit_fullscreen(self, event=None):
        self.root.attributes("-fullscreen", False)

    def on_submit(self, event=None):
        current_text = self.text.get("1.0", "end").strip()

        last_prompt_index = current_text.rfind(f"{self.USER}@{self.COMPUTER}:")
        if last_prompt_index == -1:
            return

        user_input = current_text[last_prompt_index:].split('$', 1)[-1].strip()

        if user_input:
            self.process_command(user_input)
            self.prompt()
        return "break"

    def process_command(self, command):
        if command.startswith("cd"):
            new_dir = command.split(" ", 1)[1].strip() if len(command.split()) > 1 else None
            if new_dir:
                result = cd(new_dir, self.curDir, self.fs)
                if isinstance(result, str):
                    self.text.insert("end", result + "\n")
                else:
                    self.curDir = result
                    self.text.insert("end", f"\nПерешли в: /{'/'.join(self.curDir) if self.curDir else '~'}\n")
            else:
                self.text.insert("end", "нет аргумента\n")
        elif command == "clear":
            self.text.delete("1.0", "end")
        elif command == "ls":
            result = ls(self.curDir, self.fs)
            self.text.insert("end", f"\n{result}\n")
        elif command.startswith("mv"):
            parts = command.split()
            if len(parts) != 3:
                self.text.insert("end", "\nТребуется два аргумента\n")
                return

            old_name, new_name_or_path = parts[1].strip(), parts[2].strip()

            if '/' not in new_name_or_path and '\\' not in new_name_or_path:
                result = rename(old_name, new_name_or_path, self.curDir, self.fs, self.zip_path)
                self.text.insert("end", f"\n{result}\n")
            else:
                result = move(old_name, new_name_or_path, self.curDir, self.fs, self.zip_path)
                self.text.insert("end", f"\n{result}\n")
        elif command.startswith("cp"):
            parts = command.split()
            if len(parts) != 3:
                self.text.insert("end", "\nТребуется два аргумента\n")
                return

            file_name, target_path = parts[1].strip(), parts[2].strip()

            result = copy(file_name, target_path, self.curDir, self.fs, self.zip_path)
            self.text.insert("end", f"\n{result}\n")
        elif command == "exit":
            exit(0)
        else:
            self.text.insert("end", f"\nНеизвестная команда: {command}\n")



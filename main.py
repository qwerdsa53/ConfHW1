from config.config_loader import load_config
from fs.unpack_fs import load_virtual_fs
import tkinter as tk

from ui.gui import ShellEmulator


def main():
    config = load_config("config.csv")
    root = tk.Tk()
    ShellEmulator(root, config)
    root.mainloop()


if __name__ == "__main__":
    main()

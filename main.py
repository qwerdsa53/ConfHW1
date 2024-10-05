from xml.etree.ElementTree import tostring

from config.config_loader import load_config
import tkinter as tk
from sys import argv
from ui.gui import ShellEmulator


def main():
    config = load_config(argv[1])
    root = tk.Tk()
    ShellEmulator(root, config)
    root.mainloop()


if __name__ == "__main__":
    main()
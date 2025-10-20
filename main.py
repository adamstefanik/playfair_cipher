import tkinter as tk
from gui import PlayfairCipherGUI


def main():
    root = tk.Tk()
    app = PlayfairCipherGUI(root)
    root.mainloop()


if __name__ == "__main__":
    main()

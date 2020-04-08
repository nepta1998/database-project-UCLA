import tkinter as tk
from interfaces.application_interfaces import App


def main():
    window = tk.Tk()
    window.geometry("800x600")
    app = App(window)
    window.mainloop()


if __name__ == '__main__':
    main()

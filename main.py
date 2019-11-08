from gui import MyGui
from controller import Controller
from tkinter import Tk


def main():
    root = Tk()
    c = Controller()
    MyGui(root, c)
    root.mainloop()


if __name__ == '__main__':
    main()

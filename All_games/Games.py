from tkinter import *
import os

path = '%s/Game.py'
file = __file__[:len(__file__) - 8:]


class GameBlock:
    def __init__(self, x, y, text, path_name):
        self.but = Button(text=text, command=self.button_command, height=2, width=10, font='Arial 10 bold')
        self.but.place(x=x, y=y)
        self.path_name = path_name

    def button_command(self):
        os.system("python3 " + file + path % self.path_name)


if __name__ == '__main__':
    root = Tk()
    root.geometry('400x400+100+100')

    block_Sapper = GameBlock(50, 50, 'Сапёр', 'Сапёр')
    block_2048 = GameBlock(250, 50, '2048', '2048')
    block_Graphes = GameBlock(50, 150, 'Graphes', 'Graphes')
    block_Bomberman = GameBlock(250, 150, 'Bomberman', 'Bomberman')
    block_Snake = GameBlock(50, 250, 'Snake', 'Snake')
    block_TicTacToe = GameBlock(250, 250, 'TicTacToe', 'TicTacToe')

    root.mainloop()

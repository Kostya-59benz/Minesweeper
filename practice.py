import tkinter as tk
from random import shuffle
from tkinter.messagebox import showinfo

colors = {
    1: 'red',
    2: 'blue',
    3: 'green',
    4: 'purple',
    5: 'brown',
    6: 'yellow',
    7: 'orange'
}


class MyButton(tk.Button):

    def __init__(self, master, x, y, numbers=0, *args, **kwargs):
        super(MyButton, self).__init__(master, width=3, font="Calibri 15 bold", *args, **kwargs)
        self.numbers = numbers
        self.x = x
        self.y = y
        self.is_mine = False
        self.count_bombs = 0
        self.is_open = False

    def __repr__(self):
        return f'MyButton {self.x} {self.y} {self.numbers}'


class Minesweeper:
    window = tk.Tk()
    COLUMNS = 10
    ROWS = 10
    BOMBS = 3
    IS_GAME_OVER = False

    def __init__(self):
        self.buttons = []
        for i in range(Minesweeper.ROWS + 2):
            temp = []
            for j in range(Minesweeper.COLUMNS + 2):
                btn = MyButton(Minesweeper.window, x=i, y=j)
                btn.config(command=lambda button=btn: self.click(button))
                temp.append(btn)

            self.buttons.append(temp)

    def click(self, clicked_button: MyButton):
        if clicked_button.is_mine:
            clicked_button.config(text="*", background='red', disabledforeground='black')
            clicked_button.is_open = True
            Minesweeper.IS_GAME_OVER = True
            showinfo("Game over", "Вы проиграли!")
            for i in range(1, Minesweeper.ROWS + 1):
                for j in range(1, Minesweeper.COLUMNS + 1):
                    btn = self.buttons[i][j]
                    if btn.is_mine:
                        btn['text'] = '*'
        else:

            color = colors.get(clicked_button.count_bombs, 'white')
            if clicked_button.count_bombs:
                clicked_button.config(text=clicked_button.count_bombs, disabledforeground=color)
                clicked_button.is_open = True
            else:
                self.breath_first_search(clicked_button)
        clicked_button.config(state='disabled')
        clicked_button.config(relief=tk.SUNKEN)

    def breath_first_search(self, btn: MyButton):

        queue = [btn]

        while queue:
            cur_btn = queue.pop()
            color = colors.get(cur_btn.count_bombs, 'black')
            if cur_btn.count_bombs:
                cur_btn.config(text=cur_btn.count_bombs, disabledforeground=color)
            cur_btn.is_open = True
            cur_btn.config(state='disabled')
            cur_btn.config(relief=tk.SUNKEN)

            if cur_btn.count_bombs == 0:
                x, y = cur_btn.x, cur_btn.y
                for dx in [-1, 0, 1]:
                    for dy in [-1, 0, 1]:
                       # if not abs(dx - dy) == 1:
                       #    continue

                        next_btn = self.buttons[x + dx][y + dy]
                        if not next_btn.is_open and 1 <= next_btn.x <= Minesweeper.ROWS and \
                                1 <= next_btn.y <= Minesweeper.COLUMNS and next_btn not in queue:
                            queue.append(next_btn)

    def print_buttons(self):
        for i in range(1, Minesweeper.ROWS + 1):
            for j in range(1, Minesweeper.COLUMNS + 1):
                btn = self.buttons[i][j]
                if btn.is_mine:
                    print("B", end='')
                else:
                    print(btn.count_bombs, end='')
            print()

    def create_vidget(self):
        for i in range(1, Minesweeper.ROWS + 1):
            for j in range(1, Minesweeper.COLUMNS + 1):
                btn = self.buttons[i][j]
                btn.grid(row=i, column=j)

    def insert_mines(self):
        indexes = self.indexes_mines()
        print(indexes)
        count = 1
        for i in range(1, Minesweeper.ROWS + 1):
            for j in range(1, Minesweeper.COLUMNS + 1):
                btn = self.buttons[i][j]
                btn.numbers = count
                if btn.numbers in indexes:
                    btn.is_mine = True
                count += 1

    def count_bombs_in_buttons(self):
        for i in range(1, Minesweeper.ROWS + 1):
            for j in range(1, Minesweeper.COLUMNS + 1):
                btn = self.buttons[i][j]
                count_bomb = 0
                if not btn.is_mine:
                    for row_dx in [-1, 0, 1]:
                        for col_dx in [-1, 0, 1]:
                            neightbor = self.buttons[i + row_dx][j + col_dx]
                            if neightbor.is_mine:
                                count_bomb += 1
                    btn.count_bombs = count_bomb

    def start(self):
        self.create_vidget()
        self.insert_mines()
        self.count_bombs_in_buttons()
        self.print_buttons()
        # self.open_all_buttons()
        Minesweeper.window.mainloop()

    @staticmethod
    def indexes_mines():
        indexes = list(range(1, Minesweeper.COLUMNS * Minesweeper.ROWS + 1))
        shuffle(indexes)
        return indexes[:Minesweeper.BOMBS]


on = Minesweeper()
on.start()

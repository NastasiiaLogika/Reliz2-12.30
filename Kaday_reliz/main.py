import tkinter as tk
import random
from tkinter import messagebox

class Game2048:
    def __init__(self, size):
        self.size = size
        self.window = tk.Tk()
        self.window.title('2048 Game')
        self.score = 0
        self.grid = [[0] * size for _ in range(size)]
        self.cells = []
        self.create_gui()
        self.start_game()
        self.window.mainloop()

    def create_gui(self):
        background = tk.Frame(self.window, bg='azure3')
        background.grid()
        for i in range(self.size):
            row = []
            for j in range(self.size):
                cell = tk.Label(background, text='', bg='azure4',
                                font=('arial', 22, 'bold'), width=4, height=2)
                cell.grid(row=i, column=j, padx=5, pady=5)
                row.append(cell)
            self.cells.append(row)
        self.window.bind('<Key>', self.key_handler)

    def start_game(self):
        self.add_new_tile()
        self.add_new_tile()
        self.update_gui()

    def add_new_tile(self):
        empty_cells = [(i, j) for i in range(self.size)
                       for j in range(self.size) if self.grid[i][j] == 0]
        if empty_cells:
            i, j = random.choice(empty_cells)
            self.grid[i][j] = random.choice([2, 4])

    def update_gui(self):
        for i in range(self.size):
            for j in range(self.size):
                value = self.grid[i][j]
                if value == 0:
                    self.cells[i][j].configure(text='', bg='azure4')
                else:
                    self.cells[i][j].configure(text=str(value),
                                               bg='lightblue',
                                               fg='black')

    def key_handler(self, event):
        key = event.keysym
        if key == 'Up':
            self.move('up')
        elif key == 'Down':
            self.move('down')
        elif key == 'Left':
            self.move('left')
        elif key == 'Right':
            self.move('right')
        self.update_gui()
        if self.check_win():
            messagebox.showinfo('2048', 'You Win!')
            self.window.quit()
        elif self.check_game_over():
            messagebox.showinfo('2048', 'Game Over!')
            self.window.quit()

    def move(self, direction):
        def merge(row):
            non_zero = [num for num in row if num != 0]
            merged = []
            skip = False
            for i in range(len(non_zero)):
                if skip:
                    skip = False
                    continue
                if i + 1 < len(non_zero) and non_zero[i] == non_zero[i + 1]:
                    merged.append(non_zero[i] * 2)
                    self.score += non_zero[i] * 2
                    skip = True
                else:
                    merged.append(non_zero[i])
            return merged + [0] * (self.size - len(merged))

        moved = False
        for i in range(self.size):
            if direction == 'left':
                original = self.grid[i]
                merged = merge(original)
                if merged != original:
                    moved = True
                self.grid[i] = merged
            elif direction == 'right':
                original = self.grid[i][::-1]
                merged = merge(original)
                if merged[::-1] != self.grid[i]:
                    moved = True
                self.grid[i] = merged[::-1]
            elif direction == 'up':
                original = [self.grid[j][i] for j in range(self.size)]
                merged = merge(original)
                if merged != original:
                    moved = True
                for j in range(self.size):
                    self.grid[j][i] = merged[j]
            elif direction == 'down':
                original = [self.grid[j][i] for j in range(self.size)][::-1]
                merged = merge(original)
                if merged[::-1] != [self.grid[j][i] for j in range(self.size)]:
                    moved = True
                for j in range(self.size):
                    self.grid[j][i] = merged[::-1][j]
        if moved:
            self.add_new_tile()

    def check_win(self):
        for row in self.grid:
            if 2048 in row:
                return True
        return False

    def check_game_over(self):
        for i in range(self.size):
            for j in range(self.size):
                if self.grid[i][j] == 0:
                    return False
                if j + 1 < self.size and self.grid[i][j] == self.grid[i][j + 1]:
                    return False
                if i + 1 < self.size and self.grid[i][j] == self.grid[i + 1][j]:
                    return False
        return True

def main():
    def start_game(size):
        root.destroy()
        Game2048(size)

    root = tk.Tk()
    root.title("Select Grid Size")
    tk.Label(root, text="Choose grid size:", font=('arial', 14)).pack(pady=10)
    tk.Button(root, text="4 x 4 (Easy)", command=lambda: start_game(4),
              width=20, height=2).pack(pady=5)
    tk.Button(root, text="8 x 8 (Medium)", command=lambda: start_game(8),
              width=20, height=2).pack(pady=5)
    tk.Button(root, text="16 x 16 (Hard)", command=lambda: start_game(16),
              width=20, height=2).pack(pady=5)
    root.mainloop()

if __name__ == '__main__':
    main()
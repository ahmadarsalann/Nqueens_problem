import random
import sys
import numpy
from numpy.random import default_rng
import time
import tkinter as tk
import tkinter.font as tkFont
import tkinter.ttk as ttk
from tkinter import * 

class aahmad3_nqueens:
    def __init__(self):
        self.board = []
        self.temp_board = []
        self.board_length = int(sys.argv[1])
        self.queens = sys.argv[1]
        self.list = []
        self.nothing = False

    def make_board(self):
        rand = default_rng()
        self.board = rand.choice(self.board_length * self.board_length, size=(self.board_length, self.board_length),
                                 replace=False)
        self.temp_board = numpy.copy(self.board)
        return self.board

    def print_board(self):
        print(self.board)

    def place_queen(self, column):
        self.list = self.board[:, column].copy()
        if column == 0:
            queen = random.choice(self.board[:, column])
            index = numpy.where(self.board[:, column] == queen)
            self.board[:, column] = numpy.where(self.board[:, column] == queen, 9000, self.board[:, column])
            return column
        else:
            index = self.find_the_index(column, self.list, column)
            if index[1] != column:
                temp_board = self.board[:, :index[1] + 1]
                second_tempboard = self.temp_board[:, index[1] + 1:]
                temp_board = numpy.concatenate((temp_board, second_tempboard), axis=1)
                temp_board[:, index[1]] = numpy.where(temp_board[:, index[1]] == index[0], 9000,
                                                      temp_board[:, index[1]])
                self.board = temp_board
            else:
                self.board[:, column] = numpy.where(self.board[:, column] == index[0], 9000, self.board[:, column])

            temp_list = numpy.where(self.board == 9000)
            final_list = list(zip(temp_list[1], temp_list[0]))
            final_list = sorted(final_list, key=lambda x: x[0])
            final_list = [x[1] for x in final_list]
            print(final_list)
            return index[1]

    def find_the_index(self, column, list, original_column):
        if column == 0 and len(list) > 0:
            test = random.choice(list), original_column
            return test

        elif column == 0 and len(list) == 0 or len(list) == 0:
            column = original_column - 1
            original_column = original_column - 1
            self.place_24(column)
            list = self.board[:, column]
            list = list[list != 24000]
            found_the_new_index = self.find_the_index(column, list, original_column)
            return found_the_new_index

        diagonal_pattern = self.get_diagonal_pattern(column - 1)
        vertical_pattern = self.get_vertical_pattern(column - 1)
        all_patterns = diagonal_pattern[0] + diagonal_pattern[1] + vertical_pattern
        common_elements = numpy.intersect1d(list, all_patterns)
        self.list = [i for i in list if i not in common_elements]
        return self.find_the_index(column - 1, self.list, original_column)

    def place_24(self,column):
        self.board[:, column] = numpy.where(self.board[:, column] == 9000, 24000, self.board[:, column])

    def get_diagonal_pattern(self, column):
        index = numpy.where(self.board[:, column] == 9000)
        if len(index[0]) == 0:
            return "No Queen Found"
        if column == 0:
            bottom_diagonal_values = numpy.diag(self.board, -index[0][0])
            bottom_diagonal_values = numpy.delete(bottom_diagonal_values, [0])
            flipped_board = numpy.copy(self.board)
            flipped_board = numpy.flipud(flipped_board)
            new_index = numpy.where(flipped_board[:, column] == 9000)
            upper_diagonal_values = numpy.diag(flipped_board, -new_index[0][0])
            upper_diagonal_values = numpy.delete(upper_diagonal_values, 0)
        else:
            second_board = numpy.delete(self.board, numpy.s_[0: column], axis=1)
            bottom_diagonal_values = numpy.diag(second_board, -index[0][0])
            bottom_diagonal_values = numpy.delete(bottom_diagonal_values, 0)
            flipped_board = numpy.copy(second_board)
            flipped_board = numpy.flipud(flipped_board)
            new_index = numpy.where(flipped_board[:, 0] == 9000)
            upper_diagonal_values = numpy.diag(flipped_board, -new_index[0][0])
            upper_diagonal_values = numpy.delete(upper_diagonal_values, 0)
        return upper_diagonal_values.tolist(), bottom_diagonal_values.tolist()

    def get_vertical_pattern(self, column):
        index = numpy.where(self.board[:, column] == 9000)
        if len(index[0]) == 0:
            return "No Queens Found"
        row = self.board[index]
        index2 = numpy.where(row[0] == 9000)
        elements_after_nth_index = row[0][index2[0][0]:]
        elements_after_nth_index = numpy.delete(elements_after_nth_index, 0)
        return elements_after_nth_index.tolist()

class draw_Queen_board:

    def __init__(self, final_list, end_time):
        self.do_replay = False
        self.root = tk.Tk()
        self.root.title('                    ' + str(end_time) + ' seconds')
        self.top = ttk.Frame(self.root)
        self.canvas = tk.Canvas(self.root, width=1000, height=1000)
        self.draw_board()
        self.place_queens(final_list)
        self.canvas.pack()
        self.root.mainloop()

    def draw_board(self):
        number = 0
        odd = False
        if int(sys.argv[1]) > 28:
            number = 13
        else:
            number = 25
        if int(sys.argv[1]) % 2 != 0:
            odd= True
        curr_col = "LightPink1"

        for x in range(0, int(sys.argv[1]) * number,
                       number):
            for y in range(0, int(sys.argv[1]) * number,
                           number):

                x2, y2 = x + number, y + number
                self.canvas.create_rectangle(x, y, x2, y2, fill=curr_col)
                curr_col = ("LightBlue1"
                            if curr_col == "LightPink1"
                            else "LightPink1")
            if odd is False:
                curr_col = ("LightBlue1"
                            if curr_col == "LightPink1"
                            else "LightPink1")

    def place_queens(self, final_list):
        base = 5
        number = 0
        size = 0
        if int(sys.argv[1]) > 28:
            number = 13
            size = 2
        else:
            number = 25
            size = 10

        for i in range(int(sys.argv[1])):
            widget = Label(self.root, text='Q', fg='white', bg='black', width=0, height=0)
            widget.config(font=("Courier", size))
            widget.place(x=base, y=final_list[i]*number)
            base = base + number

start_time = time.time()
queen = aahmad3_nqueens()
board = queen.make_board()
i = 0
while i <= queen.board_length - 1:
    track = queen.place_queen(i)
    if i != track:
        i = track
    i = i + 1

print("")
queen.print_board()
temp_list = numpy.where(queen.board == 9000)
final_list = list(zip(temp_list[1], temp_list[0]))
final_list = sorted(final_list, key=lambda x: x[0])
final_list = [x[1] for x in final_list]
print("")
print(final_list)
end_time = round(time.time() - start_time, 4)
print("")
print(end_time)
draw_board = draw_Queen_board(final_list, end_time)

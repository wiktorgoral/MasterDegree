from enum import Enum
from model.Cell import Cell


class Layer:
    name = ""
    # Length of array
    size = 0
    # 2D array of Cell
    cells = None
    # Array of tuples (state's name, state's color)
    cells_states = []

    def __init__(self, name="", size=100, neighbour="", cell_states=[]):
        self.name = name
        self.size = size
        self.cells = [[Cell() for col in range(size)] for row in range(size)]
        self.cells_states = cell_states
        self.add_neighbourhood(neighbour)

    # Function that adds neighbourhoods for all cells
    def add_neighbourhood(self, neighbour):
        if neighbour.lower() == "moore":
            self.moore()
        elif neighbour.lower() == "neumann":
            self.von_neumann()
        elif neighbour.lower() == "none":
            return
        else:
            raise Exception("No neighbourhood")

    # Iteration step
    def step(self):
        self.calculate_state()
        self.change_state()

    # Function that clears one cell
    def clear(self, x, y):
        self.cells[x][y].clear()

    # Function that clears all cells
    def reset(self):
        for x in range(self.size):
            for y in range(self.size):
                self.clear(x, y)

    # Function that calculates state for each cell
    def calculate_state(self):
        for x in range(self.size):
            for y in range(self.size):
                self.cells[x][y].calculate_state()

    # Function that changes state for each cell
    def change_state(self):
        for x in range(self.size):
            for y in range(self.size):
                self.cells[x][y].current_state = self.cells[x][y].next_state
                self.cells[x][y].next_state = self.cells_states[0][0]

    # Function that changes cell
    def change_cell(self, cell, x, y):
        self.cells[x][y] = cell

    # Function that prints cell's state
    def print_cell_state(self, x, y):
        state = self.cells[x][y].current_state
        print(self.cells_states[state][0])

    '''
    neighbourhood indexes
    Moore:
        1
    0   x   3
        2
    '''
    def moore(self):
        for x in range(1, self.size - 1):
            for y in range(1, self.size - 1):

                for xi in range(x - 1, x + 2):
                    for yi in range(y - 1, y + 2):
                        if xi == x and yi == y: continue
                        self.cells[x][y].neighbours_add(self.cells[xi][yi])

    '''
    Von Neumann:
    0   3   5
    1   x   6
    2   4   7
    '''
    def von_neumann(self):
        for x in range(1, self.size - 1):
            for y in range(1, self.size - 1):
                self.cells[x][y].neighbours_add(self.cells[x - 1][y])
                self.cells[x][y].neighbours_add(self.cells[x][y + 1])
                self.cells[x][y].neighbours_add(self.cells[x][y - 1])
                self.cells[x][y].neighbours_add(self.cells[x + 1][y])

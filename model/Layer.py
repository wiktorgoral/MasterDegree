from model.Cell import Cell
import numpy as np


class Layer:
    name = ""
    # Length of array
    size = 0
    # 2D array of Cell
    cells = np.zeros(1, dtype=Cell)
    # Array of tuples (state's name, state's color)
    cells_states = [("nothing", "white")]

    def __init__(self, name: str, size: int, neighbour: str, cell_states: list):
        self.name = name
        self.size = size
        self.cells = np.zeros((size, size), dtype=Cell)
        self.cells_states.extend(cell_states)
        self.add_neighbourhood(neighbour)

    # Function that adds neighbourhoods for all cells
    def add_neighbourhood(self, neighbour: str):
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
    def clear(self, x: int, y: int):
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

    # Function that changes cell state
    def change_cell_state(self, x: int, y: int, state: int):
        self.cells[x][y].state = state

    # Function that prints cell's state
    def return_cell_state_color(self, x: int, y: int):
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

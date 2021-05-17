import os
from copy import deepcopy
from typing import List, Tuple

from model.Cell import Cell


class Layer:
    name: str
    size: int
    cells: List[List[Cell]] = [[Cell(0, [], False) for x in range(2)] for y in range(2)]
    # Array of tuples (state's name, state's color)
    cells_states: List[Tuple[str, str]] = []
    neighbourhood: str
    rules: list

    def __init__(self, name: str, size: int, neighbour: str, cell_states: list):
        self.name = name
        self.size = size
        self.cells = [[Cell(0, [], False) for _ in range(size)] for _ in range(size)]
        self.cells_states = cell_states
        self.neighbourhood = neighbour
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
        self.iteration()

    # Function that clears one cell
    def clear(self, x: int, y: int):
        self.cells[x][y].clear()

    def clear_all(self):
        for x in range(self.size):
            for y in range(self.size):
                self.clear(x, y)

    # Function that calculates state for each cell
    def calculate_state(self):
        for x in range(self.size):
            for y in range(self.size):
                self.cells[x][y].calculate_state()

    def calculate_state_with_rules(self):
        for x in range(self.size):
            for y in range(self.size):
                self.cells[x][y].calculate_state(self.rules)

    # Function that changes state for each cell
    def iteration(self):
        for x in range(self.size):
            for y in range(self.size):
                self.cells[x][y].current_state = self.cells[x][y].next_state
                self.cells[x][y].next_state = 0

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

    # Save layer to txt file
    def to_file(self, path):
        file = open(os.path.join(path, self.name), "x")
        file.write(self.name + os.linesep)
        file.write(str(self.size) + os.linesep)
        file.write(self.neighbourhood + os.linesep)
        file.write(os.linesep)
        for x in range(self.size):
            line = ""
            for y in range(self.size):
                line += self.cells[x][y].current_state
            file.write(line + os.linesep)
        file.write(os.linesep)
        for x in range(1, len(self.cells_states)):
            file.write(self.cells_states[x][0] + " " + self.cells_states[x][1] + os.linesep)
        file.write(os.linesep)
        for x in range(self.size):
            for y in range(self.size):
                if self.cells[x][y].current_state != 0:
                    file.write(str(self.cells[x][y].value) + os.linesep)
        file.close()

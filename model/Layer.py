import os
from copy import deepcopy
from typing import List, Tuple

from model.Cell import Cell


class Layer:
    name: str
    size: int
    cells: List[List[Cell]]
    # Array of tuples (state's name, state's color)
    cells_states: List[Tuple[str, str]] = []
    neighbourhood: str
    rules: list
    cells_copy: List[List[tuple]] = list(list())
    iterationn: int = 0

    def __init__(self, name: str, cells: List[List[Cell]], neighbour: str, cell_states: list):
        self.name = name
        self.size = len(cells)
        self.cells = cells
        self.cells_states = cell_states
        self.neighbourhood = neighbour
        self.add_neighbourhood(neighbour)
        for x in range(self.size):
            self.cells_copy.append(list())
            for y in range(self.size):
                self.cells_copy[x].append((deepcopy(self.cells[x][y].current_state),deepcopy(self.cells[x][y].value)))

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

    # Clear all cells
    def clear_all(self):
        for x in range(self.size):
            for y in range(self.size):
                self.cells[x][y].clear()

    # Reset cells to state at iteration 0
    def reset(self):
        for x in range(self.size):
            for y in range(self.size):
                self.cells[x][y].current_state = self.cells_copy[x][y][0]
                self.cells[x][y].next_state = 0
                self.cells[x][y].value = self.cells_copy[x][y][1]
        self.iterationn = 0

    # Function that calculates state for each cell
    def calculate_state(self):
        for x in range(self.size):
            for y in range(self.size):
                self.cells[x][y].calculate_state()

    # Function that calculates state based on slide window rules
    def calculate_state_with_rules(self):
        for x in range(1, self.size-1):
            for y in range(1, self.size-1):
                self.cells[x][y].calculate_state(self.rules)

    # Function that changes state for each cell
    def iteration(self):
        for x in range(self.size):
            for y in range(self.size):
                self.cells[x][y].current_state = self.cells[x][y].next_state
                self.cells[x][y].next_state = 0
        self.iterationn += 1

    '''
    neighbourhood indexes
    Moore:
    0   3   5
    1   x   6
    2   4   7
    '''

    def moore(self):
        for x in range(1, self.size - 1):
            for y in range(1, self.size - 1):
                neighbours = []
                for xi in range(x - 1, x + 2):
                    for yi in range(y - 1, y + 2):
                        if xi == x and yi == y: continue
                        neighbours.append(self.cells[xi][yi])
                self.cells[x][y].neighbours = neighbours

    '''
    Von Neumann:
        1
    0   x   3
        2
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

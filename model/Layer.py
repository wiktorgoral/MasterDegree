import os
from copy import deepcopy
from typing import List, Tuple

from model.Cell import Cell


class Layer:
    name: str
    height: int
    width: int
    cells: List[List[Cell]]
    # Array of tuples (state's name, state's color)
    cells_states: List[Tuple[str, str]] = []
    neighbourhood: str
    rules: list
    cells_copy: List[List[tuple]] = list(list())
    iterationn: int = 0

    def __init__(self, name: str, cells: List[List[Cell]], neighbour: str, cell_states: list):
        self.name = name
        self.height = len(cells)
        self.width = len(cells[0])
        self.cells = cells
        self.cells_states = cell_states
        self.neighbourhood = neighbour
        self.add_neighbourhood(neighbour)
        for y in range(self.height):
            self.cells_copy.append(list())
            for x in range(self.width):
                self.cells_copy[y].append((deepcopy(self.cells[y][x].current_state), deepcopy(self.cells[y][x].value)))

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
        for y in range(self.height):
            for x in range(self.width):
                self.cells[y][x].clear()

    # Reset cells to state at iteration 0
    def reset(self):
        for y in range(self.height):
            for x in range(self.width):
                self.cells[y][x].current_state = self.cells_copy[y][x][0]
                self.cells[y][x].next_state = 0
                self.cells[y][x].value = self.cells_copy[y][x][1]
        self.iterationn = 0

    # Function that calculates state for each cell
    def calculate_state(self):
        for y in range(self.height):
            for x in range(self.width):
                self.cells[y][x].calculate_state()

    # Function that calculates state based on slide window rules
    def calculate_state_with_rules(self):
        for y in range(1, self.height-1):
            for x in range(1, self.width-1):
                self.cells[y][x].calculate_state(self.rules)

    # Function that changes state for each cell
    def iteration(self):
        for y in range(self.height):
            for x in range(self.width):
                self.cells[y][x].current_state = self.cells[y][x].next_state
                self.cells[y][x].next_state = 0
        self.iterationn += 1

    # Functions that add appropriate neighbourhood to all cells
    '''
    neighbourhood indexes
    Moore:
    0   3   5
    1   x   6
    2   4   7
    '''

    def moore(self):
        for y in range(1, self.height - 1):
            for x in range(1, self.width - 1):
                neighbours = []
                for yi in range(y - 1, y + 2):
                    for xi in range(x - 1, x + 2):
                        if xi == x and yi == y: continue
                        neighbours.append(self.cells[yi][xi])
                self.cells[y][x].neighbours = neighbours

    '''
    Von Neumann:
        1
    0   x   3
        2
    '''

    def von_neumann(self):
        for y in range(1, self.height - 1):
            for x in range(1, self.width - 1):
                self.cells[y][x].neighbours_add(self.cells[y - 1][x])
                self.cells[y][x].neighbours_add(self.cells[y][x + 1])
                self.cells[y][x].neighbours_add(self.cells[y][x - 1])
                self.cells[y][x].neighbours_add(self.cells[y + 1][x])

    # Save layer to txt file
    def to_file(self, path):
        file = open(os.path.join(path, self.name), "x")
        file.write(self.name + os.linesep)
        file.write(str(self.height) + " " + str(self.width) + os.linesep)
        file.write(self.neighbourhood + os.linesep)
        file.write(os.linesep)
        for y in range(self.height):
            line = ""
            for x in range(self.width):
                line += self.cells[y][x].current_state
            file.write(line + os.linesep)
        file.write(os.linesep)
        for i in range(1, len(self.cells_states)):
            file.write(self.cells_states[i][0] + " " + self.cells_states[i][1] + os.linesep)
        file.write(os.linesep)
        for y in range(self.height):
            for x in range(self.width):
                if self.cells[y][x].current_state != 0:
                    file.write(str(self.cells[y][x].value) + os.linesep)
        file.close()

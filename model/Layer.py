from enum import Enum
from model.Cell import Cell


class Layer:
    columns = 0
    rows = 0
    cells = None
    cells_states = Enum("STATE", ["DEAD", "ALIVE"])

    def __init__(self, columns=100, rows=100, neighbour="", cell_states=[]):
        self.columns = columns
        self.rows = rows
        self.cells = [[Cell() for col in range(columns)] for row in range(rows)]
        self.cells_states = Enum('STATE', cell_states)
        self.add_neighbourhood(neighbour)

    def add_neighbourhood(self, neighbour):
        if neighbour.lower() == "moore":
            self.moore()
        elif neighbour.lower() == "neumann":
            self.von_neumann()
        else:
            raise Exception("No neighbourhood")

    def step(self):
        self.calculate_state()
        self.move()

    def clear(self):
        for x in range(self.columns):
            for y in range(self.rows):
                self.cells[x][y].clear()

    def calculate_state(self):
        for x in range(self.columns):
            for y in range(self.rows):
                self.cells[x][y].calculate_state()

    def change_state(self):
        for x in range(self.columns):
            for y in range(self.rows):
                self.cells[x][y].current_state = self.cells[x][y].next_state
                self.cells[x][y].next_state = self.cells_states.DEFAULT

    def move(self):
        for x in range(self.columns):
            for y in range(self.rows):
                self.cells[x][y].move()

    def print_cell_state(self, x, y):
        print(list(self.cells_states)[self.cells[x][y].current_state])

    def moore(self):
        for x in range(1, self.columns - 1):
            for y in range(1, self.rows - 1):

                for xi in range(x - 1, x + 2):
                    for yi in range(y - 1, y + 2):
                        if xi == x and yi == y: continue
                        self.cells[x][y].neighbours_add(self.cells[xi][yi])

    def von_neumann(self):
        for x in range(1, self.columns - 1):
            for y in range(1, self.rows - 1):
                self.cells[x][y].neighbours_add(self.cells[x - 1][y])
                self.cells[x][y].neighbours_add(self.cells[x][y + 1])
                self.cells[x][y].neighbours_add(self.cells[x][y - 1])
                self.cells[x][y].neighbours_add(self.cells[x + 1][y])

    def value(self):
        value = 0
        for x in range(1, self.columns):
            for y in range(1, self.rows):
                value = self.cells[x][y].current_state
        return value

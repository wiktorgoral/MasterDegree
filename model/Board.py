from model.Cell import Cell


class Board:

    layers_count = 0
    columns = 0
    rows = 0
    cells = None

    def __init__(self, columns =100, rows = 100, layers_count = 3):
        self.columns = columns
        self.rows = rows
        self.layers_count = layers_count
        self.cells = [[[Cell() for col in range(columns)]
                      for row in range(rows)]
                      for layer in range(layers_count)]
        self.add_neighbourhood()

    def add_neighbourhood(self):


    def step(self):
        self.calculate_state()
        self.move()

    def clear(self):
        for layer in range(self.layers_count):
            for row in range(self.rows):
                for column in range(self.columns):
                    self.cells[row][column][layer].clear()

    def calculate_state(self):
        for layer in range(self.layers_count):
            for row in range(self.rows):
                for column in range(self.columns):
                    self.cells[row][column][layer].calculate_state()

    def move(self):
        for layer in range(self.layers_count):
            for row in range(self.rows):
                for column in range(self.columns):
                    self.cells[row][column][layer].move()

    def moore(self):

        for layer in range(self.layers_count):
            for y in range(1, self.rows-1):
                for x in range(1, self.columns-1):

                    for yi in range (y-1, y+2):
                        for xi in range(x-1, x+2):
                            if xi==x and yi==y:continue
                            self.cells[x][y][layer].neighbours_add(self.cells[xi][yi][layer])


    def von_Neumann(self):
        for layer in range(self.layers_count):
            for y in range(1, self.rows-1):
                for x in range(1, self.columns-1):
                    self.cells[x][y][layer].neighbours_add(self.cells[x-1][y][layer])
                    self.cells[x][y][layer].neighbours_add(self.cells[x][y+1][layer])
                    self.cells[x][y][layer].neighbours_add(self.cells[x+1][y][layer])
                    self.cells[x][y][layer].neighbours_add(self.cells[x][y-1][layer])

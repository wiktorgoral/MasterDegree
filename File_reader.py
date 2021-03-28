import copy
import os

from model.Layer import Layer
from model.Board import ModelBoard


def read_layer(name):
    with open(name) as reader:

        name = reader.readline().rstrip('\n')
        size = int(reader.readline().rstrip('\n'))
        cells = [[0 for x in range(size)] for y in range(size)]
        cells_states = []
        neighbourhood = reader.readline().rstrip('\n')

        # read cells
        line = reader.readline()

        for y in range(size):
            line = reader.readline().rstrip('\n')
            for x in range(len(line)):
                cells[y][x] = int(line[x])

        # read cells states
        reader.readline()
        line = reader.readline()
        cells_states.append(("nothing", "white"))
        while line != '\n':
            line = line.rstrip('\n').split()
            cells_states.append((line[0], line[1]))
            line = reader.readline()

        # read cells values
        line = reader.readline()
        values = list()
        while line != "":
            line = line.rstrip('\n')
            values.append(float(line))
            line = reader.readline()

        # Create layer with all parameters
        layer = Layer(name, size, neighbourhood, cells_states)
        i = 0
        for x in range(size):
            for y in range(size):
                layer.cells[x][y].current_state = cells[x][y]
                if cells[x][y] != 0:
                    layer.cells[x][y].value = values[i]
                    i += 1

        return layer


def read_board(folder: str):
    layers = list()
    number_of_files = next(os.walk(folder))[2]
    for file in number_of_files:
        layer = read_layer(os.path.join(folder, file))
        layers.append(layer)
    return ModelBoard(layers)

from typing import List

from model.Layer import Layer


class ModelBoard:

    layers_count = 0
    layers = []
    layer_size = 0
    result = None

    def __init__(self, layers: List[Layer]):
        size = layers[0].size
        for layer in layers:
            if layer.size != size:
                raise Exception("Layers not same size")
        self.layers_count = len(layers)
        self.layer_size = size
        self.layers = layers

    # Iteration step
    def step(self):
        self.calculate_state()
        self.change_state()
        self.resolve_conflicts()

    # Function that changes state for each layer
    def change_state(self):
        for layer in self.layers:
            layer.change_state()

    # Function that clears one layer
    def clear(self, i: int):
        self.layers[i].reset()

    # Function that clears all layers
    def reset(self):
        for layer in self.layers:
            layer.reset()

    # Function that calculates states of all layers
    def calculate_state(self):
        for layer in self.layers:
            layer.calculate_state()

    # Function that checks if cells of coordinates [x y] are occupied
    def occupied(self, x: int, y: int):
        occupied = False
        for layer in self.layers:
            if layer.cells[x][y] == 0:
                continue
            elif layer.cells[x][y] != 0 and occupied is False:
                occupied = True
            elif layer.cells[x][y] != 0 and occupied is True:
                return True
        return False

    # Function that resolves conflict and changes cells accordingly
    def conflict(self, x: int, y: int):
        types = []
        for layer in self.layers:
            types.append(layer.cells[x][y])

    # Function that resolves conflicts
    def resolve_conflicts(self):
        for x in range(self.layer_size):
            for y in range(self.layer_size):
                if self.occupied(x, y):
                    self.conflict(x, y)

    # Function that adds layer
    def add_layer(self, layer: Layer):
        if layer.size != self.layer_size:
            raise Exception("Layers not same size")
        else:
            self.layers.append(layer)

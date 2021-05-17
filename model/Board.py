import os
from copy import deepcopy
from typing import List

from model.Layer import Layer


class ModelBoard:
    layers_count: int = 0
    layers: List[Layer] = []
    layer_size: int = 0
    start_copy = None
    layer_ranking: List[int] = []

    def __init__(self, layers: List[Layer]):
        size = layers[0].size
        for layer in layers:
            if layer.size != size:
                raise Exception("Layers not same size")
        self.layers_count = len(layers)
        self.layer_size = size
        self.layers = layers
        #self.start_copy = deepcopy(self.layers)

    # Iteration step
    # Strategy in which all layers iterate and after resolve conflicts
    def step(self):
        self.iteration_all()
        self.resolve_conflicts(self.layer_ranking)

    # Strategy in which all layers iterate and conflicts are not resolved
    def unaware_strategy(self):
        self.iteration_all()

    # Strategy in which layers take turns
    def player_strategy(self):
        for i in self.layer_ranking:
            self.layers[i].step()
            self.resolve_conflicts(self.layer_ranking)

    # Function that changes state for each layer
    def change_state(self):
        for layer in self.layers:
            layer.iteration()

    # Function that clears one layer
    def clear(self, i: int):
        self.layers[i].clear_all()

    # Function that clears all layers
    def reset(self):
        self.layers = deepcopy(self.start_copy)

    # Function that calculates states of all layers
    def iteration_all(self):
        for layer in self.layers:
            layer.calculate_state()

    # Function that checks if cells of coordinates [x y] in all layers are occupied
    def occupied(self, x: int, y: int):
        occupied = False
        for layer in self.layers:
            if layer.cells[x][y].current_state == 0:
                continue
            elif layer.cells[x][y].current_state != 0 and occupied is False:
                occupied = True
            elif layer.cells[x][y].current_state != 0 and occupied is True:
                return True
        return False

    # Function that resolves conflict and changes cells accordingly in coordinate [x y]
    def conflict(self, x: int, y: int, ranking: List[int]):
        occupied_layers = []
        for i in range(len(self.layers)):
            if self.layers[i].cells[x][y].current_state != 0: occupied_layers.append(i)

        winner = 0
        for i in range(len(ranking)):
            for j in range(len(occupied_layers)):
                if ranking[i] == occupied_layers[j]: winner = i

        for i in range(len(self.layers)):
            if i == winner: continue
            self.layers[i].cells[x][y].current_state = 0

    # Function that finds conflicts in all layers
    def resolve_conflicts(self, ranking: List[int]):
        for x in range(self.layer_size):
            for y in range(self.layer_size):
                if self.occupied(x, y):
                    self.conflict(x, y, ranking)

    # Function that adds layer
    def add_layer(self, layer: Layer):
        if layer.size != self.layer_size:
            raise Exception("Layers not same size")
        else:
            self.layers.append(layer)

    # Save board to folder with txt files
    def to_file(self, path):
        os.mkdir(path)
        for layer in self.layers:
            layer.to_file(path)

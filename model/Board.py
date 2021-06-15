import os
from typing import List

from model.Layer import Layer


class ModelBoard:
    layers_count: int = 0
    layers: List[Layer] = []
    layer_height: int = 0
    layer_width: int = 0
    layer_ranking: List[int] = []

    def __init__(self, layers: List[Layer], strategy: str):
        height = layers[0].height
        width = layers[0].width
        for layer in layers:
            if layer.height != height or layer.width != width:
                raise Exception("Layers are not same size")
        self.layers_count = len(layers)
        self.layer_height = height
        self.layer_width = width
        self.layers = layers
        self.layer_ranking = [i for i in range(self.layers_count)]

        # define layer competition strategy
        if strategy == "unaware strategy":
            self.iteration = self.unaware_strategy
        elif strategy == "player strategy":
            self.iteration = self.player_strategy
        elif strategy == "ranking layers":
            self.iteration = self.all_layers_strategy
        elif strategy == "custom":
            return
        else: raise NameError("No strategy")

    # Strategy in which all layers iterate and then conflicts are resolved based on ranking
    def all_layers_strategy(self):
        for layer in self.layers:
            layer.step()
            self.resolve_conflicts(self.layer_ranking)

    # Strategy in which all layers iterate simultaneously and conflicts are not resolved
    def unaware_strategy(self):
        for layer in self.layers:
            layer.step()

    # Strategy in which each layer iterates and then resolves conflicts as first in ranking
    def player_strategy(self):
        for i in range(self.layers_count):
            self.layers[i].step()
            self.layer_ranking[0] = i
            self.resolve_conflicts(self.layer_ranking)

    # Function that clears one layer
    def clear(self, i: int):
        self.layers[i].clear_all()

    # Function that calculates states of all layers
    # You can implement your own iteration here
    def iteration(self):
        return None

    # Function that checks if cells of coordinates [x y] in all layers are occupied
    def occupied(self, x: int, y: int) -> bool:
        occupied = False
        for layer in self.layers:
            if layer.cells[y][x].current_state == 0:
                continue
            elif layer.cells[y][x].current_state != 0 and occupied is False:
                occupied = True
            elif layer.cells[y][x].current_state != 0 and occupied is True:
                return True
        return False

    # Function that resolves conflict and changes cells accordingly in coordinate [x y]
    def conflict(self, x: int, y: int, ranking: List[int]):
        occupied_layers = []
        for i in range(len(self.layers)):
            if self.layers[i].cells[y][x].current_state != 0: occupied_layers.append(i)

        winner = 0
        for i in range(len(ranking)):
            for j in range(len(occupied_layers)):
                if ranking[i] == occupied_layers[j]: winner = i

        for i in range(len(self.layers)):
            if i == winner: continue
            self.layers[i].cells[y][x].current_state = 0

    # Function that finds conflicts in all layers
    def resolve_conflicts(self, ranking: List[int]):
        for y in range(self.layer_height):
            for x in range(self.layer_width):
                if self.occupied(x, y):
                    self.conflict(x, y, ranking)

    # Function that adds layer
    def add_layer(self, layer: Layer):
        if layer.height != self.layer_height or layer.width != self.layer_width:
            raise Exception("Layers not same size")
        else:
            self.layers.append(layer)

    # Save board to folder with txt files
    def to_file(self, path):
        os.mkdir(path)
        for layer in self.layers:
            layer.to_file(path)

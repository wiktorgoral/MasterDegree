from model.Board import ModelBoard
from view.View import ViewBoard

import numpy as np
import copy


class ViewController:

    # model
    board: ModelBoard = None
    # View
    view: ViewBoard = None

    def __init__(self, board: ModelBoard, size: int):
        self.board = board
        #self.board_copy = copy.deepcopy(board)
        layers_names = list()
        for layer in board.layers:
            layers_names.append(layer.name)
        self.view = ViewBoard(self, layers_names, board.layers[0], board.layer_size, size)

    # Return size of layers
    def get_size(self):
        return self.board.layer_size

    # Return names of layers
    def get_layers_names(self):
        names = []
        for layer in self.board.layers:
            names.append(layer.name)
        return names

    # Return layer's cells
    def layer_to_view(self, i: int):
        return self.board.layers[i]

    # Return all layers cells
    def result_to_view(self):
        result = np.zeros((self.board.layer_size, self.board.layer_size), dtype=str)
        for i in range(1, self.board.layers_count):
            for x in range(self.board.layer_size):
                for y in range(self.board.layer_size):
                    if self.board.layers[i].cells[x][y] == 0: continue
                    result[x][y] = self.board.layers[i].return_cell_state_color(x, y)
        return result

    # Clear layer of cells
    def clear(self, i: int):
        self.board.layers[i].clear_all()

    # Todo implement it
    def reset(self):
        self.board.reset()
        self.layer_to_view(self.view.current_layer_index)

    def iteration(self):
        self.board.iteration_all()
        self.view.change_layer(self.view.current_layer_index)




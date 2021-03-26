from model.Board import ModelBoard
from view.View import ViewBoard

import numpy as np
import copy


class ViewController:

    # model
    board = None
    # View
    view = None

    def __init__(self, board: ModelBoard, size: int):
        self.board = board
        self.board_copy = copy.deepcopy(board)
        self.view = ViewBoard(self, size)

    # return size of layers
    def get_size(self):
        return self.board.layer_size

    # return names of layers
    def get_layers_names(self):
        names = []
        for layer in self.board.layers:
            names.append(layer.name)
        return names

    # return layer's cells
    def layer_to_view(self, i: int):
        return self.board.layers[i]

    # return all layers cells
    def result_to_view(self):
        result = np.zeros((self.board.layer_size, self.board.layer_size), dtype=str)
        for i in range(1, self.board.layers_count):
            for x in self.board.layer_size:
                for y in self.board.layer_size:
                    if self.board.layers[i].cells[x][y] == 0: continue
                    result[x][y] = self.board.layers[i].return_cell_state_color(x, y)
        return result

    # change cell from model to same in view
    def cell_to_model(self, position, cell_type: int, layer: int):
        self.board.layers[layer].change_cell_state(position[0], position[1], cell_type)

    # clear layer of cells
    def clear(self, i: int):
        self.board.layers[i].clear_all()

    # Todo implement it
    def reset(self):
        self.board.reset()
        self.layer_to_view(self.view.current_layer)


    def iteration(self):




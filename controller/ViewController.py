from typing import List

from model.Board import ModelBoard
from model.Layer import Layer
from view.View import ViewBoard


class ViewController:

    # model
    board: ModelBoard = None
    # View
    view: ViewBoard = None

    def __init__(self, board: ModelBoard, size: int):
        self.board = board
        layers_names = list()
        for layer in board.layers:
            layers_names.append(layer.name)
        self.view = ViewBoard(self, layers_names, board.layers[0], size)
        self.view.window.mainloop()

    # Return names of layers
    def get_layers_names(self) -> List[str]:
        names = []
        for layer in self.board.layers:
            names.append(layer.name)
        return names

    # Return layer's cells
    def layer_to_view(self, i: int) -> Layer:
        return self.board.layers[i]

    # Clear layer of cells
    def clear(self, i: int):
        self.board.layers[i].clear_all()

    # Reset all cells in all layers to iteration 0
    def reset_all(self):
        for layer in self.board.layers:
            layer.reset()

    # Iterate board and draw changes
    def iteration(self):
        self.board.iteration()
        self.view.change_layer(self.view.current_layer_index)




from model.Board import ModelBoard
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
        self.view = ViewBoard(self, layers_names, board.layers[0], board.layer_size, size)
        self.view.window.mainloop()

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

    # Clear layer of cells
    def clear(self, i: int):
        self.board.layers[i].clear_all()

    def iteration(self):
        self.board.iteration()
        self.view.change_layer(self.view.current_layer_index)




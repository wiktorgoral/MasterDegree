from File_reader import read_board, read_layer_excel
from controller.ViewController import ViewController
from model.Board import ModelBoard

layer = read_layer_excel("wireworld")
board = ModelBoard(layer, "ranking layers")

controller = ViewController(board, 50)



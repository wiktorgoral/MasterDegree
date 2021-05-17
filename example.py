from File_reader import read_board
from controller.ViewController import ViewController

board = read_board("Test/excel")

controller = ViewController(board, 50)

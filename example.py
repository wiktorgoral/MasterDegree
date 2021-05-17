from File_reader import read_board
from controller.ViewController import ViewController

board = read_board("Examples/Forest Fire/excel")

controller = ViewController(board, 20)

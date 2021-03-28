from File_reader import read_board
from controller.ViewController import ViewController

board = read_board("Test text/test1")

controller = ViewController(board, 50)

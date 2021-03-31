from File_reader import read_board
from controller.ViewController import ViewController

# Todo imports with just import, no from
board = read_board("Test text/test1")

controller = ViewController(board, 50)

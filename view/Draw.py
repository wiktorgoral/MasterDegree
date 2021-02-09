from tkinter import *
import numpy as np


class Board:
    size = 0
    tile_size = 0

    def __init__(self, size=1000, tile_size=10):
        self.window = Tk()
        self.window.geometry(str(size+140)+"x"+str(size))
        self.window.title("Board")
        self.canvas = Canvas(self.window, width=size, height=size)

        self.window.rowconfigure(0, minsize=size, weight=1)
        self.window.columnconfigure(1, minsize=size, weight=1)

        self.buttons = Frame(self.window, height=size)

        listbox_layer_label = Label(self.buttons, text="Select layer:")
        listbox_layer = Listbox(self.buttons, font=('Times', 14), width=5, height=5)
        listbox_layer.insert(1, "1")
        listbox_layer.insert(2, "2")
        listbox_layer.insert(2, "result")

        listbox_cell_label = Label(self.buttons, text="Available cell types:")
        listbox_cell = Listbox(self.buttons, font=('Times', 14), width=5, height=5)
        listbox_cell.insert(1, "fire")
        listbox_cell.insert(2, "water")
        listbox_cell.itemconfig(0, {'bg': 'red'})
        listbox_cell.itemconfig(1, {'bg': 'blue'})

        btn_clear = Button(self.buttons, text="Clear layer")
        btn_reset = Button(self.buttons, text="Reset all")

        listbox_layer_label.grid(row=0, column=0, sticky="ew", padx=5, pady=5)
        listbox_layer.grid(row=1, column=0, sticky="ew", padx=5, pady=5)
        listbox_cell_label.grid(row=2, column=0, sticky="ew", padx=5, pady=5)
        listbox_cell.grid(row=3, column=0, sticky="ew", padx=5, pady=5)
        btn_clear.grid(row=4, column=0, sticky="ew", padx=5, pady=5)
        btn_reset.grid(row=5, column=0, sticky="ew", padx=5)

        self.buttons.grid(row=0, column=0, sticky="ns")
        self.canvas.grid(row=0, column=1, sticky="nsew")

        self.size = size
        self.tile_size = tile_size
        self.board_status = np.zeros(shape=(size // tile_size, size // tile_size))

        self.initialize_board()
        self.canvas.bind("<B1-Motion>", self.click)
        self.canvas.bind("<Button-1>", self.click)

    def mainloop(self):
        self.window.mainloop()

    def initialize_board(self):
        tiles_number = self.size // self.tile_size
        for i in range(tiles_number - 1):
            self.canvas.create_line((i + 1) * self.tile_size, 0,
                                    (i + 1) * self.tile_size, self.size)

        for i in range(tiles_number - 1):
            self.canvas.create_line(0, (i + 1) * self.tile_size,
                                    self.size, (i + 1) * self.tile_size)

    def pixel_to_grid(self, pixel_position):
        pixel_position = np.array(pixel_position)
        return np.array(pixel_position // self.tile_size, dtype=int)

    def grid_to_pixel(self, grid_position):
        grid_position = np.array(grid_position, dtype=int)
        return self.tile_size * grid_position

    def fill_cell(self, grid_position, color):
        pixel_position = self.grid_to_pixel(grid_position)
        self.canvas.create_rectangle(
            pixel_position[0], pixel_position[1],
            pixel_position[0] + self.tile_size, pixel_position[1] + self.tile_size,
            fill=color
        )

    def click(self, event):
        pixel_position = [event.x, event.y]
        grid_position = self.pixel_to_grid(pixel_position)

        self.fill_cell(grid_position)
        self.board_status[grid_position[0]][grid_position[1]] = -1


game_instance = Board(500, 50)
game_instance.mainloop()

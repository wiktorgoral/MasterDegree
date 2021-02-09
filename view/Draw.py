from tkinter import *
import numpy as np


class Board:
    size = 0
    tile_size = 0
    board_status = []
    cell_types = []

    def __init__(self, layers=None, tile_size=10):

        self.size = layers[0].size
        self.tile_size = tile_size
        size_pixel = self.size * self.tile_size
        self.board_status = np.zeros(shape=self.size)
        for i in range(layers):
            self.cell_types.append(layers[i].cell_types)

        # Declaring window
        self.window = Tk()
        self.window.geometry(str(size_pixel + 140) + "x" + str(size_pixel))
        self.window.title("Board")

        # Splitting window into two columns for tooltip and canvas
        self.window.rowconfigure(0, minsize=size_pixel, weight=1)
        self.window.columnconfigure(1, minsize=size_pixel, weight=1)

        # Declaring canvas and tooltip
        self.canvas = Canvas(self.window, width=size_pixel, height=size_pixel)
        self.tooltip = Frame(self.window, height=size_pixel)

        # Laying out canvas and tooltip
        self.tooltip.grid(row=0, column=0, sticky="ns")
        self.canvas.grid(row=0, column=1, sticky="nsew")

        # Initializing canvas
        self.initialize_board()
        self.canvas.bind("<B1-Motion>", self.click)
        self.canvas.bind("<Button-1>", self.click)

        # Declaring layer list selection
        listbox_layer_label = Label(self.tooltip, text="Select layer:")
        self.listbox_layer = Listbox(self.tooltip, font=('Times', 14), width=5, height=5)
        for i in range(layers):
            self.listbox_layer.insert(i + 1, layers[i].name)
        self.listbox_layer.activate(0)

        # Declaring types of cells in layer list selection
        listbox_cell_label = Label(self.tooltip, text="Available cell types:")
        self.listbox_cell = Listbox(self.tooltip, font=('Times', 14), width=5, height=5)
        for i in range(layers[0].cell_types):
            # All cell types in layer
            layer_types = layers[0].cell_types
            self.listbox_cell.insert(i + 1, layer_types[i][0])
            self.listbox_cell.itemconfig(i + 1, {'bg': layer_types[i][1]})
        self.listbox_cell.activate(0)

        # Buttons for clear and reset
        btn_clear = Button(self.tooltip, text="Clear layer")
        btn_reset = Button(self.tooltip, text="Reset all")

        # Laying out buttons in tooltip
        listbox_layer_label.grid(row=0, column=0, sticky="ew", padx=5, pady=5)
        self.listbox_layer.grid(row=1, column=0, sticky="ew", padx=5, pady=5)
        listbox_cell_label.grid(row=2, column=0, sticky="ew", padx=5, pady=5)
        self.listbox_cell.grid(row=3, column=0, sticky="ew", padx=5, pady=5)
        btn_clear.grid(row=4, column=0, sticky="ew", padx=5, pady=5)
        btn_reset.grid(row=5, column=0, sticky="ew", padx=5)
        self.mainloop()

    def mainloop(self):
        self.window.mainloop()

    # Function to create netting for canvas
    def initialize_board(self):
        for i in range(self.size - 1):
            self.canvas.create_line((i + 1) * self.tile_size, 0,
                                    (i + 1) * self.tile_size, self.size * self.tile_size)

        for i in range(self.size - 1):
            self.canvas.create_line(0, (i + 1) * self.tile_size,
                                    self.size * self.tile_size, (i + 1) * self.tile_size)

    # Function to translate pixel position to grid coordinates
    def pixel_to_grid(self, pixel_position):
        pixel_position = np.array(pixel_position)
        return np.array(pixel_position // self.tile_size, dtype=int)

    # Function to translate grid coordinates to pixel position
    def grid_to_pixel(self, grid_position):
        grid_position = np.array(grid_position, dtype=int)
        return self.tile_size * grid_position

    # Function to color appropriate cell in grid
    def fill_cell(self, grid_position, color):
        pixel_position = self.grid_to_pixel(grid_position)
        self.canvas.create_rectangle(
            pixel_position[0], pixel_position[1],
            pixel_position[0] + self.tile_size, pixel_position[1] + self.tile_size,
            fill=color)

    # On-Click function to change cell type
    def click(self, event):
        # Get current mouse coordinates and translate them to grid coordinates
        pixel_position = [event.x, event.y]
        grid_position = self.pixel_to_grid(pixel_position)
        # Get current cell type
        current_layer = self.listbox_layer.curselection()[0]
        current_type = self.listbox_cell.curselection()[0]
        # Fill rectangle with appropriate color and change cell's board status
        self.fill_cell(grid_position, self.cell_types[current_layer][current_type][2])
        self.board_status[grid_position[0]][grid_position[1]] = self.cell_types[current_layer][current_type][0]

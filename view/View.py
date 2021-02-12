from tkinter import *
import numpy as np


class Board:

    layers = []
    size = 0
    tile_size = 0
    board_status = []
    cell_types = []
    current_type = 0
    current_layer = 0
    start = False

    def __init__(self, layers=None, tile_size=10):

        self.layers = layers
        self.size = layers[0].size
        self.tile_size = tile_size
        size_pixel = self.size * self.tile_size
        self.board_status = np.zeros(shape=self.size)
        self.cell_types = layers[0].cell_types

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
        self.draw_netting()
        self.draw_layer("env")

        # Declaring layer list selection
        listbox_layer_label = Label(self.tooltip, text="Select layer:")
        self.listbox_layer = Listbox(self.tooltip, font=('Times', 14), width=5, height=5)
        for i in range(layers):
            self.listbox_layer.insert(i + 1, layers[i].name)
        self.listbox_layer.insert(len(layers), "Result")
        self.listbox_layer.activate(self.current_layer)

        # Declaring types of cells in layer list selection
        listbox_cell_label = Label(self.tooltip, text="Available cell types:")
        self.listbox_cell = Listbox(self.tooltip, font=('Times', 14), width=5, height=5)
        for i in range(self.cell_types):
            self.listbox_cell.insert(i + 1, self.cell_types[i][0])
            self.listbox_cell.itemconfig(i + 1, {'bg': self.cell_types[i][1]})
        self.listbox_cell.activate(self.current_type)

        # Buttons for clear and reset
        button_start = Button(self.tooltip, text="Start")
        button_stop = Button(self.tooltip, text="Stop")
        button_clear = Button(self.tooltip, text="Clear layer")
        button_reset = Button(self.tooltip, text="Reset all")

        # Laying out buttons in tooltip
        button_start.grid(row=0, column=0, sticky="ew", padx=5, pady=5)
        button_stop.grid(row=1, column=0, sticky="ew", padx=5, pady=5)

        listbox_layer_label.grid(row=2, column=0, sticky="ew", padx=5)
        self.listbox_layer.grid(row=3, column=0, sticky="ew", padx=5, pady=5)

        listbox_cell_label.grid(row=4, column=0, sticky="ew", padx=5)
        self.listbox_cell.grid(row=5, column=0, sticky="ew", padx=5, pady=5)

        button_clear.grid(row=6, column=0, sticky="ew", padx=5, pady=5)
        button_reset.grid(row=7, column=0, sticky="ew", padx=5, pady=5)

        # Bind functions with mouse events
        self.canvas.bind("<B1-Motion>", self.click_canvas)
        self.canvas.bind("<Button-1>", self.click_canvas)
        self.listbox_cell.bind("<Button-1>", self.click_type)
        self.listbox_layer.bind("<Button-1>", self.click_layer)
        button_start.bind("<Button-1>", self.click_start)
        button_stop.bind("<Button-1>", self.click_stop)
        button_clear.bind("<Button-1>", self.click_clear)
        button_clear.bind("<Button-1>", self.click_reset)
        self.mainloop()

    def mainloop(self):
        self.window.mainloop()

    '''Draw functions'''

    # Function that creates netting for canvas
    def draw_netting(self):
        for i in range(self.size - 1):
            self.canvas.create_line((i + 1) * self.tile_size, 0,
                                    (i + 1) * self.tile_size, self.size * self.tile_size)

        for i in range(self.size - 1):
            self.canvas.create_line(0, (i + 1) * self.tile_size,
                                    self.size * self.tile_size, (i + 1) * self.tile_size)

    # Function that colors appropriate cell in grid
    def fill_cell(self, grid_position, color, tag=""):
        pixel_position = self.grid_to_pixel(grid_position)
        self.canvas.create_rectangle(
            pixel_position[0], pixel_position[1],
            pixel_position[0] + self.tile_size, pixel_position[1] + self.tile_size,
            fill=color, tag=tag)

    # Todo change to draw input layer
    def draw_layer(self, tag):
        for x in range(self.size):
            for y in range(self.size):
                self.fill_cell([x, y], self.cell_types[self.board_status[x][y]][1], tag)

    '''Logic Functions'''

    # Function that translates pixel position to grid coordinates
    def pixel_to_grid(self, pixel_position):
        pixel_position = np.array(pixel_position)
        return np.array(pixel_position // self.tile_size, dtype=int)

    # Function that translates grid coordinates to pixel position
    def grid_to_pixel(self, grid_position):
        grid_position = np.array(grid_position, dtype=int)
        return self.tile_size * grid_position

    def change_layer(self, layer):
        self.click_stop()
        self.board_status = layer.cells
        self.change_types(layer)
        self.canvas.delete("new")
        self.draw_layer("new")

    def change_types(self, layer):
        self.listbox_cell.delete(0, len(self.cell_types))
        self.cell_types = layer.cells_states
        for i in range(self.cell_types):
            self.listbox_cell.insert(i + 1, self.cell_types[i][0])
            self.listbox_cell.itemconfig(i + 1, {'bg': self.cell_types[i][1]})
        self.current_type = 0
        self.listbox_cell.activate(self.current_type)

    '''Mouse Events Functions'''

    # Todo add controller 
    # On-Click/Mouse-Down function to change cell type
    def click_canvas(self, event):
        # Get current mouse coordinates and translate them to grid coordinates
        pixel_position = [event.x, event.y]
        grid_position = self.pixel_to_grid(pixel_position)

        # Fill rectangle with appropriate color and change cell's board status
        self.fill_cell(grid_position, self.cell_types[self.current_type][0], "new")
        self.board_status[grid_position[0]][grid_position[1]] = self.current_type

    # On-Click function that tracks currently selected cell type
    def click_type(self):
        self.current_type = self.listbox_cell.curselection()[0]

    # On-Click function that tracks currently selected layer
    # Todo add controller instead for storing all layers
    def click_layer(self):
        self.current_layer = self.listbox_layer.curselection()[0]
        if self.current_layer == len(self.layers):
            for layer in self.layers:
                self.draw_layer(layer, "new")
            self.listbox_cell.delete(0, len(self.cell_types))
            self.cell_types = []
            self.current_type = 0
        else:
            self.change_layer(self.layers[self.current_layer])

    # On-Click function that resets current layer
    def click_clear(self):
        self.board_status = np.zeros(shape=self.size)
        self.cell_types = []

    # On-Click function that resets whole simulation
    # Todo add layers clear with controller
    def click_reset(self):
        self.click_clear()

    # On-Click function that starts simulation
    def click_start(self):
        self.start = True

    # On-Click function that stops simulation
    def click_stop(self):
        self.start = False

from tkinter import *
import numpy as np
from typing import List

from controller.ViewController import ViewController


class ViewBoard:

    controller = None
    size = 0
    layers_count = 0
    tile_size = 0
    current_layer = None
    current_type = 0
    current_layer_index = 0
    start = False

    def __init__(self, controller: ViewController, tile_size: int = 10):

        self.controller = controller
        self.size = controller.get_size()
        self.tile_size = tile_size
        size_pixel = self.size * self.tile_size

        self.current_layer_index = 0
        self.current_layer = controller.layer_to_view(self.current_layer_index)
        self.cell_types = self.current_layer.cells_states
        self.start = False

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
        for x in range(self.size):
            for y in range(self.size):
                self.fill_cell([x, y], self.current_layer.cells[x][y], "env")

        # Declaring layer list selection
        listbox_layer_label = Label(self.tooltip, text="Select layer:")
        self.listbox_layer = Listbox(self.tooltip, font=('Times', 14), width=5, height=5)
        layers_names = controller.get_layers_names()
        self.layers_count = len(layers_names)
        for i in range(layers_names):
            self.listbox_layer.insert(i + 1, layers_names[i])
        self.listbox_layer.insert(len(layers_names), "Result")
        self.listbox_layer.activate(self.current_layer_index)

        # Declaring types of cells in layer list selection
        listbox_cell_label = Label(self.tooltip, text="Available cell types:")
        self.listbox_cell = Listbox(self.tooltip, font=('Times', 14), width=5, height=5)
        for i in range(self.cell_types):
            self.listbox_cell.insert(i + 1, self.cell_types[i][0])
            self.listbox_cell.itemconfig(i + 1, {'bg': self.cell_types[i][1]})
        self.current_type = 0
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
    def fill_cell(self, grid_position, color: str, tag: str):
        pixel_position = self.grid_to_pixel(grid_position)
        self.canvas.create_rectangle(
            pixel_position[0], pixel_position[1],
            pixel_position[0] + self.tile_size, pixel_position[1] + self.tile_size,
            fill=color, tag=tag)

    def draw_layer(self, tag: str):
        for x in range(self.size):
            for y in range(self.size):
                if self.current_layer.cells[x][y] == "white": continue
                self.fill_cell([x, y], self.current_layer.cells[x][y], tag)

    '''Logic Functions'''

    # Function that translates pixel position to grid coordinates
    def pixel_to_grid(self, pixel_position):
        pixel_position = np.array(pixel_position)
        return np.array(pixel_position // self.tile_size, dtype=int)

    # Function that translates grid coordinates to pixel position
    def grid_to_pixel(self, grid_position):
        grid_position = np.array(grid_position, dtype=int)
        return self.tile_size * grid_position

    def change_layer(self, layer: int):
        self.click_stop()
        self.current_layer = self.controller.layer_to_view(layer)
        self.change_types(self.current_layer.cells_states)
        self.canvas.delete("new")
        self.draw_layer("new")

    def change_types(self, types: List[tuple]):
        self.listbox_cell.delete(0, len(self.cell_types))
        self.cell_types = types
        for i in range(len(self.cell_types)):
            self.listbox_cell.insert(i + 1, self.cell_types[i][0])
            self.listbox_cell.itemconfig(i + 1, {'bg': self.cell_types[i][1]})
        self.current_type = 0
        self.listbox_cell.activate(self.current_type)

    '''Mouse Events Functions'''

    # On-Click/Mouse-Down function to change cell type
    def click_canvas(self, event):
        if self.start:
            self.start = False
        # Get current mouse coordinates and translate them to grid coordinates
        pixel_position = [event.x, event.y]
        grid_position = self.pixel_to_grid(pixel_position)

        # Fill rectangle with appropriate color and change cell's board status
        self.fill_cell(grid_position, self.cell_types[self.current_type][1], "new")
        self.current_layer.cells[grid_position[0]][grid_position[1]] = self.cell_types[self.current_type][1]

        self.controller.cell_to_model(grid_position, self.current_type, self.current_layer_index)

    # On-Click function that tracks currently selected cell type
    def click_type(self):
        self.current_type = self.listbox_cell.curselection()[0]

    # On-Click function that tracks currently selected layer
    # Todo add result layer
    def click_layer(self):
        self.current_layer_index = self.listbox_layer.curselection()[0]
        if self.current_layer_index == self.layers_count:
            result = self.controller.result_to_view()
            self.listbox_cell.delete(0, len(self.cell_types))
            self.cell_types = []
            self.current_type = 0
        elif self.current_layer_index == 0:
            self.canvas.delete("new")
        else:
            self.change_layer(self.current_layer_index)

    # On-Click function that resets current layer
    def click_clear(self):
        self.start = False
        self.controller.clear(self.current_layer_index)
        self.change_layer(self.current_layer_index)

    # On-Click function that resets whole simulation
    # Todo add layers clear with controller
    def click_reset(self):
        self.start = False
        self.controller.reset()

    # On-Click function that starts simulation
    def click_start(self):
        self.start = True

    # On-Click function that stops simulation
    def click_stop(self):
        self.start = False

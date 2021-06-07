import time
from tkinter import *
import numpy as np
from typing import List

from controller import ViewController
from model.Layer import Layer


class ViewBoard:
    controller: ViewController = None
    size: int = 0
    layers_count: int = 0
    tile_size: int = 0
    current_layer: Layer = None
    current_type: int = 0
    current_layer_index: int = 0
    start: bool = False

    def __init__(self, controller, layers_names: list, layer: Layer, size: int, tile_size: int = 10):

        self.controller = controller
        self.size = size
        self.tile_size = tile_size
        size_pixel = self.size * self.tile_size

        self.current_layer_index = 0
        self.current_layer = layer
        self.cell_types = self.current_layer.cells_states

        # Declaring window
        self.window = Tk()
        self.window.geometry(str(size_pixel + 140) + "x" + str(size_pixel))
        self.window.resizable(width=False, height=False)
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
                self.fill_cell([x, y], self.cell_types[self.current_layer.cells[x][y].current_state][1], "new")

        # Declaring layer list selection
        listbox_layer_label = Label(self.tooltip, text="Select layer:")
        self.listbox_layer = Listbox(self.tooltip, font=('Times', 14), width=5, height=5,
                                     selectmode=SINGLE)
        self.layers_count = len(layers_names)
        for i in range(len(layers_names)):
            self.listbox_layer.insert(i, layers_names[i])
        self.listbox_layer.insert(len(layers_names), "Result")

        # Declaring types of cells in layer list selection
        listbox_cell_label = Label(self.tooltip, text="Available cell types:")
        self.listbox_cell = Listbox(self.tooltip, font=('Times', 14), width=5, height=5,
                                    selectmode=SINGLE)
        for i in range(len(self.cell_types)):
            self.listbox_cell.insert(i, self.cell_types[i][0])
            self.listbox_cell.itemconfig(i, {'bg': self.cell_types[i][1]})
        self.current_type = 0
        self.listbox_cell.selection_set(0)

        # Buttons for clear and reset
        button_start = Button(self.tooltip, text="Start")
        button_stop = Button(self.tooltip, text="Stop")
        button_iterate = Button(self.tooltip, text="Iterate this")
        button_clear = Button(self.tooltip, text="Clear layer")
        button_reset = Button(self.tooltip, text="Reset")
        button_reset_all = Button(self.tooltip, text="Reset all")

        # Laying out buttons in tooltip
        button_start.grid(row=0, column=0, sticky="ew", padx=5, pady=5)
        button_stop.grid(row=1, column=0, sticky="ew", padx=5, pady=5)

        listbox_layer_label.grid(row=2, column=0, sticky="ew", padx=5)
        self.listbox_layer.grid(row=3, column=0, sticky="ew", padx=5, pady=5)

        listbox_cell_label.grid(row=4, column=0, sticky="ew", padx=5)
        self.listbox_cell.grid(row=5, column=0, sticky="ew", padx=5, pady=5)

        button_iterate.grid(row=6, column=0, sticky="ew", padx=5, pady=5)
        button_clear.grid(row=7, column=0, sticky="ew", padx=5, pady=5)
        button_reset.grid(row=8, column=0, sticky="ew", padx=5, pady=5)
        button_reset_all.grid(row=9, column=0, sticky="ew", padx=5, pady=5)

        # Bind functions with mouse events
        self.canvas.bind("<B1-Motion>", self.click_canvas)
        self.canvas.bind("<Button-1>", self.click_canvas)
        self.listbox_cell.bind("<<ListboxSelect>>", self.click_type)
        self.listbox_layer.bind("<<ListboxSelect>>", self.click_layer)
        button_start.bind("<Button-1>", self.click_start)
        button_stop.bind("<Button-1>", self.click_stop)
        button_clear.bind("<Button-1>", self.click_clear)
        button_reset.bind("<Button-1>", self.click_reset)
        button_reset_all.bind("<Button-1>", self.click_reset_all)
        button_iterate.bind("<Button-1>", self.click_iterate)

    # Function that calls iteration on model every 1 sec
    def mainloop(self):
        start = time.time()
        self.controller.iteration()
        if self.start:
            self.window.after(1000 - int(time.time() - start), self.mainloop)

    # Function that calls iteration on current layer every 1 sec
    def iterate(self):
        start = time.time()
        self.current_layer.step()
        self.change_layer(self.current_layer_index)
        if self.start:
            self.window.after(1000 - int(time.time() - start), self.iterate)

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

    # Function draws layer
    def draw_layer(self, tag: str):
        for x in range(self.size):
            for y in range(self.size):
                if self.current_layer.cells[x][y].current_state == 0: continue
                self.fill_cell([x, y], self.cell_types[self.current_layer.cells[x][y].current_state][1], tag)

    '''Logic Functions'''

    # Function that translates pixel position to grid coordinates
    def pixel_to_grid(self, pixel_position):
        pixel_position = np.array(pixel_position)
        return np.array(pixel_position // self.tile_size, dtype=int)

    # Function that translates grid coordinates to pixel position
    def grid_to_pixel(self, grid_position):
        grid_position = np.array(grid_position, dtype=int)
        return self.tile_size * grid_position

    # Function that changes currently displayed layer
    def change_layer(self, layer: int):
        if self.current_layer_index == self.layers_count:
            self.canvas.delete("new")
            for i in range(self.layers_count):
                self.current_layer = self.controller.layer_to_view(i)
                self.change_types(self.current_layer.cells_states)
                self.draw_layer("new")
            self.change_types([])
            return
        self.current_layer = self.controller.layer_to_view(layer)
        self.change_types(self.current_layer.cells_states)
        self.canvas.delete("new")
        self.draw_layer("new")

    # Function that changes currently displayed cell types
    def change_types(self, types: List[tuple]):
        self.listbox_cell.delete(0, len(self.cell_types))
        self.cell_types = types
        for i in range(len(self.cell_types)):
            self.listbox_cell.insert(i, self.cell_types[i][0])
            self.listbox_cell.itemconfig(i, {'bg': self.cell_types[i][1]})
        self.current_type = 0
        self.listbox_cell.select_set(self.current_type)

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
        self.current_layer.cells[grid_position[0]][grid_position[1]].current_state = self.current_type

    # On-Click function that tracks currently selected cell type
    def click_type(self, event):
        if len(self.listbox_cell.curselection()) == 0: return
        self.current_type = self.listbox_cell.curselection()[0]

    # On-Click function that tracks currently selected layer
    def click_layer(self, event):
        # Bug in tkinter sometimes double activates this function
        if len(self.listbox_layer.curselection()) == 0: return

        self.current_layer_index = self.listbox_layer.curselection()[0]
        self.current_type = 0
        self.change_layer(self.current_layer_index)

    # On-Click function that clears current layer
    def click_clear(self, event):
        self.start = False
        self.controller.clear(self.current_layer_index)
        self.change_layer(self.current_layer_index)

    # On-Click function that resets current layer
    def click_reset(self, event):
        self.current_layer.reset()
        self.change_layer(self.current_layer_index)

    # On-Click function that resets all layers
    def click_reset_all(self, event):
        self.controller.reset_all()
        self.change_layer(self.current_layer_index)

    # On-Click function that starts simulation
    def click_start(self, event):
        self.start = True
        self.mainloop()

    # On-Click function that stops simulation
    def click_stop(self, event):
        self.start = False

    # On-Click function that iterates current layer
    def click_iterate(self, event):
        self.start = True
        self.iterate()

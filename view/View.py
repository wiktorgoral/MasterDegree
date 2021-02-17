from tkinter import *
import numpy as np

from controller.ViewController import ViewController


class ViewBoard:

    controller = None
    size = 0
    layers_count = 0
    tile_size = 0
    board_status = []
    cell_types = []
    current_type = 0
    current_layer = 0
    start = False

    def __init__(self, controller: ViewController, tile_size=10):

        self.controller = controller
        self.size = controller.get_size()
        self.tile_size = tile_size
        size_pixel = self.size * self.tile_size

        self.current_layer = 0
        self.board_status = controller.layer_to_view(self.current_layer)
        self.cell_types = controller.types_to_view(self.current_layer)
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
                self.fill_cell([x, y], self.cell_types[self.board_status[x][y]][1], "env")

        # Declaring layer list selection
        listbox_layer_label = Label(self.tooltip, text="Select layer:")
        self.listbox_layer = Listbox(self.tooltip, font=('Times', 14), width=5, height=5)
        layers_names = controller.get_layers_names()
        self.layers_count = len(layers_names)
        for i in range(layers_names):
            self.listbox_layer.insert(i + 1, layers_names[i])
        self.listbox_layer.insert(len(layers_names), "Result")
        self.listbox_layer.activate(self.current_layer)

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
    def fill_cell(self, grid_position, color, tag=""):
        pixel_position = self.grid_to_pixel(grid_position)
        self.canvas.create_rectangle(
            pixel_position[0], pixel_position[1],
            pixel_position[0] + self.tile_size, pixel_position[1] + self.tile_size,
            fill=color, tag=tag)

    def draw_layer(self, tag):
        for x in range(self.size):
            for y in range(self.size):
                if self.board_status[x][y] == 0: continue
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
        self.board_status = self.controller.layer_to_view(layer)
        self.change_types(self.controller.types_to_view(layer))
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
        if self.start:
            self.start = False
        # Get current mouse coordinates and translate them to grid coordinates
        pixel_position = [event.x, event.y]
        grid_position = self.pixel_to_grid(pixel_position)

        # Fill rectangle with appropriate color and change cell's board status
        self.fill_cell(grid_position, self.cell_types[self.current_type][0], "new")
        self.board_status[grid_position[0]][grid_position[1]] = self.current_type

        self.controller.cell_to_model(grid_position, self.current_type, self.current_layer)

    # On-Click function that tracks currently selected cell type
    def click_type(self):
        self.current_type = self.listbox_cell.curselection()[0]

    # On-Click function that tracks currently selected layer
    # Todo dont draw 0 type cells for layers other than env
    def click_layer(self):
        self.current_layer = self.listbox_layer.curselection()[0]
        if self.current_layer == self.layers_count:
            for i in range(1, self.layers_count):
                self.controller.layer_to_view(i)
                self.draw_layer("new")
            self.listbox_cell.delete(0, len(self.cell_types))
            self.cell_types = []
            self.current_type = 0
        elif self.current_layer == 0:
            self.canvas.delete("new")
        else:
            self.change_layer(self.current_layer)

    # On-Click function that resets current layer
    def click_clear(self):
        self.board_status = np.zeros(shape=self.size)
        self.cell_types = []
        self.controller.clear(self.current_layer)

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

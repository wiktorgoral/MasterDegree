from model.Layer import Layer


class Board:

    layers_count = 0
    layers = []
    layer_size = 0

    def __init__(self, layers_count=3, layer_size=100, layers=None):
        self.layers_count = layers_count
        self.layer_size = layer_size
        self.layers = layers
        result = Layer("result", layer_size, "none",)
        self.layers.append()

    def step(self):
        self.calculate_state()

    def clear(self, i):
        self.layers[i].reset()

    def reset(self):
        for layer in self.layers:
            layer.reset()

    def calculate_state(self):
        for layer in self.layers:
            layer.calculate_state()

        value = 0
        for x in range(self.layer_size):
            for y in range(self.layer_size):
                for i in range(self.layers):



    def add_layer(self, layer=None):
        if isinstance(layer, Layer):
            self.layers.append(layer)
        else:
            raise Exception("Object is not layer")
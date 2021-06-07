from typing import List, Tuple


class Cell:
    current_state: int = 0
    next_state: int = 0
    value: float = 0
    neighbours: list = []

    def __init__(self, state: int, **kwargs):
        self.current_state = state
        if "value" in kwargs:
            self.value = kwargs.get("value")
        if "example" in kwargs:
            name = kwargs["example"]
            if name == "forest fire":
                self.calculate_state = self.life_example
            elif name == "game of life":
                self.calculate_state = self.life_example
            elif name == "Langton ant":
                self.calculate_state = self.langton_example
            elif name == "wireworld":
                self.calculate_state = self.wireworld_example
            else:
                return

    # Function that resets cell to base state
    def clear(self):
        self.current_state = 0
        self.next_state = 0
        self.value = 0

    # Transition function
    # You can implement your own transition function here
    def calculate_state(self):
        return 1

    # Function that adds neighbour
    def neighbours_add(self, cell):
        self.neighbours.append(cell)

    # https://en.wikipedia.org/wiki/Conway%27s_Game_of_Life
    # Game of Life with moore neighbourhood
    def life_example(self):
        # States: 0 - dead, 1 - alive
        alive = 0
        for neighbour in self.neighbours:
            alive += neighbour.current_state
        if self.current_state == 1:
            if alive in [2, 3]:
                self.next_state = 1
            else:
                self.next_state = 0
        if self.current_state == 0:
            if alive == 3:
                self.next_state = 1
            else:
                self.next_state = 0

    # https://en.wikipedia.org/wiki/Langton%27s_ant
    # Langton's Ant with moore neighbourhood
    def langton_example(self):
        # States: 1 - white, 2 - black,
        # 3 - ant(up) square (white), 4 - ant(right) square (white),
        # 5 - ant(down) square (white), 6 - ant(left) square (white),
        # 7 - ant(up) square (black), 8 - ant(right) square (black),
        # 9 - ant(down) square (black), 10 - ant(left) square (black)

        # guard against overwriting ants next step
        if self.next_state != 0: return

        # ant is not on current cell
        if self.current_state == 1:
            self.next_state = 1
        elif self.current_state == 2:
            self.next_state = 2

        # calculate ants next step based on direction and if cell was visited
        # ant on white cell
        elif self.current_state == 3:
            self.next_state = 2
            if self.neighbours[6].current_state == 1:
                self.neighbours[6].next_state = 4
            else:
                self.neighbours[6].next_state = 8

        elif self.current_state == 4:
            self.next_state = 2
            if self.neighbours[4].current_state == 1:
                self.neighbours[4].next_state = 5
            else:
                self.neighbours[4].next_state = 9

        elif self.current_state == 5:
            self.next_state = 2
            if self.neighbours[1].current_state == 1:
                self.neighbours[1].next_state = 6
            else:
                self.neighbours[1].next_state = 10

        elif self.current_state == 6:
            self.next_state = 2
            if self.neighbours[3].current_state == 1:
                self.neighbours[3].next_state = 3
            else:
                self.neighbours[3].next_state = 7

        # ant on black cells
        elif self.current_state == 7:
            self.next_state = 1
            if self.neighbours[1].current_state == 2:
                self.neighbours[1].next_state = 10
            else:
                self.neighbours[1].next_state = 6

        elif self.current_state == 8:
            self.next_state = 1
            if self.neighbours[3].current_state == 2:
                self.neighbours[3].next_state = 7
            else:
                self.neighbours[3].next_state = 3

        elif self.current_state == 9:
            self.next_state = 1
            if self.neighbours[6].current_state == 2:
                self.neighbours[6].next_state = 10
            else:
                self.neighbours[6].next_state = 6

        elif self.current_state == 10:
            self.next_state = 1
            if self.neighbours[4].current_state == 2:
                self.neighbours[4].next_state = 9
            else:
                self.neighbours[4].next_state = 5

    # https://en.wikipedia.org/wiki/Wireworld
    # Wireworld with moore neighbourhood
    def wireworld_example(self):
        # States: 0 - nothing, 1 - electron head,
        # 2 - electron tail, 3 - conductor

        if self.current_state == 0:
            self.next_state = 0
        elif self.current_state == 1:
            self.next_state = 2
        elif self.current_state == 2:
            self.next_state = 3

        elif self.current_state == 3:
            heads = 0
            for neighbour in self.neighbours:
                if neighbour.current_state == 1: heads += 1
            if heads in [1, 2]:
                self.next_state = 1
            else:
                self.next_state = 3

    # Sliding window is comparing rule(list) with cell and it's neighbourhood
    # similar to image processing morphological operations
    def sliding_window(self, rules: List[Tuple[List[int], List[int]]]):
        # creation of list that represents cell state and neighbours states
        window = []
        for neighbour in self.neighbours:
            window.append(neighbour.current_state)
        window.insert(int(len(self.neighbours) / 2), self.current_state)

        # comparing rules to window
        for rule in rules:
            match = rule[0]
            result = rule[1]
            flag = True
            for i in range(len(window)):
                if match[i] != window[i]: flag = False
            if flag:
                for i in range(len(result)):
                    if i + 0.5 == len(result) / 2:
                        self.next_state = result[i]
                    else:
                        self.neighbours[i].next_state = result[i]

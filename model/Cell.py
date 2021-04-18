class Cell:
    current_state: int = 0
    next_state: int = 0
    value: float = 0
    neighbours: list = []

    def __init__(self, state: int, neighbours: list, blocked: bool, **value):
        self.value = value.get("value")
        self.current_state = state
        self.neighbours = neighbours
        self.blocked = blocked

    def clear(self):
        self.current_state = 0
        self.next_state = 0
        self.value = 0
        self.blocked = False

    def calculate_state(self):
        return 1

    def neighbours_add(self, cell):
        self.neighbours.append(cell)

    # https://en.wikipedia.org/wiki/Conway%27s_Game_of_Life
    # Game of Life with moore neighbourhood
    def life_example(self):
        # States: 0 - dead, 1 - alive
        value = 0
        for neighbour in self.neighbours:
            value += neighbour.current_state
        if self.current_state == 1 and value in [2, 3]:
            self.next_state = 1
        if self.current_state == 0 and value == 3:
            self.next_state = 1
        else:
            self.next_state = 0

    # https://en.wikipedia.org/wiki/Langton%27s_ant
    # Langton's Ant with moore neighbourhood
    def langton_example(self):
        # States: 0 - white, 1 - black,
        # 2 - ant(up) square (white), 3 - ant(right) square (white),
        # 4 - ant(down) square (white), 5 - ant(left) square (white),
        # 6 - ant(up) square (black), 7 - ant(right) square (black),
        # 8 - ant(down) square (black), 9 - ant(left) square (black)

        # ant is not on current cell
        if self.current_state == 0: self.next_state = 0
        elif self.current_state == 1: self.next_state = 1
        # ant on white cell
        elif self.current_state == 2:
            self.next_state = 1
            if self.neighbours[3].current_state == 0:
                self.neighbours[3].next_state = 3
            else:
                self.neighbours[3].next_state = 7

        elif self.current_state == 3:
            self.next_state = 1
            if self.neighbours[2].current_state == 0:
                self.neighbours[2].next_state = 4
            else:
                self.neighbours[2].next_state = 8
        elif self.current_state == 4:
            self.next_state = 1
            if self.neighbours[0].current_state == 0:
                self.neighbours[0].next_state = 5
            else:
                self.neighbours[0].next_state = 9
        elif self.current_state == 5:
            self.next_state = 1
            if self.neighbours[1].current_state == 0:
                self.neighbours[1].next_state = 2
            else:
                self.neighbours[1].next_state = 6
        # ant on black cells
        elif self.current_state == 6:
            self.next_state = 0
            if self.neighbours[0].current_state == 1:
                self.neighbours[0].next_state = 9
            else:
                self.neighbours[0].next_state = 5
        elif self.current_state == 7:
            self.next_state = 0
            if self.neighbours[1].current_state == 1:
                self.neighbours[1].next_state = 6
            else:
                self.neighbours[1].next_state = 2
        elif self.current_state == 8:
            self.next_state = 0
            if self.neighbours[3].current_state == 1:
                self.neighbours[3].next_state = 9
            else:
                self.neighbours[3].next_state = 5
        elif self.current_state == 9:
            self.next_state = 0
            if self.neighbours[1].current_state == 1:
                self.neighbours[1].next_state = 6
            else:
                self.neighbours[1].next_state = 2

    # https://en.wikipedia.org/wiki/Wireworld
    # Wireworld with moore neighbourhood
    def wireworld_example(self):
        # States: 0 - nothing, 1 - electron head,
        # 2 - electron tail, 3 - conductor

        if self.current_state == 0: self.next_state = 0
        elif self.current_state == 1: self.next_state = 2
        elif self.current_state == 2: self.next_state = 3

        elif self.current_state == 3:
            value = 0
            for neighbour in self.neighbours:
                value += neighbour.current_state

            if value in [1, 2]: self.next_state = 1
            else: self.next_state = 3

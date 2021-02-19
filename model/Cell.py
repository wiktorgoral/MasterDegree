class Cell:

    current_state = 0
    next_state = 0
    value = 0
    neighbours = []

    def __init__(self, state: int = 0, neighbours: list = None, blocked: bool = True):
        self.current_state = state
        self.neighbours = neighbours
        self.blocked = blocked

    def clear(self):
        self.current_state = 0
        self.next_state = 0
        self.value = 0
        self.blocked = False

    def calculate_state(self):

    def neighbours_add(self, cell):
        self.neighbours.append(cell)

    def life_example(self):
        value = 0
        for i in range(len(self.neighbours)):
            if self.neighbours[i]== 1: value+=1
        if self.current_state == 1 and value in [2,3]:
            self.next_state = 1
        if self.current_state == 0 and value == 3:
            self.next_state = 1
        else: self.next_state = 0


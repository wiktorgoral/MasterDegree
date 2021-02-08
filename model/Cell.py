class Cell:

    current_state = 0
    next_state = 0
    '''
    neighbourhood indexes
    Moore:
        1
    0   x   3
        2
        
    Von Neumann:
    0   3   5
    1   x   6
    2   4   7
    '''
    neighbours = list()
    blocked = False

    def __init__(self, state=0, neighbours=None, blocked=True):
        self.current_state = state
        self.neighbours = neighbours
        self.blocked = blocked

    def clear(self):
        self.current_state = 0
        self.next_state = 0
        self.blocked = False

    def calculate_state(self):

    def move(self):

    def neighbours_add(self, cell):
        self.neighbours.append(cell)

    def life_example(self):
        value = 0
        for i in range(self.neighbours):
            if self.neighbours[i]== 1: value+=1
        if self.state == 1 and value in [2,3]:
            next_state = 1
        if self.state == 0 and value == 3:
            next_state = 1
        else: next_state == 0


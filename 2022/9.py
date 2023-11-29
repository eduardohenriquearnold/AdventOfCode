class Rope:
    def __init__(self) -> None:
        self.head = [0, 0]
        self.tail = [0, 0]

    def move_head(self, direction: str, quantity: int):
        axis_directions = {'U':(1, 1), 'D':(1, -1), 'R':(0, 1), 'L':(0, -1)}
        assert direction in axis_directions.keys(), "invalid direction"
        axis, amount = axis_directions[direction]
        
        for _ in range(quantity):
            self.head[axis] += amount
            self.update_tail()

    def update_tail(self):
        diff  = [h-t for h, t in zip(self.head, self.tail)]

        # head is two steps up/down/left/right
        if (diff[0] == 0 or diff[1] == 0) and (abs(diff[0])>1 or abs(diff[1])>1):
            direction = [d/max((abs(x) for x in diff)) for d in diff]
            self.tail = [t + dir for t, dir in zip(self.tail, direction)]
        #TODO: other cases

        
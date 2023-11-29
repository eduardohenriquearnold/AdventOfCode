class Board:
    def __init__(self, lines) -> None:
        self.numbers = {} # number -> (i,j) position in board
        self.marked = {}  # (i,j) position -> 0/1 (un-marked/marked)

        for i, line in enumerate(lines):
            for j, number in enumerate(line.strip().replace('  ', ' ').split(' ')):
                number = int(number)
                self.numbers[number] = (i, j)
                self.marked[(i,j)] = 0

    def draw(self, number) -> None:
        if number in self.numbers:
            idx = self.numbers[number]
            self.marked[idx] = 1

    def won(self) -> bool:
        n = int(len(self.marked)**0.5)
        for i in range(n):
            rowsum, colsum = 0, 0
            for j in range(n):
                rowsum += self.marked[(i,j)]
                colsum += self.marked[(j,i)]
            if max(rowsum, colsum) == n:
                return True
        return False
    
    def sum_unmarked(self) -> int:
        return sum([number for number, idx in self.numbers.items() if self.marked[idx] == 0])

def loader(path):
    '''Loads input data'''

    with open(path, 'r') as f:
        lines = f.readlines()

    draws = map(int, lines[0].rstrip().split(','))

    boards = []
    buffer = []
    for line in lines[2:]:
        if line == '\n':
            boards.append(Board(buffer))
            buffer.clear()
        else:
            buffer.append(line)

    return draws, boards


def solve():
    draws, boards = loader('4/input.txt')

    win_scores = []

    for number in draws:
        for board in boards:
            board.draw(number)
            if board.won():
                score = number * board.sum_unmarked()
                win_scores.append(score)

                # remove dics to prevent this board to keep 'playing'
                board.numbers = {}
                board.marked = {}

    return win_scores[0], win_scores[-1]
 
if __name__ == '__main__':
    r1, r2 = solve()
    print(f'Part1: {r1}')
    print(f'Part2: {r2}')
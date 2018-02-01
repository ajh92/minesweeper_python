from random import shuffle


marks = {'opened': '_',
         'unknown': 'x',
         'maybe': '?',
         'flagged': '*',
         'mine': '!'}


class Difficulty:
    def __init__(self, x, y, num_of_mines):
        self.x = x
        self.y = y
        self.num_of_mines = num_of_mines


class Cell:
    def __init__(self, is_mine, mark):
        self.is_mine = is_mine
        self.mark = mark


class Board:
    def __init__(self, difficulty, starting_cell_coords):
        self.difficulty = difficulty
        board = [[None for _ in range(difficulty.x)]
                 for _ in range(difficulty.y)]

        coords = [(x, y) for x in
                  range(difficulty.x) for y in range(difficulty.y)]

        values = [True for _ in range(difficulty.num_of_mines)]
        num_to_fill = difficulty.x * difficulty.y - difficulty.num_of_mines - 1
        values = values + [False for _ in range(num_to_fill)]

        shuffle(values)

        for coord_pair in coords:
            if coord_pair == starting_cell_coords:
                board[coord_pair[0]][coord_pair[1]] = Cell(False,
                                                           marks['opened'])
            else:
                board[coord_pair[0]][coord_pair[1]] = Cell(values.pop(),
                                                           marks['unknown'])

        self.board = board
        self.open_cell_and_reveal(starting_cell_coords)

    def open_cell_and_reveal(self, cell_coords, seen_cells=[]):
        seen_cells.append(cell_coords)

        neighbors = self.get_neighbors(cell_coords)

        for neighbor in neighbors:
            if self.get_cell_from_coords(neighbor).is_mine:
                count_str = str(self.get_display_count(neighbors))
                self.get_cell_from_coords(cell_coords).mark = count_str
                return

        self.board[cell_coords[0]][cell_coords[1]].mark = marks['opened']

        for neighbor in neighbors:
            if neighbor not in seen_cells:
                self.open_cell_and_reveal(neighbor, seen_cells)

    def get_neighbors(self, cell_coords):
        return [x for x in [(cell_coords[0] - 1, cell_coords[1]),
                            (cell_coords[0] + 1, cell_coords[1]),
                            (cell_coords[0], cell_coords[1] - 1),
                            (cell_coords[0], cell_coords[1] + 1),
                            (cell_coords[0] - 1, cell_coords[1] - 1),
                            (cell_coords[0] - 1, cell_coords[1] + 1),
                            (cell_coords[0] + 1, cell_coords[1] - 1),
                            (cell_coords[1] + 1, cell_coords[1] + 1)]
                if not (x[0] < 0
                        or x[0] >= self.difficulty.x
                        or x[1] < 0
                        or x[1] >= self.difficulty.y)]

    def get_cell_from_coords(self, coords):
        return self.board[coords[0]][coords[1]]

    def get_display_count(self, neighbors):
        x = 0
        for coords in neighbors:
            if self.get_cell_from_coords(coords).is_mine:
                x += 1
        return x

    def get_board_display(self):
        b = ''
        for x in range(self.difficulty.x):
            for y in range(self.difficulty.y):
                b += self.board[x][y].mark
            b += '\n'
        return b

    def get_board_contents(self):
        b = ''
        for x in range(self.difficulty.x):
            for y in range(self.difficulty.y):
                b += str(self.board[x][y].is_mine) + ' '
            b += '\n'
        return b

    def make_move(self, cell_coords):
        if self.board[cell_coords[0]][cell_coords[1]]:
            return False
        else:
            self.open_cell_and_reveal(cell_coords)
            return True

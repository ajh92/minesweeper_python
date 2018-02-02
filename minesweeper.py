from random import shuffle
from sys import exit


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
        b = "  " + " ".join([str(x).zfill(2) for x in range(self.difficulty.x)])
        b += "\r\n"
        for y in range(self.difficulty.y):
            b += str(y).zfill(2) + " "
            for x in range(self.difficulty.x):
                b += self.board[x][y].mark + "  "
            b += '\n'
        return b

    def get_board_contents(self):
        b = ''
        for x in range(self.difficulty.x):
            for y in range(self.difficulty.y):
                b += str(self.board[x][y].is_mine) + ' '
            b += '\n'
        return b

    def mark_cell(self, cell_coords, mark):
        self.board[cell_coords[0]][cell_coords[1]].mark = mark

    def open_cell(self, cell_coords):
        if self.board[cell_coords[0]][cell_coords[1]].is_mine:
            self.reveal_mines()
            return False
        else:
            self.open_cell_and_reveal(cell_coords)
            return True
    def reveal_mines(self):
        for x in range(self.difficulty.x):
            for y in range(self.difficulty.y):
                if self.board[x][y].is_mine:
                    self.board[x][y].mark = marks["mine"]


class Game:

    GREETING = 'Welcome to Minesweeper. Please Select a difficulty -- (e)asy, (m)edium, (h)ard. Type quit to quit.'

    def prompt(self):
        print(">> ", end="")

    def greet(self):
        print(Game.GREETING)

    def start_game(self, difficulty):
        self.prompt()
        print("Enter starting cell:")
        self.prompt()
        cell_str = input()
        cell = tuple(int(x) for x in cell_str.split(","))
        board = Board(difficulty, cell)
        print(board.get_board_display())
        self.game_loop(board)

    def main_prompt(self):
        main_commands = {'e': lambda: self.start_game(Difficulty(9, 9, 10)),
                         'm': lambda: self.start_game(Difficulty(16, 16, 40)),
                         'h': lambda: self.start_game(Difficulty(16, 30, 99)),
                         'quit': exit}
        self.prompt()
        command = input()
        while command not in main_commands:
            print("Invalid command. Valid commands are: " +
                  ', '.join(map(str, main_commands.keys())))
            self.prompt()
            command = input()
        main_commands[command]()

    def game_loop(self, board):
        ok = True
        while ok:
            self.prompt()
            command = input()
            command = tuple(int(x) for x in command.split(","))
            ok = board.open_cell(command)
            if not ok:
                print("YOU LOSE!")
            print(board.get_board_display())
            
g = Game()
g.greet()
g.main_prompt()

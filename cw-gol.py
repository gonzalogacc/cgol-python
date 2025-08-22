import argparse
import cProfile
import collections
import random
from array import array
from time import sleep

"""
## Rules
- A living cell dies if it has fewer than two living neighboring cells.
- A living cell with two or three living neighbors lives on.
- A living cell with more than three living neighboring cells dies in the next time step.
- A dead cell is revived if it has exactly three living neighboring cells.
"""
Cell = collections.namedtuple("Cell", ['x', 'y'])
LIVE_CELL_SYMBOL = 'o'
DEAD_CELL_SYMBOL = ' '
class Board:
    board: array[int]
    temp_board: array[int]

    def __init__(self, board_size: int):
        self.board_size = board_size
        self.board = self.make_board(board_size)
        self.temp_board = self.make_board(board_size)

    @staticmethod
    def make_board(board_size: int) -> array[int]:
        return array('I', [0 for _ in range(board_size*board_size)])

    def draw_board(self, title: str = "") -> None:
        print(chr(27) + "[2J")
        print(chr(27) + "[1;1f")
        board_string = ""
        for i, line in enumerate(self.board):
            if i % self.board_size == 0:
                board_string+='\n'
                print()
            if line:
                board_string+=f"{LIVE_CELL_SYMBOL} "
            else:
                board_string += f"{DEAD_CELL_SYMBOL} "
        print(title)
        print(board_string)

    def set_cell(self, cell: Cell, value: bool) -> None:
        self.board[cell.y*self.board_size + cell.x] = value

    def set_temp_cell(self, cell: Cell, value: bool) -> None:
        self.temp_board[cell.y*self.board_size + cell.x] = value

    def get_cell(self, cell: Cell) -> bool:
        if cell.y < 0 or cell.y >= self.board_size or cell.x < 0 or cell.x >= self.board_size:
            raise IndexError(f"Index out of range cell: {cell}")
        return self.board[cell.y*self.board_size + cell.x]

    def zero_temp_board(self) -> None:
        for i in range(len(self.temp_board)):
            self.temp_board[i] = False

    def random_cells(self, cell_number: int) -> set[Cell]:
        cells = set()
        for _ in range(cell_number):
            cells.add(Cell(x=random.choice(range(self.board_size)), y=random.choice(range(self.board_size))))
        return cells


    def number_of_neighbours(self, center: Cell) -> int:
        """Given a cell returns the number of live cells around the center"""

        top_left = Cell(x=center.x-1, y=center.y-1)
        top_middle = Cell(x=center.x, y=center.y-1)
        top_right = Cell(x=center.x+1, y=center.y-1)
        middle_left = Cell(x=center.x-1, y=center.y)
        middle_right = Cell(x=center.x+1, y=center.y)
        bottom_left = Cell(x=center.x-1, y=center.y+1)
        bottom_middle = Cell(x=center.x, y=center.y+1)
        bottom_right = Cell(x=center.x+1, y=center.y+1)

        return sum(
            [
                self.get_cell(c)
                for c in [top_left, top_middle, top_right, middle_left, middle_right, bottom_left, bottom_middle, bottom_right]
                if 0 <= c.x < self.board_size and 0 < c.y < self.board_size
            ]
        )

    def apply_rules_to_cell(self, cell: Cell) -> bool:
        """ Returns true is the cell lives, false otherwise
        """
        nn = self.number_of_neighbours(cell)
        if self.get_cell(cell):
            # cell is alive
            if nn < 2:
                return False
            elif nn <= 3:
                return True
            else:
                return False
        else:
            # cell is dead
            if nn == 3:
                return True
        return False

    def set_random_board(self, initial_cell_count: int = 10) -> None:
        """ Setup random cells in the board """
        [self.set_cell(cell, True) for cell in self.random_cells(initial_cell_count)]

    def board_step(self) -> None:
        self.zero_temp_board()
        for cell_idx in range(len(self.board)):
            py = cell_idx // self.board_size
            px = cell_idx - ( py * self.board_size)

            cell = Cell(x=px, y=py)
            self.set_temp_cell(cell, self.apply_rules_to_cell(cell))

        # Could find a better way to transfer the array
        for i, nv in enumerate(self.temp_board):
            self.board[i] = nv

    def run(self, periods: int = 10, sleep_time: float = .2) -> None:
        for step in range(1, periods+1):
            title = f"-- Generation: {step} --"
            self.board_step()
            self.draw_board(title)
            sleep(sleep_time)

    def set_blinker(self, center: Cell) -> None:
        # linea vertical de 3
        self.set_cell(Cell(x=center.x, y=center.y), True)
        self.set_cell(Cell(x=center.x, y=center.y-1), True)
        self.set_cell(Cell(x=center.x, y=center.y+1), True)

def main(board_size: int, freq: float, periods: int, saturation: float):
    board = Board(board_size)
    board.set_random_board(int(board_size*board_size*saturation))
    board.draw_board("-- Initial board --")
    input()
    board.run(periods=periods, sleep_time=freq)


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Launch board")
    parser.add_argument("-b", "--board_size", type=int, default=25)
    parser.add_argument("-f", "--freq", help="1/f refresh per second.", type=float, default=.2)
    parser.add_argument("-g", "--generations", help="Number of generations", type=int, default=100)
    parser.add_argument("-s", "--saturation", help="% of the board populated at start", type=float, default=.4)
    args = parser.parse_args()

    # cProfile.run('main()', sort='cumtime')
    main(args.board_size, args.freq, args.generations, args.saturation)

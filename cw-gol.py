import argparse
import cProfile
import collections
import random
import timeit
from array import array
from time import sleep, perf_counter

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
        """Create a flat array representing a 2D board.

        Args:
            board_size: Size of the square board.

        Returns:
            Flat array initialized with zeros (all dead cells).
        """
        return array('I', [0 for _ in range(board_size*board_size)])

    def draw_board(self, title: str = "") -> None:
        """Render the board to terminal.

        Args:
            title: Optional title to display above the board.
        """
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
        """Set a cell's state.

        Args:
            cell: Cell coordinates.
            value: True for alive, False for dead.
        """
        self.board[cell.y*self.board_size + cell.x] = value

    def zero_temp_board(self) -> None:
        """Clear the temporary board by setting all cells to dead."""
        for i in range(len(self.temp_board)):
            self.temp_board[i] = False

    def random_cells(self, cell_number: int) -> set[Cell]:
        """Generate a set of random cell coordinates.

        Args:
            cell_number: Number of random cells to generate.

        Returns:
            Set of Cell objects with random coordinates.
        """
        cells = set()
        for _ in range(cell_number):
            cells.add(Cell(x=random.choice(range(self.board_size)), y=random.choice(range(self.board_size))))
        return cells

    def set_random_board(self, initial_cell_count: int = 10) -> None:
        """Populate the board with random living cells.

        Args:
            initial_cell_count: Number of cells to set alive randomly.
        """
        [self.set_cell(cell, True) for cell in self.random_cells(initial_cell_count)]

    def number_of_neighbours(self, cy: int, cx: int) -> int:
        """Count living neighbors around a cell.

        Args:
            cy: Y coordinate (row) of center cell.
            cx: X coordinate (column) of center cell.

        Returns:
            Number of living neighbors (0-8).
        """
        count = 0
        board = self.board
        size = self.board_size

        # Search neighbouring cells
        for dy in [-1, 0, 1]:
            for dx in [-1, 0, 1]:
                if dx == 0 and dy == 0:
                    # ignore central cell
                    continue
                nx, ny = cx + dx, cy + dy
                if 0<=nx< size and 0<=ny<size:
                    count += board[ny*size+nx]

        return count

    def board_step(self) -> None:
        """Execute one generation of Conway's Game of Life.

        Applies Conway's rules to every cell and generates the next board state.
        """
        self.zero_temp_board()
        size = self.board_size
        for cell_idx in range(len(self.board)):
            py = cell_idx // size
            px = cell_idx - ( py * size)

            nn = self.number_of_neighbours(py, px)
            is_alive = self.board[py * size + px]
            if is_alive:
                new_value = 2 <= nn <= 3
            else:
                new_value = nn == 3
            self.temp_board[py * size + px] = new_value

        self.board, self.temp_board = self.temp_board, self.board

    def run(self, periods: int = 10, sleep_time: float = .2) -> None:
        """Run the simulation for a specified number of generations.

        Args:
            periods: Number of generations to simulate.
            sleep_time: Time to sleep between generations.
        """
        for step in range(1, periods+1):
            title = f"-- Generation: {step} --"
            self.board_step()
            self.draw_board(title)
            sleep(sleep_time)

    def set_blinker(self, center: Cell) -> None:
        """Set up a blinker pattern (3-cell vertical oscillator).

        Args:
            center: Center cell of the blinker pattern.
        """
        # linea vertical de 3
        self.set_cell(Cell(x=center.x, y=center.y), True)
        self.set_cell(Cell(x=center.x, y=center.y-1), True)
        self.set_cell(Cell(x=center.x, y=center.y+1), True)

def main(board_size: int, freq: float, periods: int, saturation: float):
    """Run Game of Life simulation with specified parameters.

    Args:
        board_size: Size of the square board.
        freq: Refresh frequency (unused in this version).
        periods: Number of generations to simulate.
        saturation: Initial population density (0.0 to 1.0).
    """
    board = Board(board_size)
    board.set_random_board(int(board_size*board_size*saturation))
    board.run(periods=periods, sleep_time=freq)


if __name__ == "__main__":
    # cProfile.run('main(20, .2, 101, .3)', sort='cumtime')
    # t1_start = perf_counter()
    # main(20, .2, 101, .3)
    # t1_stop = perf_counter()
    # print("Elapsed time:", t1_stop, t1_start)
    # print("Elapsed time during the whole program in seconds:", t1_stop - t1_start)

    parser = argparse.ArgumentParser(description="Launch board")
    parser.add_argument("-b", "--board_size", type=int, default=25)
    parser.add_argument("-f", "--freq", help="1/f refresh per second.", type=float, default=.2)
    parser.add_argument("-g", "--generations", help="Number of generations", type=int, default=100)
    parser.add_argument("-s", "--saturation", help="% of the board populated at start", type=float, default=.4)
    args = parser.parse_args()
    main(args.board_size, args.freq, args.generations, args.saturation)

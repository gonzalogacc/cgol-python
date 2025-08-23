from pathlib import Path

import pytest

from cwgol import Board


@pytest.mark.parametrize("filename, len_cells, bounding_box", [
    ('blinker.cells', 3, 3),
    ('glider.cells', 5, 3),
    ('arrows.cells', 10, 5),
    ('6bits.cells', 49, 40),
])
def test_load_figure(filename, len_cells, bounding_box):
    input_figure_path = Path(__file__).parent / filename
    cells, bb = Board.load_file_figure(str(input_figure_path))
    assert len(cells) == len_cells
    assert bb == bounding_box
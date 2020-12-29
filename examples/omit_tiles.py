import os
import sys
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
from hex_maze import Board

board = Board(6, 8)

# must be neighbour tiles
NUMBER_1 = (
    (0, 1),
    (1, 1),
    (2, 0),
    (2, 1),
    (2, 2),
    (2, 3),
)

board.omit_tiles(NUMBER_1, offset_x=1, offset_y=1)

board.shuffle()
board.to_svg(size=10, tile_margin=2)

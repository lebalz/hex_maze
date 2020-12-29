import os
import sys
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
from hex_maze import Board

LETTER_2 = (
    (0, 0),
    (1, 0),
    (2, 0),
    (2, 1),
    (1, 2),
    (0, 2),
    (0, 3),
    (1, 3),
    (2, 3),
)
LETTER_1 = (
    (0, 1),
    (1, 1),
    (2, 0),
    (2, 1),
    (2, 2),
    (2, 3),
)
LETTER_0 = (
    (0, 0),
    (1, 0),
    (2, 0),
    (2, 1),
    (2, 2),
    (1, 3),
    (0, 2),
    (0, 1)
)

INNER_0 = (
    (1, 1),
    (1, 2)
)

panel = Board(18, 8)


panel.omit_tiles(LETTER_2, offset_x=1, offset_y=1)
panel.omit_tiles(LETTER_0, offset_x=5, offset_y=1)
panel.omit_tiles(INNER_0, offset_x=5, offset_y=1)
panel.omit_tiles(LETTER_2, offset_x=9, offset_y=2)
panel.omit_tiles(LETTER_1, offset_x=13, offset_y=1)

panel.shuffle()
panel.to_svg('hello_2021.svg')

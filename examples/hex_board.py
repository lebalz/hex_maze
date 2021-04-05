import os
import sys
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
from hex_maze import Board

panel = Board(9, 9, entry_pos=(0, 2))
panel[4][4].omit()

panel.omit_tiles(
    [
        (0, 0),
        (0, 1),
        (1, 1),
        (0, 0),
        (1, 0),
        (2, 0),
        (3, 0)
    ]
)
panel.omit_tiles(
    [
        (0, 7),
        (0, 8),
        (1, 8),
        (2, 8)
    ]
)
panel.omit_tiles(
    [
        (8, 8),
        (8, 7),
        (7, 8),
        (6, 8),
    ]
)
panel.omit_tiles(
    [
        (8, 0),
        (8, 1),
        (7, 1),
        (8, 0),
        (7, 0),
        (6, 0),
        (5, 0),
    ]
)

panel.shuffle()
print('shuffle done')
panel.to_svg('hexa.svg')

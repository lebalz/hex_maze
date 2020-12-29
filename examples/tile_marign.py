import os
import sys
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
from hex_maze import Board

b = Board(15, 10)
b.shuffle()
b.to_svg(size=20, tile_margin=2)

import os
import sys
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
from hex_maze import Board

b = Board(10, 10)
b.shuffle()
b.turtle_draw_in_one_piece()

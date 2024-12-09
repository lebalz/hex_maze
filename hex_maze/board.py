from __future__ import annotations
import sys
from .tile import Tile
from typing import Union, List, Tuple
import random
from datetime import datetime
from turtle import *
from pathlib import Path
random.seed(datetime.timestamp(datetime.now()))


class Board:
    '''
    the tiles of a grid are indexed as follows (x, y):

          x (major)
        ----->
      |        /---\     /---\     /---\
    y |       / 1,0 \---/ 3,0 \---/ 5,0 \    <--- lifted
      |   /---\     /---\     /---\     /
      v  / 0,0 \---/ 2,0 \---/ 4,0 \---/     <--- baseline
         \     /---\     /---\     /---\
          \---/ 1,1 \---/ 3,1 \---/ 5,1 \
          /---\     /---\     /---\     /
         / 0,1 \---/ 2,1 \---/ 4,1 \---/
         \     /---\     /---\     /---\
          \---/ 1,2 \---/ 3,2 \---/ 5,1 \
    '''
    _board: List[List[Tile]]
    entry: Tuple[int, int]
    exit: Tuple[int, int]
    _path: List[Tile] = []

    def __init__(self, dimx: int, dimy: int, entry_pos: Tuple[int, int] = (0, 0), exit_pos: Tuple[int, int] = (-1, -1)) -> None:
        self._board = []
        self.entry = entry_pos
        exit_x = exit_pos[0] if exit_pos[0] >= 0 else dimx + exit_pos[0]
        exit_y = exit_pos[1] if exit_pos[1] >= 0 else dimy + exit_pos[1]
        self.exit = (exit_x, exit_y)
        for x in range(dimx):
            self._board.append([])
            for y in range(dimy):
                self._board[x].append(Tile(x, y, self))

    @property
    def dim_x(self):
        return len(self._board)

    @property
    def dim_y(self):
        return len(self._board[0])

    @property
    def entry_tile(self) -> Tile:
        return self._board[self.entry[0]][self.entry[1]]

    @property
    def exit_tile(self) -> Tile:
        return self._board[self.exit[0]][self.exit[1]]

    def __getitem__(self, x: int) -> List[Tile]:
        return self._board[x]

    def __setitem__(self, x: int, value: List[Tile]):
        self._board[x] = value

    def top(self, tile: Tile) -> Union[Tile, None]:
        if tile.y < 1:
            return None
        return self._board[tile.x][tile.y - 1]

    def bottom(self, tile: Tile) -> Union[Tile, None]:
        if tile.y >= self.dim_y - 1:
            return None
        return self._board[tile.x][tile.y + 1]

    def top_right(self, tile: Tile) -> Union[Tile, None]:
        if tile.x >= self.dim_x - 1:
            return None
        if tile.is_baseline:
            return self._board[tile.x + 1][tile.y]
        elif tile.y > 0:
            return self._board[tile.x + 1][tile.y - 1]

    def top_left(self, tile: Tile) -> Union[Tile, None]:
        if tile.x <= 0:
            return None
        if tile.is_baseline:
            return self._board[tile.x - 1][tile.y]
        elif tile.y > 0:
            return self._board[tile.x - 1][tile.y - 1]

    def bottom_right(self, tile: Tile) -> Union[Tile, None]:
        if tile.x >= self.dim_x - 1:
            return None
        if tile.is_lifted:
            return self._board[tile.x + 1][tile.y]
        elif tile.y < self.dim_y - 1:
            return self._board[tile.x + 1][tile.y + 1]

    def bottom_left(self, tile: Tile) -> Union[Tile, None]:
        if tile.x <= 0:
            return None
        if tile.is_lifted:
            return self._board[tile.x - 1][tile.y]
        elif tile.y < self.dim_y - 1:
            return self._board[tile.x - 1][tile.y + 1]

    def reset(self):
        for x in range(self.dim_x):
            for y in range(self.dim_y):
                self[x][y].reset()

    def shuffle(self):
        self._path = []
        start = self.entry_tile
        current = start
        while True:
            current = self.join_next(current)
            if current is None:
                print('current was None!')
                break

    def join_next(self, current: Tile) -> Union[Tile, None]:
        opts = current.untaken_neighbours
        if len(opts) > 0:
            tile_to_enter = random.choice(opts)
            print(current.x, current.y)
            current.join(tile_to_enter)
            self._path.append(tile_to_enter)
            return tile_to_enter
        elif len(self._path) > 1:
            self._path.pop()
            return self.join_next(self._path[-1])

    def configure(self, size: float = 10, tile_margin: float = 0):
        for x in range(self.dim_x):
            for y in range(self.dim_y):
                self[x][y].configure(size=size, margin=tile_margin)

    def turtle_draw(self, size: float = 10, tile_margin: float = 0, open_entry: bool = True, enumerate: bool = False):
        if open_entry:
            self.entry_tile._walls[0] = False
            self.exit_tile._walls[3] = False
        self.configure(size=size, tile_margin=tile_margin)
        Screen().tracer(1, 0)
        for x in range(self.dim_x):
            for y in range(self.dim_y):
                self[x][y].turtle_draw()
                if enumerate:
                    penup()
                    goto(*self[x][y].center)
                    write(f'{x},{y}')
        Screen().exitonclick()

    def turtle_draw_in_one_piece(self, size: float = 10, tile_margin: float = 0):
        self.configure(size=size, tile_margin=tile_margin)
        Screen().tracer(1, 0)
        current = self.entry_tile
        wall_idx = 0
        done = False
        while True:
            cnt = 0
            while current.turtle_draw_wall(wall_idx):
                wall_idx = (wall_idx + 1) % 6
                cnt = cnt + 1
                if cnt > 5:
                    break
            if done:
                break
            current = current.negibour_at(wall_idx)
            wall_idx = (wall_idx + 4) % 6
            if current.x == 0 and current.y == 0:
                done = True
        hideturtle()
        Screen().exitonclick()

    def to_svg(self, name: str = None, size: float = 10, stroke_width:float=3, tile_margin: float = 0, add_frame: bool = True):
        if name is None:
            name = f'maze_{self.dim_x}x{self.dim_y}.svg'
        if not name.endswith('.svg'):
            name += '.svg'
        self.configure(size=size, tile_margin=tile_margin)
        current = self.entry_tile
        done = False
        height = (self.dim_y + 1) * current.height
        width = (self.dim_x + 1) * 3 * current.width / 4

        with open(Path(sys.argv[0]).parent.joinpath(name), 'w') as f:
            f.write(f'''\
<?xml version="1.0"?>
    <svg version="1.1" xmlns="http://www.w3.org/2000/svg" xmlns:xlink="http://www.w3.org/1999/xlink" height="{height}" width="{width}">
        <polyline stroke-width="{stroke_width}" fill="none" stroke="black" stroke-linecap="round" stroke-linejoin="round" points="
''')

            wall_idx = 0
            while True:
                cnt = 0
                while current.write_wall_to_svg(f, wall_idx):
                    wall_idx = (wall_idx + 1) % 6
                    cnt = cnt + 1
                    if cnt > 5:
                        break
                if done:
                    break
                current = current.negibour_at(wall_idx)
                wall_idx = (wall_idx + 4) % 6
                if current.x == self.entry[0] and current.y == self.entry[1]:
                    done = True
            f.write('"/>\n')
            if add_frame:
                f.write(f'''<polyline stroke-width="{stroke_width}" fill="none" stroke="black" points="0,0 {width},0 {width},{height} 0,{height} 0,0" />\n''')
            f.write('''</svg>''')

    def omit_tile_at(self, pos_x: int, pos_y: int):
        '''omits a single tile'''
        self[pos_x][pos_y].omit()
    
    def omit_tiles(self, sequence: list[tuple[int, int]], offset_x: int = 0, offset_y: int = 0):
        '''omits a sequence of connected tiles'''
        if len(sequence) == 1:
            self.omit_tile_at(sequence[0][0] + offset_x, sequence[0][1] + offset_y)
            return

        for i in range(len(sequence) - 1):
            from_x_idx = sequence[i][0] + offset_x
            from_y_idx = sequence[i][1] + offset_y
            to_x_idx = sequence[i + 1][0] + offset_x
            to_y_idx = sequence[i + 1][1] + offset_y
            if offset_x % 2 == 1:
                if sequence[i][0] % 2 == 0:
                    from_y_idx += 1
                if sequence[i + 1][0] % 2 == 0:
                    to_y_idx += 1

            from_tile = self[from_x_idx][from_y_idx]
            to_tile = self[to_x_idx][to_y_idx]

            from_tile.join(to_tile)

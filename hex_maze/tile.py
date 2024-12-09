from __future__ import annotations
from io import TextIOWrapper
import math
from typing import List, Tuple
import random
from datetime import datetime
from turtle import *
random.seed(datetime.timestamp(datetime.now()))


class Tile:
    '''
    The walls of a single tile is indexed as follows
            0
       5  /---\  1
         /     \
         \     /
       4  \---/  2
            3
    '''
    _x: int
    _y: int
    board: Board
    size: float
    margin: float
    _omitted: bool = False
    _walls: list
    _cache: dict

    def __init__(self, x, y, board: Board):
        self._x = x
        self._y = y
        self.configure(size=10, margin=0)
        self.board = board
        self._walls = [True, True, True, True, True, True]

    def configure(self, size: float = 10, margin: float = 0):
        self._cache = {}
        self.size = size
        self.margin = margin

    def reset(self):
        self.configure()
        self._walls = [True, True, True, True, True, True]

    @property
    def x(self):
        return self._x

    @property
    def y(self):
        return self._y

    @property
    def is_lifted(self):
        return (self._x % 2) != 0

    @property
    def is_baseline(self):
        return (self._x % 2) == 0

    @property
    def neighbours(self):
        if 'neighbours' not in self._cache:
            self._cache['neighbours'] = (
                self.board.top(self),
                self.board.top_right(self),
                self.board.bottom_right(self),
                self.board.bottom(self),
                self.board.bottom_left(self),
                self.board.top_left(self),
            )
        return [*self._cache['neighbours']]

    def negibour_at(self, wall_idx: int) -> Tile:
        return self.neighbours[wall_idx]

    def omit(self):
        self._omitted = True

    @property
    def is_taken(self):
        return self._omitted or sum(self._walls) != 6

    @property
    def untaken_neighbours(self):
        opts = filter(lambda tile: tile is not None, self.neighbours)
        return list(filter(lambda tile: not tile.is_taken, opts))

    def join(self, other: Tile):
        idx = self.index_of(other)
        self._walls[idx] = False
        other._walls[(idx + 3) % 6] = False

    def knock_down_wall(self, wall_idx: int) -> Tile:
        to_join = self.negibour_at(wall_idx)
        self.join(to_join)
        return to_join

    def index_of(self, other: Tile) -> int:
        dx = self._x - other.x
        dy = self._y - other.y
        if abs(dx) > 1 or abs(dy) > 1 or (dy == 0 and dx == 0):
            print(f"Tile@[{other.x},{other.y}] is no neighbour of self@[{self._x},{self._y}]")
            # raise f"The provided tile@[{other.x},{other.y}] is no neighbour of self@[{self._x},{self._y}]"
        if dx == 0:
            if dy < 0:
                return 3
            else:
                return 0
        elif dx > 0:
            if dy == 0:
                if self.is_baseline:
                    return 5
                else:
                    return 4
            elif dy > 0:
                return 5
            else:
                return 4
        else:
            if dy == 0:
                if self.is_baseline:
                    return 1
                else:
                    return 2
            elif dy > 0:
                return 1
            else:
                return 2

    @property
    def brickable_walls(self) -> List[int]:
        brickable = [idx for (idx, keep) in zip(list(range(6)), self._walls) if keep]
        if self.x == 0:
            if 4 in brickable:
                brickable.remove(4)
            if 5 in brickable:
                brickable.remove(5)
        elif self.x == self.board.dim_x - 1:
            if 1 in brickable:
                brickable.remove(1)
            if 2 in brickable:
                brickable.remove(2)
        if self.y == 0:
            if 0 in brickable:
                brickable.remove(0)
            if self.is_lifted:
                if 1 in brickable:
                    brickable.remove(1)
                if 5 in brickable:
                    brickable.remove(5)
        elif self.y == self.board.dim_y - 1:
            if 3 in brickable:
                brickable.remove(3)
            if self.is_baseline:
                if 2 in brickable:
                    brickable.remove(2)
                if 4 in brickable:
                    brickable.remove(4)
        return brickable

    @property
    def height(self):
        '''height of a tile'''
        if 'height' in self._cache:
            return self._cache['height']
        self._cache['height'] = self.size * math.sqrt(3)
        return self._cache['height']

    @property
    def width(self):
        '''width of a tile'''
        if 'width' in self._cache:
            return self._cache['width']
        self._cache['width'] = self.size * 2
        return self._cache['width']

    @property
    def center(self) -> Tuple[float, float]:
        if 'center' not in self._cache:
            x = (self._x // 2) * self.size * 3
            y = -self._y * self.height
            if self._x % 2 == 1:
                y += self.height / 2
                x += 3 / 4 * self.width
            self._cache['center'] = (x, y)
        return [*self._cache['center']]

    @property
    def hexpoints(self):
        if 'hexpoints' not in self._cache:
            angle = math.radians(360 / 6)
            center = self.center
            hex_points = [((math.cos(i * angle) * (self.size - self.margin)) + center[0],
                           (math.sin(i * angle) * (self.size - self.margin)) + center[1]) for i in range(2, -4, -1)]
            self._cache['hexpoints'] = tuple(hex_points)
        return [*self._cache['hexpoints']]

    def write_wall_to_svg(self, file: TextIOWrapper, wall_idx: int) -> bool:
        points = self.hexpoints
        target = points[(wall_idx + 1) % 6]
        offset_y = 5 * self.height / 4
        offset_x = 3 * self.width / 4
        if self._walls[wall_idx]:
            file.write(f'{offset_x + target[0]},{offset_y - target[1]} ')
            return True
        else:
            if self.margin > 0:
                to = self.negibour_at(wall_idx)
                if to:
                    conn_p = to.hexpoints[(wall_idx + 4) % 6]
                    file.write(f'{offset_x + conn_p[0]},{offset_y - conn_p[1]} ')
            return False

    def turtle_draw_wall(self, wall_idx: int) -> bool:
        '''draws a single wall and returns true when the wall is solid (thus drawn), otherwise false
        '''
        points = self.hexpoints
        penup()
        goto(*points[wall_idx])
        if self._walls[wall_idx]:
            pendown()
            goto(*points[(wall_idx + 1) % 6])
            return True
        else:
            if self.margin > 0:
                to = self.negibour_at(wall_idx)
                if to:
                    conn_p = to.hexpoints
                    pendown()
                    goto(*conn_p[(wall_idx + 4) % 6])
            else:
                goto(*points[(wall_idx + 1) % 6])
            return False

    def turtle_draw(self):
        points = self.hexpoints
        start = points.pop(0)
        points.append(start)
        penup()
        goto(*start)
        for (inner, draw, idx) in zip(points, self._walls, range(6)):
            if draw:
                pendown()
            else:
                if idx < 3 and self.margin > 0:
                    to = self.negibour_at(idx)
                    if to:
                        conn_p = to.hexpoints
                        pendown()
                        goto(*conn_p[(idx + 4) % 6])
                        penup()
                        goto(*points[(idx) % 6])
                        pendown()
                        goto(*conn_p[(idx + 3) % 6])
                        penup()
                penup()

            goto(*inner)

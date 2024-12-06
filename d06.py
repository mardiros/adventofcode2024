from enum import Enum
import pathlib
from dataclasses import field, dataclass

codes = pathlib.Path("d06.txt").read_text()

# codes = """\
# ....#.....
# .........#
# ..........
# ..#.......
# .......#..
# ..........
# .#..^.....
# ........#.
# #.........
# ......#...
# """


class PointType(Enum):
    empty = "."
    obstruction = "#"


class Direction(Enum):
    UP = "^"
    DOWN = "v"
    LEFT = "<"
    RIGHT = ">"


@dataclass
class Point:
    typ: PointType
    visited: bool = field(default=False)

    def visit(self):
        self.visited = True

    def obstr(self) -> bool:
        return self.typ == PointType.obstruction


MapType = list[Point]


class World:
    def __init__(
        self, map: MapType, position: int, direction: Direction, row_width: int
    ):
        self.map = map
        self.position = position
        self.row_width = row_width
        self.direction = direction
        self.map[position].visit()

    def count_visited(self):
        return sum([p.visited for p in self.map])

    def hit_top(self, x: int):
        return x < self.row_width

    def hit_left(self, x: int):
        return x % self.row_width == 0

    def hit_right(self, x: int):
        return x % self.row_width == (self.row_width - 1)

    def hit_bottom(self, x: int):
        return x > len(self.map) - self.row_width

    def is_done(self) -> bool:
        if self.hit_top(self.position):
            return True
        if self.hit_bottom(self.position):
            return True
        if self.hit_left(self.position):
            return True
        if self.hit_right(self.position):
            return True
        return False

    def move(self):
        print(self.direction)
        match self.direction:
            case Direction.UP:
                self.position -= self.row_width
                if (
                    not self.is_done()
                    and self.map[self.position - self.row_width].obstr()
                ):
                    self.direction = Direction.RIGHT

            case Direction.DOWN:
                self.position += self.row_width
                if (
                    not self.is_done()
                    and self.map[self.position + self.row_width].obstr()
                ):
                    self.direction = Direction.LEFT
            case Direction.LEFT:
                self.position -= 1
                if not self.is_done() and self.map[self.position - 1].obstr():
                    self.direction = Direction.UP

            case Direction.RIGHT:
                self.position += 1
                if not self.is_done() and self.map[self.position + 1].obstr():
                    self.direction = Direction.DOWN

        self.map[self.position].visit()

    def __str__(self) -> str:
        r = ""
        for i, p in enumerate(self.map):
            if p.visited:
                r += "X"
                continue
            if i == self.position:
                r += self.direction.value
                continue
            r += p.typ.value
            if self.hit_right(i):
                r += "\n"
        return r


def parse_input(codes: str) -> World:
    map = []
    row_width = 0
    start_pos = 0
    pos = 0
    start_direction = Direction.UP
    for line in codes.strip().splitlines():
        row_width = len(line)
        if start_pos == 0:
            for direction in Direction:
                if direction.value in line:
                    start_pos = pos + line.index(direction.value)
                    start_direction = direction
                    line = line.replace(direction.value, ".")
                    break

        line = [Point(PointType(x)) for x in line]
        map.extend(line)
        pos += row_width

    return World(map, start_pos, start_direction, row_width)


world = parse_input(codes)
while not world.is_done():
    world.move()

print(world)
print(world.count_visited())

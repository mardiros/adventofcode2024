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
    visited_pos: dict[Direction, bool] = field(
        default_factory=lambda: {
            Direction.UP: False,
            Direction.DOWN: False,
            Direction.RIGHT: False,
            Direction.LEFT: False,
        }
    )
    conflict: bool = field(default=False)

    def visit(self, direction: Direction):
        self.visited = True
        self.visited_pos[direction] = True

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
        self.map[position].visit(direction)

    def count_conflict(self):
        return sum([p.conflict for p in self.map])

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

    def detect_conflict(self):
        pos = self.position
        match self.direction:
            case Direction.UP:
                cpos = self.position - self.row_width
                while True:
                    if self.map[pos].visited_pos[Direction.RIGHT]:
                        self.map[cpos].conflict = True
                        break
                    if self.map[pos].obstr():
                        break
                    if self.hit_right(pos):
                        break
                    pos += 1

            case Direction.DOWN:
                cpos = self.position + self.row_width
                while True:
                    if self.map[pos].visited_pos[Direction.LEFT]:
                        self.map[cpos].conflict = True
                        break
                    if self.map[pos].obstr():
                        break
                    if self.hit_left(pos):
                        break
                    pos -= 1

            case Direction.LEFT:
                cpos = self.position - 1
                while True:
                    if self.map[pos].visited_pos[Direction.UP]:
                        self.map[cpos].conflict = True
                        break
                    if self.map[pos].obstr():
                        break
                    if self.hit_top(pos):
                        break
                    pos -= self.row_width

            case Direction.RIGHT:
                cpos = self.position + 1
                while True:
                    if self.map[pos].visited_pos[Direction.DOWN]:
                        self.map[cpos].conflict = True
                        break
                    if self.map[pos].obstr():
                        break
                    if self.hit_bottom(pos):
                        break
                    pos += self.row_width

    def move(self):
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

        self.map[self.position].visit(self.direction)

    def __str__(self) -> str:
        r = ""
        for i, p in enumerate(self.map):
            if p.conflict >= 1:
                r += "O"
                continue
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
    world.detect_conflict()
    # print(world)
    # breakpoint()

print(world.count_conflict())
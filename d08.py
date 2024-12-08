from itertools import product
from collections import defaultdict
from dataclasses import dataclass, field
from typing import Self

import pathlib

codes = pathlib.Path("d08.txt").read_text()


codes = """
............
........0...
.....0......
.......0....
....0.......
......A.....
............
............
........A...
.........A..
............
............
"""


@dataclass
class Antenna:
    x: int
    y: int
    typ: str

    def __hash__(self):
        return self.x * self.y

    def __eq__(self, other):
        return self.x == other.x and self.y == other.y and self.typ == other.typ


@dataclass
class Point:
    antenna: Antenna | None
    antinode: bool = field(default=False)

    def mark(self):
        self.antinode = True

    def __str__(self) -> str:
        if self.antenna:
            return self.antenna.typ
        if self.antinode:
            return "#"
        return "."


@dataclass
class Map:
    width: int
    height: int
    antennas: dict[str, list[Antenna]]
    points: list[list[Point]]

    @classmethod
    def from_str(cls, codes: str) -> Self:
        points = []
        antennas = defaultdict(list)
        height = 0
        width = 0
        for y, line in enumerate(codes.strip().splitlines()):
            row = []
            for x, c in enumerate(line):
                antenna = None
                if c != ".":
                    antenna = Antenna(x=x, y=y, typ=c)
                    antennas[c].append(antenna)
                row.append(Point(antenna))

            points.append(row)
            width = len(line)
            height = y
        return cls(width, height, dict(antennas), points)

    def detect_anti(self) -> None:
        visits = set()
        for typ, antennas in self.antennas.items():
            for a1, a2 in product(antennas, repeat=2):
                if a1 == a2:
                    continue
                if (a2, a1) in visits:
                    continue

                visits.add((a1, a2))

                anti1x = 2 * a1.x - a2.x
                anti1y = 2 * a1.y - a2.y
                if 0 <= anti1x < self.width and 0 <= anti1y <= self.height:
                    self.points[anti1y][anti1x].mark()

                anti2x = 2 * a2.x - a1.x
                anti2y = 2 * a2.y - a1.y
                if 0 <= anti2x < self.width and 0 <= anti2y <= self.height:
                    self.points[anti2y][anti2x].mark()

    def __str__(self) -> str:
        r = ""
        for row in self.points:
            for p in row:
                r += str(p)
            r += "\n"

        return r

    def count_antinode(self):
        p = [point.antinode for row in self.points for point in row]
        return sum(p)


map = Map.from_str(codes)
map.detect_anti()
# print(map)
print(map.count_antinode())

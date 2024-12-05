from collections import defaultdict
from collections.abc import Iterator
import pathlib
from dataclasses import dataclass, field
from math import floor

codes = pathlib.Path("d05.txt").read_text()

# codes = """
# 47|53
# 97|13
# 97|61
# 97|47
# 75|29
# 61|13
# 75|53
# 29|13
# 97|29
# 53|29
# 61|53
# 97|53
# 61|29
# 47|13
# 75|47
# 97|75
# 47|61
# 75|61
# 47|29
# 75|13
# 53|13

# 75,47,61,53,29
# 97,61,53,29,13
# 75,29,13
# 75,97,47,61,53
# 61,13,29
# 97,13,75,29,47
# """

ordrul, expects = codes.split("\n\n")


@dataclass
class Page:
    number: int
    parents: set["Page"] = field(default_factory=set)

    def __hash__(self) -> int:
        return self.number

    def __repr__(self):
        return repr({p.number for p in self.parents})

    def append(self, child: "Page"):
        child.parents.add(self)


def build_pages():
    pages = {}

    for line in ordrul.strip().splitlines():
        a, b = map(int, line.split("|"))
        if b not in pages:
            pages[b] = Page(number=b)

        if a not in pages:
            pages[a] = Page(number=a)

        pages[a].append(pages[b])

    return pages


pages = build_pages()


def build_expected() -> Iterator[list[int]]:
    for line in expects.strip().splitlines():
        yield list(map(int, line.split(",")))


def is_valid_order(pages: dict[int, Page], expected_order: list[int]):
    page_positions = {page: i for i, page in enumerate(expected_order)}

    for page in pages.values():
        if page.number not in page_positions:
            continue
        for parent in page.parents:
            if parent.number in page_positions:
                if page_positions[page.number] < page_positions[parent.number]:
                    return False
    return True


def repair(pages: dict[int, Page], to_repair: list[int]) -> list[int]:
    """
    Topological sort using Kahn's algorithm

    wiki: https://en.wikipedia.org/wiki/Topological_sorting#Kahn's_algorithm
    """
    adj = defaultdict(set)
    in_degree: dict[int, int] = {page: 0 for page in to_repair}

    for before in pages.values():
        if before.number in to_repair:
            for after in pages[before.number].parents:
                if after.number in to_repair:
                    adj[before.number].add(after.number)
                    in_degree[after.number] += 1

    queue = [page for page in to_repair if in_degree[page] == 0]
    result = []

    while queue:
        page = queue.pop(0)
        result.append(page)

        for neighbor in adj[page]:
            in_degree[neighbor] -= 1

            if in_degree[neighbor] == 0:
                queue.append(neighbor)

    return result


valid_expects = []
for exp in build_expected():
    if not is_valid_order(pages, exp):
        valid_expects.append(repair(pages, exp))

middles = [int(v[floor(len(v) / 2)]) for v in valid_expects]

print(sum(middles))
# print(sum(middles) == 123)

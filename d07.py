from dataclasses import dataclass
# import pathlib
# codes = pathlib.Path("d07.txt").read_text()

codes = """
190: 10 19
3267: 81 40 27
83: 17 5
156: 15 6
7290: 6 8 6 15
161011: 16 10 13
192: 17 8 14
21037: 9 7 18 13
292: 11 6 16 20
"""


def sum_or_mul(operands):
    my_operands = operands.copy()
    op0 = my_operands.pop()

    if len(my_operands) > 1:
        for res in sum_or_mul(my_operands):
            yield op0 + res
            yield op0 * res
    else:
        yield op0 + my_operands[0]
        yield op0 * my_operands[0]


@dataclass
class Item:
    result: int
    operands: list[int]


def parse_input(codes: str):
    for line in codes.strip().splitlines():
        result, operands = line.split(":")
        yield Item(
            int(result),
            list(map(int, operands.strip().split())),
        )


def part1():
    summ = set()
    for items in parse_input(codes):
        for x in sum_or_mul(items.operands):
            if x == items.result:
                summ.add(x)
    return sum(summ)


print(part1())

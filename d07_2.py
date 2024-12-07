from dataclasses import dataclass
from itertools import product
import pathlib
codes = pathlib.Path("d07.txt").read_text()

# codes = """
# 190: 10 19
# 3267: 81 40 27
# 83: 17 5
# 156: 15 6
# 7290: 6 8 6 15
# 161011: 16 10 13
# 192: 17 8 14
# 21037: 9 7 18 13
# 292: 11 6 16 20
# """


def sum_or_mul(operands, expected):
    for operators in product("+*|", repeat=len(operands) - 1):
        ops = list(operators)
        operands_ = operands.copy()
        res = operands_.pop(0)
        while ops:
            op = ops.pop(0)
            match op:
                case "+":
                    res += operands_.pop(0)
                case "*":
                    res *= operands_.pop(0)
                case "|":
                    res = int(str(res) + str(operands_.pop(0)))
            if res > expected:
                break
        yield res


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


def part2():
    summ = set()
    for items in parse_input(codes):
        for x in sum_or_mul(items.operands, items.result):
            if x == items.result:
                summ.add(x)
    return sum(summ)


print(part2())

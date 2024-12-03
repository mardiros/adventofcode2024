import pathlib
from functools import reduce
from operator import add, mul

codes = pathlib.Path("d03.txt").read_text()
# codes = "xmul(2,4)&mul[3,7]!^don't()_mul(5,5)+mul(32,64](mul(11,8)undo()?mul(8,5))"

results = []
enabled = True
for lpart in codes.split(")"):
    ops = lpart.rsplit("(", maxsplit=1)
    if len(ops) != 2:
        continue
    x, y = ops

    if x.endswith("don't"):
        enabled = False
    if x.endswith("do"):
        enabled = True

    if not enabled:
        continue

    if x.endswith("mul"):
        snumbers = y.split(",")
        try:
            numbers = list(map(int, snumbers))
        except ValueError:
            pass
        else:
            if len(numbers) == 2 and 0 < numbers[0] <= 999 and 0 < numbers[1] <= 999:
                results.append(reduce(mul, numbers))

res = reduce(add, results)
print(res)

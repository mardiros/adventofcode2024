import pathlib

codes = pathlib.Path("d2.txt").read_text()


def safe_count(line):
    val = line.pop(0)
    positive = val > line[0]

    for i in line:
        if positive:
            t = val - i
        else:
            t = i - val
        if t > 3 or t <= 0:
            return 0
        val = i
    return 1


count_safe = 0
for line in codes.strip().splitlines():
    line = [int(x) for x in line.split()]
    count_safe += safe_count(line)

print(count_safe)

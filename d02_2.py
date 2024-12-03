import pathlib

codes = pathlib.Path("d02.txt").read_text()


def clone_list(line: list[int]):
    for i in range(len(line)):
        yield line[:i] + line[i + 1 :]


def safe_count(line, recursive=True):
    lcp = line.copy()
    val = line.pop(0)
    positive = val > line[0]

    for i in line:
        if positive:
            t = val - i
        else:
            t = i - val
        if t > 3 or t <= 0:
            if recursive:
                for lc in clone_list(lcp):
                    if safe_count(lc, recursive=False):
                        return 1
            return 0
        val = i
    return 1


count_safe = 0
for line in codes.strip().splitlines():
    line = [int(x) for x in line.split()]
    count_safe += safe_count(line)

print(count_safe)

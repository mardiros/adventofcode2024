import pathlib
codes = pathlib.Path("d04.txt").read_text()

# codes = """
# MMMSXXMASM
# MSAMXMSMSA
# AMXSXMAAMM
# MSAMASMSMX
# XMASAMXAMM
# XXAMMXXAMA
# SMSMSASXSS
# SAXAMASAAA
# MAMMMXMMMM
# MXMXAXMASX
# """

xmas = "XMAS"
samx = xmas[::-1]


def verticals(rows):
    v = [""] * len(rows)
    for line in rows:
        for i, c in enumerate(line):
            v[i] += c
    return v


def diag(rows):
    n = len(rows)
    m = len(rows[0])
    diagonals = []
    for d in range(-n + 1, m):
        diagonal = []
        for i in range(n):
            j = d + i
            if 0 <= j < m:
                diagonal.append(rows[i][j])
        diagonals.append("".join(diagonal))

    return diagonals


def anti_diag(rows):
    n = len(rows)
    m = len(rows[0])

    anti_diagonals = []

    for d in range(m + n - 1):
        anti_diagonal = []
        for i in range(n):
            j = d - i
            if 0 <= j < m:
                anti_diagonal.append(rows[i][j])
        anti_diagonals.append("".join(anti_diagonal))

    return anti_diagonals


def countx(*args):
    cnt = 0
    for l in args:
        for i in l:
            cnt += i.count(xmas)
            cnt += i.count(samx)
    return cnt


codes = codes.strip()

rows = codes.splitlines()
cols = verticals(rows)
diag1 = diag(rows)
diag2 = anti_diag(rows)
print(countx(rows, cols, diag1, diag2))

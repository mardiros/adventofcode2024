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


def diag(rows):
    cnt = 0
    n = len(rows)
    m = len(rows[0])
    for i in range(1, m - 1):
        for j in range(1, n - 1):
            if rows[i][j] == "A":
                if (
                    rows[i - 1][j - 1] == "M"
                    and rows[i + 1][j + 1] == "S"
                    and rows[i - 1][j + 1] == "M"
                    and rows[i + 1][j - 1] == "S"
                ):
                    cnt += 1
                elif (
                    rows[i - 1][j - 1] == "S"
                    and rows[i + 1][j + 1] == "M"
                    and rows[i - 1][j + 1] == "S"
                    and rows[i + 1][j - 1] == "M"
                ):
                    cnt += 1
                elif (
                    rows[i - 1][j - 1] == "S"
                    and rows[i + 1][j + 1] == "M"
                    and rows[i - 1][j + 1] == "M"
                    and rows[i + 1][j - 1] == "S"
                ):
                    cnt += 1
                elif (
                    rows[i - 1][j - 1] == "M"
                    and rows[i + 1][j + 1] == "S"
                    and rows[i - 1][j + 1] == "S"
                    and rows[i + 1][j - 1] == "M"
                ):
                    cnt += 1

    return cnt


codes = codes.strip()
rows = codes.splitlines()
print(diag(rows))

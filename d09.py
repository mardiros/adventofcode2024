from pathlib import Path
from typing import Iterator


codes = Path(__file__.replace(".py", ".puzzle")).read_text().strip()


def flatten(codes: str) -> Iterator[int]:
    chars = list(map(int, codes))

    block = 0
    last_pos = len(chars) - 1

    for idx, val in enumerate(chars):
        if idx % 2 == 0:
            for _ in range(val):
                block += 1
                yield idx // 2
        elif last_pos > idx:
            for _ in range(val):
                while last_pos > idx and chars[last_pos] == 0:
                    last_pos -= 2
                if last_pos <= idx:
                    break
                yield (last_pos // 2)
                block += 1
                chars[last_pos] -= 1


def checksum(codes: str):
    r = 0
    for idx, val in enumerate(flatten(codes)):
        r += idx * val
    return r


print(checksum(codes))

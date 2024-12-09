from pathlib import Path
from typing import Iterator


codes = Path(__file__.replace(".py", ".puzzle")).read_text().strip()

# codes = "2333133121414131402"


# def unflatten(codes: str) -> Iterator[str]:
#     cnt = 0
#     freespace = False
#     for c in codes:
#         if freespace:
#             yield "." * int(c)
#         else:
#             yield str(cnt) * int(c)
#             cnt += 1
#         freespace = not freespace


# print("".join(unflatten(codes)))
# assert "".join(unflatten(codes)) == "00...111...2...333.44.5555.6666.777.888899"


def flatten(codes):
    chars = list(codes)
    cnt = 0
    freespace = False
    freespacecnt = 0
    queue = []
    last_free_space = len(codes) % 2 == 0
    lastnum = len(codes) // 2
    while chars:
        char = chars.pop(0)
        if freespace:
            fragsize = int(char)
            while len(queue) < fragsize:
                if not chars:
                    break
                last_char = int(chars.pop())
                if last_free_space:
                    freespacecnt += last_char
                else:
                    queue.extend(
                        (str(lastnum) * last_char)[::-1],
                    )
                    lastnum -= 1

                last_free_space = not last_free_space

            for i in range(fragsize):
                freespacecnt += 1
                yield queue.pop(0)

        else:
            yield str(cnt) * int(char)
            cnt += 1

        freespace = not freespace

    while queue:
        breakpoint()
        yield queue.pop()
    for i in range(freespacecnt):
        yield "."


# print("0099811188827773336446555566..............")
# print("".join(list(flatten(codes))))
# assert "".join(flatten(codes)) == "0099811188827773336446555566.............."


def checksum(codes):
    r = 0
    idx = 0
    for string in flatten(codes):
        if string == ".":
            break
        for c in string:
            r += idx * int(c)
            idx += 1
    return r

print(checksum(codes))
# print(checksum(codes) == 1928)

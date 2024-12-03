import pathlib

codes = pathlib.Path("d01.txt").read_text()

list1, list2 = [], []
for line in codes.strip().splitlines():
    a, b = line.split()
    list1.append(int(a))
    list2.append(int(b))

list1.sort()
list2.sort()

dist = 0
while list1:
    a, b = list1.pop(), list2.pop()
    dist += abs(a - b)

print(dist)

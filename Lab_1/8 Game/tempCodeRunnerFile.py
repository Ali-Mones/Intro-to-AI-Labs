
l: list[(str, int)] = []
l.append((3,2))
l.append((13,212))
l.append((44,2223))
l.append((3,3122))
l.append((5,31232))
l.append((11,2414))
l.append((32,232))
print(l)
cur, depth = l.pop()
print(cur, depth)
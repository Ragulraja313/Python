a = [2, 4, 10, 20, 5, 2, 20, 4]

lt = []

for i in a:
    if i not in lt:
        lt.append(i)
print(lt)
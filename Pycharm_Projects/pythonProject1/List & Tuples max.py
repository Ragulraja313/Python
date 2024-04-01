a = int(input("Enter the Number: "))

lt = []

for i in range(a):
    x = int(input())
    lt.append(x)

print(lt)

tt = tuple(lt)
print(tt)

max = 0

for z in lt:
    if max < z:
        max = z
print(max)

for i in tt:
    if max < i:
        max = i
print(max)







a = int(input())
for i in range(a):
    a, b = map(int, input().split())
    result = a + b

    if result <= 6:
        print("NO")
    else:
        print("YES")
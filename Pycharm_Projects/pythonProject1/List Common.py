def common(a, b):
    c = []

    for i in a:
        if i in b:
            c.append(i)

    print(c)


a = [1, 2, 3]
b = [2, 3, 4]

common(a,b)

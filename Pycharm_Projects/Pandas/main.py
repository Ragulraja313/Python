print((dir(locals()['__builtins__'])))


def fun():
    a = int(input())
    b = int(input())
    c = a + b
    print(c)


a = fun()
print(a)
if a != 5:
    print("Ture")

else:
    print("False")

c = 5 + 7

b = [1,2,3,4]
for b in range(0,3):
    print(b)

try:
    print(x)
    print(5 / 0)
except NameError as e:
    print(e)

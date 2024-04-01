a = int(input("Enter the Number: "))

num = lambda a: a % 2 == 0

if num(a):
    print("Even")
else:
    print("odd")


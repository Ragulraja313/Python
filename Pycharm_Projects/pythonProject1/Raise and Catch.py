x = -1

if x < 0:
    raise Exception("Value cannot be Negative")

print(x)

# Catching an Exception

try:
    a = 5
    b = 0
    print(a/b)

except ZeroDivisionError:
    print("Cannot Divide by Zero")

# Handling Multiple Exceptions

try:
    a = int(input("Enter the Number1: "))
    b = int(input("Enter the Number1: "))
    result = a/b

except NameError:
    print("Name is Not defined")
except ValueError:
    print("Integer is only supported")
except ZeroDivisionError:
    print("Value cannot be Zero")
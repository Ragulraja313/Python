# function Arguments

# Positional Arguments

def name(name, age):
    print("My name is " + name + " and the age is " + age)


name("Rahul", "15")
name("15", "Rahul")


# Default Arguments:

def fun(name, age="23"):
    print("My name is " + name + " and the age is " + age)


fun("Rahul")


# Keyword Arguments:
def mul(val1, val2):
    return val1 * val2


print(mul(val1=5, val2=5))


# Arbitrary Arguments
# *args
def mul(*val1, val2=5):
    print(val1[2] * val2)


mul(2, 3, 4, 5)


# kwargs
def mul(**val):
    print(val["one"] * val["three"])


mul(one=5, two=3, three=8)


# return Values

# single Return

def add(x, y):
    return x + y


add(5, 6)


# Multiple Return

def func(x, y):
    sub = x - y
    mul = x * y
    return sub, mul
print(func(5,5))

# Variable Scope

# Local Scope

def fun():
    x = 200
    print(x)

fun()

# Function inside Function

def fun():
    x = 100 #Enclosing Scope
    def fun1():
        print(x)
    fun1()

fun()

# Global Scope

x = 300
def name():
    print(x)

name()

# Global Keyword

def my():
    global x
    x = 300
    print(x)

my()
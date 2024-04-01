try:
    if '1' != 1:
        raise"SomeError"
    else:
        print("Error Occured")
except "SomeError":
    print("SomeError")

def getmonth(m):
    if m < 1 or m > 12:
        raise ValueError("Invalid")
    print(m)
getmonth(6)


valid = False
while not valid:
    try:
        n = int(input("Enter the number: "))
        while n%2 == 0:
            print("Bye")
        valid = True
    except ValueError:
        print("Invalid")

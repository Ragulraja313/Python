def calculate(n1,n2,op):
    result = 0
    if op == '+':
        result = n1+n2
    elif op == '-':
        result = n1-n2
    elif op == '*':
        result = n1*n2
    elif op == '/':
        result = n1/n2
    elif op == '^':
        result = n1**n2

    print(result)


calculate(55.25,33.42,"*")

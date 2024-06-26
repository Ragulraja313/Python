# Dictionary comprehension

keys = ['a', 'b', 'c', 'd', 'e']
values = [1, 2, 3, 4, 5]

myDict = {k: v for (k, v) in zip(keys, values)}

print(myDict)

# Sorting the Dictionary

myDict = {'ravi': 10, 'rajnish': 9, 'sanjeev': 15, 'yash': 2, 'suraj': 32}
print(sorted(myDict.items()))
print(sorted(myDict.keys()))
print(sorted(myDict.values()))
print(sorted(myDict.items(), reverse=True))

# Updating the Dictionary

myDict = {'ravi': 10, 'rajnish': 9, 'sanjeev': 15, 'yash': 2, 'suraj': 32}
myDict.update({'rahul': 22 ,'raja' : 25})
a = {'murali' : 33}
b = {'ajeeth' : 3}
myDict.update(**a, **b)
print(myDict)

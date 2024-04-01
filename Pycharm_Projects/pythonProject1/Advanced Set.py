# Set union
x = {"a", "b", "c"}
y = {"f", "d", "a"}
z = {"c", "d", "e"}

print(x.union(y,z))

# Set Intersection

x = {"a", "b", "c"}
y = {"f", "d", "a"}

c = x.intersection(y)
print(c)

# Set Difference

x = {"a", "b", "c"}
y = {"f", "d", "a"}

d = x.difference(y)
print(d)

# Symmetric Difference

y = {"f", "d", "a"}
z = {"c", "d", "e"}

e = y.symmetric_difference(z)
print(e)

# Set Comprehension

st = {x for x in range(10) if x % 2 == 0}
print(st)
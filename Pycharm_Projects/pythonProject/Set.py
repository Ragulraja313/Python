a = {"apple", "ball", "Cat"}

# Adding and Removing

a.add("Dog")
print(a)
a.remove("Dog")
print(a)

# Set methods

b = {"Dog", "Eli", "Forest", "Goat"}
e = a.union(b)
print(e)

c = ["apple", "Hat", "Cat"]
f = a.intersection(c)
print(f)

g = a.difference(c)
print(g)
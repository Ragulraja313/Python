a = {"name" : "Rahul", "Emp Id" : 11547, "Age" : 22}

# Accessing the Dictionary

b = a["Emp Id"]
print(b)

# Dictionary Methods

c = a.copy()
print(c)

x = ("key1", "key2", "key3")
y = 0
z = dict.fromkeys(x,y)
print(z)

print(a.get('name'))

print(a.items())

print(a.keys())

print(a.pop("Emp Id"))

print(a.popitem())

a.update({"Age": 60})
print(a)

print(a.setdefault("Age"))

print(a.values())
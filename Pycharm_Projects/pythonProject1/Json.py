# Parsing Json

import json

x = '{ "name":"John", "age":30, "city":"New York"}'

y = json.loads(x)

print(y["age"])

# Convert Python to Json

import json

x = {
    "name": "John",
    "age": 30,
    "city": "New York"
}

y = json.dumps(x)

print(y)

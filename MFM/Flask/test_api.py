import requests

url = "http://127.0.0.1:5000/employees/1"
data = {"name": "Ragul", "role": "Developer", "salary": 50000}

res = requests.put(url, json=data)
print(res.json())



# POST → Add new employee
# GET → View employees in Chrome
# PUT → Update employee
# DELETE → Remove employee
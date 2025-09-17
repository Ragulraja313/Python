from flask import Flask, request, jsonify
from flask_mysqldb import MySQL

app = Flask(__name__)

# Database Configuration
app.config["MYSQL_HOST"] = "localhost"
app.config["MYSQL_USER"] = "root"
app.config["MYSQL_PASSWORD"] = "Ragulraja@2002"
app.config["MYSQL_DB"] = "employee_db"

mysql = MySQL(app)


# 1. Add a new employee
@app.route('/employees', methods=['POST'])
def add_employee():
    data = request.get_json()
    name = data.get("name")
    role = data.get("role")
    salary = data.get("salary")

    cur = mysql.connection.cursor()
    query = "INSERT INTO employees (name, role, salary) VALUES (%s, %s, %s)"
    cur.execute(query, (name, role, salary))
    mysql.connection.commit()
    new_id = cur.lastrowid
    cur.close()

    return jsonify({"id": new_id, "name": name, "role": role, "salary": salary}), 201


# 2. Get all employees
@app.route('/employees', methods=['GET'])
def get_employees():
    cur = mysql.connection.cursor()
    cur.execute("SELECT id, name, role, salary FROM employees")
    rows = cur.fetchall()
    cur.close()

    employees = [{"id": r[0], "name": r[1], "role": r[2], "salary": r[3]} for r in rows]
    return jsonify(employees)


# 3. Get an employee by ID
@app.route('/employees/<int:emp_id>', methods=['GET'])
def get_employee(emp_id):
    cur = mysql.connection.cursor()
    cur.execute("SELECT id, name, role, salary FROM employees WHERE id=%s", (emp_id,))
    row = cur.fetchone()
    cur.close()

    if row:
        return jsonify({"id": row[0], "name": row[1], "role": row[2], "salary": row[3]})
    return jsonify({"error": "Employee not found"}), 404


# 4. Update employee details
@app.route('/employees/<int:emp_id>', methods=['PUT'])
def update_employee(emp_id):
    data = request.get_json()
    name = data.get("name")
    role = data.get("role")
    salary = data.get("salary")

    cur = mysql.connection.cursor()
    cur.execute("SELECT id FROM employees WHERE id=%s", (emp_id,))
    if not cur.fetchone():
        cur.close()
        return jsonify({"error": "Employee not found"}), 404

    query = "UPDATE employees SET name=%s, role=%s, salary=%s WHERE id=%s"
    cur.execute(query, (name, role, salary, emp_id))
    mysql.connection.commit()
    cur.close()

    return jsonify({"id": emp_id, "name": name, "role": role, "salary": salary})


# 5. Delete an employee
@app.route('/employees/<int:emp_id>', methods=['DELETE'])
def delete_employee(emp_id):
    cur = mysql.connection.cursor()
    cur.execute("SELECT id FROM employees WHERE id=%s", (emp_id,))
    if not cur.fetchone():
        cur.close()
        return jsonify({"error": "Employee not found"}), 404

    cur.execute("DELETE FROM employees WHERE id=%s", (emp_id,))
    mysql.connection.commit()
    cur.close()

    return jsonify({"message": "Employee deleted successfully"})


if __name__ == '__main__':
    app.run(debug=True)




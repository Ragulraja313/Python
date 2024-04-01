from flask import Flask, render_template, request
from flask_mysqldb import MySQL

app = Flask(__name__)

app.config["MYSQL_HOST"] = "localhost"
app.config["MYSQL_USER"] = "root"
app.config["MYSQL_PASSWORD"] = "Ragulraja@2002"
app.config["MYSQL_DB"] = "my_database"

mysql = MySQL(app)


@app.route('/')
@app.route('/sample')
def sample():
    return render_template('sample.html')


@app.route('/register', methods=['POST', 'GET'])
def register():
    if request.method == 'POST':
        n = request.form.get('name')
        a = request.form.get('age')
        c = request.form.get('city')
        mydb = mysql.connection.cursor()
        query = "INSERT INTO data1 (name,age,city) VALUES (%s,%s,%s)"
        mydb.execute(query, (n, a, c))
        mysql.connection.commit()
        mydb.close()
        return render_template('register.html', name=n, age=a, city=c)


if __name__ == '__main__':
    app.run(debug=True)

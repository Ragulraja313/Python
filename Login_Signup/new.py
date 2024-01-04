import sqlite3
from flask import *

app = Flask(__name__)
app.secret_key = "123"


def db_connection():
    db = sqlite3.connect('Details.db')
    # db.execute("DROP TABLE IF EXISTS data;")
    # db.execute("create table data (Name varchar not null, Age int not null, Email_ID varchar not null, "
    #            "Domain varchar not null, Password varchar not null);")
    db.commit()
    return db


@app.route('/')
@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        name = request.form['name']
        password = request.form['pass1']
        con = db_connection()
        cur = con.cursor()
        cur.execute("select * from data where Name=? and Password=?", (name, password))
        data = cur.fetchone()

        if data:
            session["name"] = data[0]
            session["password"] = data[1]
            return redirect('display')
        else:
            flash("Username and Password Mismatch", "danger")
    return render_template('login.html')


@app.route('/signup', methods=['POST', 'GET'])
def signup():
    if request.method == 'POST':
        n = request.form.get('name')
        a = request.form.get('age')
        e = request.form.get('email')
        d = request.form.get('domain')
        p = request.form.get('pass')
        conn = db_connection()
        cur = conn.cursor()
        cur.execute("insert into data(Name,Age,Email_ID,Domain,Password) values(?,?,?,?,?)", (n, a, e, d, p))
        conn.commit()
        return redirect('/login')
    return render_template("signup.html")


@app.route('/display', methods=['POST', "GET"])
def display():
    conn = db_connection()
    cur = conn.cursor()
    post = cur.execute("select Name from data").fetchall()
    conn.commit()
    return render_template('display.html', post=post)


if __name__ == '__main__':
    app.run(debug=True)

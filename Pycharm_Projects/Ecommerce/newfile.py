from flask import Flask, render_template, request, redirect
from flask_mysqldb import MySQL

app = Flask(__name__)

app.config["MYSQL_HOST"] = "localhost"
app.config["MYSQL_USER"] = "root"
app.config["MYSQL_PASSWORD"] = "Ragulraja@2002"
app.config["MYSQL_DB"] = "ecommerce"

mysql = MySQL(app)


@app.route('/')
def home():
    return render_template("index.html")


@app.route('/about', methods=['POST', 'GET'])
def about():
    if request.method == 'POST':
        return redirect('/about')
    return render_template('about.html')


# --- PRODUCTS ROUTE (Insert items into DB) ---
@app.route('/products', methods=['POST', 'GET'])
def products():
    if request.method == 'POST':
        image = request.form.get('image')
        name = request.form.get('apple')

        cur = mysql.connection.cursor()
        cur.execute(
            "INSERT INTO cart_items (image, name, description, price) VALUES (%s, %s, %s, %s)",
            (image, name, "Product Description", 29.0)
        )
        mysql.connection.commit()
        cur.close()

        return redirect('/products')

    return render_template('products.html')


@app.route('/contact', methods=['POST', 'GET'])
def contact():
    if request.method == 'POST':
        name = request.form.get('name')
        mobile = request.form.get('mobile')
        mail = request.form.get('mail')
        query = request.form.get('query')
        db = mysql.connection.cursor()
        db.execute("INSERT INTO Details (name,mobile,mail,query) VALUES (%s,%s,%s,%s)",
                   (name, mobile, mail, query))
        mysql.connection.commit()
        db.close()
        return redirect('/contact')
    return render_template('contact.html')


# --- CART ROUTE (Fetch items from DB) ---
@app.route('/cart', methods=['POST', 'GET'])
def cart():
    cur = mysql.connection.cursor()
    cur.execute("SELECT * FROM cart_items")
    items = cur.fetchall()
    cur.close()

    # Pass DB items to template
    return render_template('cart.html', items=items)


# --- REMOVE ITEM ROUTE (Delete from DB) ---
@app.route('/remove_item', methods=['POST'])
def remove_item():
    item_id = request.form.get('item_id')
    if item_id:
        cur = mysql.connection.cursor()
        cur.execute("DELETE FROM cart_items WHERE id = %s", (item_id,))
        mysql.connection.commit()
        cur.close()
    return redirect('/cart')


if __name__ == "__main__":
    app.run(debug=True)
from flask import Flask, render_template, request, redirect
from flask_mysqldb import MySQL

app = Flask(__name__)

app.config["MYSQL_HOST"] = "localhost"
app.config["MYSQL_USER"] = "root"
app.config["MYSQL_PASSWORD"] = "Ragulraja@2002"
app.config["MYSQL_DB"] = "ecommerce"

mysql = MySQL(app)

cart_items = []


@app.route('/')
def home():
    return render_template("index.html")


@app.route('/about', methods=['POST', 'GET'])
def about():
    if request.method == 'POST':
        redirect('/about')
    return render_template('about.html')


@app.route('/products', methods=['POST', 'GET'])
def products():
    if request.method == 'POST':
        image = request.form.get('image')
        name = request.form.get('apple')
        product = {
            'image': image,
            'name': name,
            'description': 'Product Description',
            'price': 29.0,
        }
        cart_items.append(product)
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
        db.execute("insert into Details(name,mobile,mail,query) values(%s,%s,%s,%s)", (name, mobile, mail, query))
        db.connection.commit()
        redirect('/contact')
    return render_template('contact.html')


@app.route('/cart', methods=['POST', 'GET'])
def cart():
    if request.method == 'POST':
        return redirect('/cart')
    return render_template('cart.html', items=cart_items)


@app.route('/remove_item', methods=['POST'])
def remove_item():
    if request.method == 'POST':
        item_name = request.form.get('item_name')
        for i, item in enumerate(cart_items):
            if item['name'] == item_name:
                cart_items.pop(i)
                break
        return redirect('/cart')

    return redirect('/cart')


if __name__ == "__main__":
    app.run(debug=True)

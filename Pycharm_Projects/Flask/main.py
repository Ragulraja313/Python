from flask import Flask, render_template, request, make_response

app = Flask(__name__)
app.secret_key = 'your_secret_key'


@app.route('/')
def index():
    user = request.cookies.get('user', 'Guest')
    return render_template('index.html', user=user)


@app.route('/set_cookie', methods=['POST'])
def set_cookie():
    user = 'John Doe'
    response = make_response(render_template('index.html', user=user))
    response.set_cookie('user', user)
    return response


if __name__ == '__main__':
    app.run(debug=True)

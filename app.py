from flask import Flask, render_template_string, request

app = Flask(__name__)

@app.route('/')
def index():
    return render_template_string(open('templates/index.html').read())

@app.route('/submit', methods=['POST'])
def submit():
    name = request.form['name']
    age = request.form['age']
    return render_template_string(f'<h1>Hello {name}, you are {age} years old!</h1>')

if __name__ == '__main__':app.run()
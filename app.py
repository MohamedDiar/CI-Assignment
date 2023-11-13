from flask import Flask, render_template, request, redirect, url_for
from flask_sqlalchemy import SQLAlchemy
import urllib
import os

app = Flask(__name__)

# Environment variables (replace these with your GitHub secrets in a real deployment)
username = os.environ.get('AZURE_SQL_USERNAME')
password = os.environ.get('AZURE_SQL_PASSWORD')
server = os.environ.get('AZURE_SQL_SERVER')
database = os.environ.get('AZURE_SQL_DATABASE')

params = urllib.parse.quote_plus(f'DRIVER={{ODBC Driver 18 for SQL Server}};'
                                 f'SERVER={server};'
                                 f'DATABASE={database};'
                                 f'UID={username};'
                                 f'PWD={password}')

app.config['SQLALCHEMY_DATABASE_URI'] = f"mssql+pyodbc:///?odbc_connect={params}"
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)

class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(50), nullable=False)
    age = db.Column(db.Integer, nullable=False)


db.create_all()

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/submit', methods=['POST'])
def submit():
    name = request.form['name']
    age = request.form['age']
    new_user = User(name=name, age=age)
    db.session.add(new_user)
    db.session.commit()
    return redirect(url_for('view_data'))

@app.route('/data')
def view_data():
    users = User.query.all()
    return render_template('data.html', users=users)

if __name__ == '__main__':app.run()

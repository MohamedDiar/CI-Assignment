from flask import Flask, render_template_string, request
import os
import pyodbc

app = Flask(__name__)

# Database connection
def get_db_connection():
    username = os.environ.get('AZURE_SQL_USERNAME')
    password = os.environ.get('AZURE_SQL_PASSWORD')
    server = os.environ.get('AZURE_SQL_SERVER')
    database = os.environ.get('AZURE_SQL_DATABASE')
    
    connection_string = f'DRIVER={{ODBC Driver 18 for SQL Server}};SERVER={server};DATABASE={database};UID={username};PWD={password}'
    return pyodbc.connect(connection_string)

@app.route('/')
def index():
    # You might want to use a separate HTML file for this form
    return render_template_string(open('templates/index.html').read())

@app.route('/submit', methods=['POST'])
def submit():
    name = request.form['name']
    age = request.form['age']
    
    # Insert into database
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute("INSERT INTO user (name, age) VALUES (?, ?)", (name, age))
    conn.commit()
    cursor.close()
    conn.close()

    return render_template_string(f'<h1>Hello {name}, you are {age} years old!</h1>')

@app.route('/users')
def users():
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM user")
    users = cursor.fetchall()
    cursor.close()
    conn.close()

    # Use render_template instead of render_template_string for external files
    return render_template_string(open('templates/data.html').read(), users=users)

if __name__ == '__main__':
    app.run()

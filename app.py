from flask import Flask, render_template_string, request, render_template, escape
from flask_wtf.csrf import CSRFProtect
from flask_talisman import Talisman
import os
import pymssql

app = Flask(__name__)
app.config['SECRET_KEY'] = os.environ.get('FLASK_SECRET_KEY', 'default_key')

# CSRF Protection
csrf = CSRFProtect(app) 

# Content Security Policy and Clickjacking Protection
Talisman(app, content_security_policy=None, frame_options='SAMEORIGIN')

# Database connection
def get_db_connection():
    username = os.environ.get('AZURE_SQL_USERNAME')
    password = os.environ.get('AZURE_SQL_PASSWORD')
    server = os.environ.get('AZURE_SQL_SERVER')
    database = os.environ.get('AZURE_SQL_DATABASE')
    
    return pymssql.connect(server, username, password, database)    

@app.route('/')
def index():
    return render_template_string(open('templates/index.html').read())

@app.route('/submit', methods=['POST'])
def submit():
    name = escape(request.form['name'])  # Apply escape here
    age = escape(request.form['age'])    # Apply escape here
    print(f"Received name: {name}, age: {age}")
    
    # Insert into database
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute("INSERT INTO user_info (name, age) VALUES (%s, %s)", (name, age))    
    conn.commit()
    cursor.close()
    conn.close()

    return render_template_string(f'''
            <h1>Hello {name}, you are {age} years old!</h1>
            <button onclick="window.location.href='/users'">Show All Users</button>
        ''')

@app.route('/users')
def users():
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM user_info")
    users = cursor.fetchall()
    cursor.close()
    conn.close()

    # Note: Ensure that user data is also escaped properly when rendered in 'data.html'
    return render_template('data.html', users=users)

if __name__ == '__main__':
    app.run()

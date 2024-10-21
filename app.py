from flask import Flask, render_template, request, redirect, url_for, session
from flask_mysqldb import MySQL
import pymysql

app = Flask(__name__)
app.secret_key = "!@#$%"

db = pymysql.connect(
    host='localhost',
    user='root',
    password='',
    database='flaskmysql',
    cursorclass=pymysql.cursors.DictCursor,
    ssl={'ssl': {'ca': None}}
)

@app.route('/', methods=['GET', 'POST'])
def login():
    if request.method == 'POST' and 'inpEmail' in request.form and 'inPass' in request.form:
        email = request.form['inpEmail']
        password = request.form['inPass']
        with db.cursor() as cur:
            cur.execute("SELECT * FROM users WHERE email = %s AND password = %s", (email, password))
            result = cur.fetchone()
        if result:
            session['is_logged_in'] = True
            session['username'] = result['username'] 
            return redirect(url_for('home'))
        else:
            return render_template('login.html', error='Invalid email or password')
    else:
        return render_template('login.html')

@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        email = request.form['email']
        
        with db.cursor() as cur:
            # Check if email already exists
            cur.execute("SELECT * FROM users WHERE email = %s", (email,))
            account = cur.fetchone()
            if account:
                return render_template('register.html', error='Email already exists')
            else:
                # Insert new user
                cur.execute("INSERT INTO users (username, password, email) VALUES (%s, %s, %s)", (username, password, email))
                db.commit()
                return redirect(url_for('login'))
    return render_template('register.html')

@app.route('/home')
def home():
    if 'is_logged_in' in session:
        with db.cursor() as cur:
            cur.execute("SELECT * FROM users")
            data = cur.fetchall()
        return render_template('home.html', users=data)
    else:
        return redirect(url_for('login'))

@app.route('/logout')
def logout():
    session.pop('is_logged_in', None)
    session.pop('username', None)
    return redirect(url_for('login'))

if __name__ == '__main__':
    app.run(debug=True)
from flask import Flask, render_template, redirect, request, session
from flask_mysqldb import MySQL
import bcrypt, os

app = Flask(__name__)

app.config['MYSQL_HOST'] = os.getenv('MYSQL_HOST')
app.config['MYSQL_USER'] = os.getenv('MYSQL_USER')
app.config['MYSQL_PASSWORD'] = os.getenv('MYSQL_PASSWORD')
app.config['MYSQL_DB'] = os.getenv('MYSQL_DB')
#app.config['SECRET_KEY'] = os.getenv('SECRET_KEY')

mysql = MySQL(app)

@app.route('/')
def index():
    return redirect('/login')

@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        name = request.form['name']
        email = request.form['email']
        password = request.form['password']
        hashed_password = bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt()).decode('utf-8')

        cur = mysql.connection.cursor()
        cur.execute("INSERT INTO users (name, email, password) VALUES (%s, %s, %s)", (name, email, hashed_password))
        mysql.connection.commit()
        cur.close()

        return redirect('/login')
    return render_template('register.html')


@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        email = request.form['email']
        password = request.form['password']

        cur = mysql.connection.cursor()
        cur.execute("SELECT * FROM users WHERE email = %s", (email,))
        user = cur.fetchone()
        cur.close()

        if user and bcrypt.checkpw(password.encode('utf-8'), user[3].encode('utf-8')):
            session['name'] = user[1]
            session['email'] = user[2]

            return redirect('/dashboard')
        else:
            return render_template('login.html', error='Invalid user')
    return render_template('login.html')


@app.route('/dashboard')
def dashboard():
    if 'name' in session:
        cur = mysql.connection.cursor()
        cur.execute("SELECT * FROM users WHERE email = %s", (session['email'],))
        user = cur.fetchone()
        cur.close()
        
        return render_template('dashboard.html', user=user)
    return redirect('/login')


@app.route('/logout')
def logout():
    session.pop('email', None)
    session.pop('name', None)
    return redirect('/login')


if __name__ == "__main__":
    app.run(host='0.0.0.0',port='5000',debug=True)


import os

# mysql
import mysql.connector
from dotenv import load_dotenv
# flask framework
from flask import Flask, flash, redirect, render_template, request, url_for, jsonify, session, make_response
from flask_bcrypt import Bcrypt
from flask_session import Session

import jwt;

load_dotenv();
db_config= {
    "host": "localhost",
    "user": "root",
    "password": os.getenv("password"),
    "database": os.getenv("database"),
}

app = Flask(__name__);
bcrypt = Bcrypt(app)
app.config['SESSION_TYPE'] = 'filesystem'
app.config['SECRET_KEY']=os.getenv('secretKey')
Session(app)
# routes
@app.route("/profile")
def home():
    token = request.args.get('token')
    user_data = None
    if token:
        try:
            data = jwt.decode(token, app.config['SECRET_KEY'], algorithms=['HS256'])
            username = data['username']
            user_data = {'username': 'TestUser'}
            # return f'Welcome, {username}!'
        except jwt.ExpiredSignatureError:
            return 'Token has expired', 401
        except jwt.InvalidTokenError:
            return 'Invalid token', 401
    
    return render_template('profile.html', user_data=user_data)

@app.route("/register", methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        username = request.form['username']
        email = request.form['email']
        password = request.form['password']
        confirmPassword = request.form['confirmPassword']

        if password != confirmPassword:
            return 'password doesnt match. try again'
        else:
            hash_password = bcrypt.generate_password_hash(password).decode('utf-8')


            connection = mysql.connector.connect(**db_config)
            cursor = connection.cursor()

            create_new_user = """
            INSERT INTO users(username, email, password)
            VALUES(
                %s, %s, %s
            )
            """

            cursor.execute(create_new_user, (username, email, hash_password))
            connection.commit()

            cursor.close()
            connection.close()

            token = jwt.encode({'username': username}, app.config['SECRET_KEY'], algorithm='HS256')
            # session['token'] = token
            # return redirect(url_for('home') + f'?token={token}')
            # return jsonify({'token': token})
            response = make_response(redirect(url_for("home")))
            response.set_cookie("token", token, httponly=True, secure=True)  # 'secure=True' is recommended for HTTPS

            return response

    return render_template('register.html')

@app.route("/login")
def login():
    return render_template('login.html')

@app.route('/logout')
def logout():
    return "<p>logout</p>"

if __name__ == '__main__':
    app.run(
        debug=True
        )
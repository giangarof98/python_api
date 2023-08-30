from flask import Flask, redirect, url_for, render_template, request;
from db import db_config;
import mysql.connector;
from config import app;

# show all route
@app.route('/home')
def home():
    connection = mysql.connector.connect(**db_config)
    cursor = connection.cursor()

    # # select all
    selectAll = """
        SELECT * FROM users;
    """

    cursor.execute(selectAll)
    data=cursor.fetchall()
    cursor.close()
    connection.close()
    print(data)
    return render_template('index.html', data=data)

# show user details
@app.route('/user/<int:user_id>')
def user(user_id):
    connection = mysql.connector.connect(**db_config)
    cursor = connection.cursor()

    get_user="""
        SELECT id, name, email, age FROM users WHERE id = %s;
    """
    cursor.execute(get_user, (user_id,))
    user_data = cursor.fetchone()
    cursor.close()
    connection.close()

    if user_data:
        user = {
            "id":user_data[0],
            "name":user_data[1],
            "email":user_data[2],
            "age":user_data[3]
        }
        return render_template('details.html', data=user)


# create route
@app.route('/create', methods=['GET', 'POST'])
def create():
    if request.method == 'POST':
        name = request.form['name']
        email = request.form['email']
        age = request.form['age']
        connection = mysql.connector.connect(**db_config)
        cursor = connection.cursor()
        create_user="""
        INSERT INTO users(name, email, age)
        VALUES(
            %s, %s, %s
        )
        """
        cursor.execute(create_user, (name, email, age))
        connection.commit()
        # data=cursor.fetchall()
        cursor.close()
        connection.close()
        return redirect(url_for('home'))
        
    return render_template('create.html')

# delete route
@app.route('/delete/<int:user_id>', methods=['POST'])
def delete(user_id):
    
    connection = mysql.connector.connect(**db_config)
    cursor = connection.cursor()

    delete="""
        DELETE FROM users WHERE id = %s;
    """

    cursor.execute(delete, (user_id,))

    connection.commit()
    cursor.close()
    connection.close()
    return redirect(url_for('home'))
    

# update route
@app.route('/user/<int:user_id>/update', methods=['GET', 'POST'])
def update(user_id):
    connection = mysql.connector.connect(**db_config)
    cursor = connection.cursor()
    if request.method == 'POST':
        name = request.form['name']
        email = request.form['email']
        age = request.form['age']
        
        update="""
            UPDATE users SET name = %s, email = %s, age = %s WHERE id = %s;
        """
        cursor.execute(update, (name, email, age, user_id))
        connection.commit()

        cursor.close()
        connection.close()

        return redirect(url_for('home'))
    
    select = "SELECT id, name, email, age FROM users WHERE id = %s"
    cursor.execute(select, (user_id,))
    user_data = cursor.fetchone()

    if user_data:
        user = {
            "id": user_data[0],
            "name": user_data[1],
            "email": user_data[2],
            "age": user_data[3]
        }
        return render_template('update.html', data=user)

    cursor.close()
    connection.close()
    return render_template('details.html', data=user)

if __name__ == '__main__':
    app.run(
        port=3000,
        debug=True, 
        use_reloader=True
        )
    

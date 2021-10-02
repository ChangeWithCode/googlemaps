from MySQLdb import Connect, connect
from flask import Flask, config, render_template, request, redirect, url_for, session, flash 
from flask.helpers import flash
from flask_mysqldb import MySQL
import MySQLdb.cursors
import re
from flask_mail import Mail, Message 




app = Flask(__name__)
app.secret_key = "Secret Key"

# Mysql db config

app.config['MYSQL_HOST'] = 'localhost'
app.config['MYSQL_USER'] = 'root'
app.config['MYSQL_PASSWORD'] = ''
app.config['MYSQL_DB'] = 'qasim'

# Intialize MySQL
mysql = MySQL(app)


# Email configuration 

app.config['MAIL_SERVER'] = 'smtp.gmail.com'
app.config['MAIL_PORT'] = 465
app.config['MAIL_USE_SSL'] = True
app.config['MAIL_USERNAME'] = "qasimriaz814@gmail.com"
app.config['MAIL_PASSWORD'] = "03215142274Qasim"
mail = Mail(app)



@app.route('/')
def home():
    return render_template('index.html')

@app.route('/pricing')
def price():
    return render_template ('pricing.html')

# @app.route('/contact', methods=['GET', 'POST'])
# def contact():

#     if request.method == "POST":

#         Name  = request.form['name']
#         Email = request.form['email']
#         Phone = request.form['phone']
#         Message = request.form['message']
#         cur = mysql.connection.cursor()
#         cur.execute("INSERT INTO contact(name,email,phone,message ) VALUES (%s, %s , %s , %s)", (Name, Email ,Phone,Message))
#         mysql.connection.commit()
#         cur.close()
#         return 'success'
#     return render_template('contact.html')

@app.route('/adminlogin' , methods=['POST', 'GET'])
def login():
    # Output message if something goes wrong...
    msg = ''
    # Check if "username" and "password" POST requests exist (user submitted form)
    if request.method == 'POST' and 'username' in request.form and 'password' in request.form:
        # Create variables for easy access
        username = request.form['username']
        password = request.form['password']
        # Check if account exists using MySQL
        cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
        cursor.execute('SELECT * FROM admin WHERE username = %s AND password = %s', (username, password,))
        # Fetch one record and return result
        admin = cursor.fetchone()
        # If account exists in accounts table in out database
        if admin:
            session['loggedin'] = True
            session['id'] = admin['id']
            session['username'] = admin['username']
            return redirect(url_for('adminhome'))
            
        else:
            # Account doesnt exist or username/password incorrect
            flash ("Incorrect username/password!" , "info")
            return redirect(url_for('login'))
        
    # Show the login form with message (if any)
    return render_template('adminlogin.html')


#- this will be the home page, only accessible for admin
@app.route('/admin')
def adminhome():
    # Check if user is loggedin
    if 'loggedin' in session:
        # User is loggedin show them the home page
        return render_template('admindashboard.html', username=session['username'])
    # User is not loggedin redirect to login page
    return redirect(url_for('login'))

#- this will be the logout page for admin
@app.route('/admin/logout')
def logout():
    # Remove session data, this will log the user out
   session.pop('loggedin', None)
   session.pop('id', None)
   session.pop('username', None)
   # Redirect to login page
   return redirect(url_for('login'))


#- this will be the pricing plan page for admin
@app.route('/admin/plans',methods=["POST","GET"])
def plans():
    cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
    cursor.execute('SELECT * FROM plans')
    Data=cursor.fetchall()
    return render_template ('plans.html',plans=Data)


#this route is for inserting plan from admin dashboard to mysql database via html forms
@app.route('/admin/plans/insert', methods = ['POST'])
def insert():

    if request.method == 'POST':

        name = request.form['name']
        price = request.form['price']


        cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
        cursor.execute("INSERT INTO plans set name=%s,price=%s",(name,price))
        mysql.connection.commit()

        flash("Plan Inserted Successfully")

        return redirect(url_for('plans'))

#this route is for editing plan from admin dashboard to mysql database via html forms
@app.route('/admin/plans/edit/<id>', methods = ['GET', 'POST'])
def edit(id):

    if request.method == 'POST':

        name = request.form['name']
        price = request.form['price']

        cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
        cursor.execute("UPDATE plans set  name= %s,price=%s WHERE id = %s" ,(name,price,id))
        mysql.connection.commit()
        flash("Plan updated Successfully")

        return redirect(url_for('plans'))



#- this will be for deleting pricing plan page for admin
@app.route('/admin/plans/delete/<id>/', methods = ['GET', 'POST'])
def delete(id):

    cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
    cursor.execute('DELETE FROM plans WHERE id = %s' ,(id))
    mysql.connection.commit()

    flash("Plan Deleted Successfully")
    # return "Employee Deleted Successfully"

    return redirect(url_for('plans'))
 

# @app.route('/adminlogin/password',methods = ['GET', 'POST'])
# def passwordreset():

#     if request.method=='POST':
#         password = request.form['password']
#         cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
#         cursor.execute("UPDATE admin set  password = %s",[password])
#         mysql.connection.commit()
#         flash ("Password Updated Succesfuly" , "info")
    
#     return render_template('passwords.html')



if __name__ == "__main__":
    app.run(debug=True)
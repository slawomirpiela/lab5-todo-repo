from flask import Flask
from flask import render_template
from flask_mysqldb import MySQL
mysql = MySQL()
app = Flask(__name__)
# My SQL Instance configurations 
# Change the HOST IP and Password to match your instance configurations
 
app.config['MYSQL_USER'] = 'root'
app.config['MYSQL_PASSWORD'] = 'piela'
app.config['MYSQL_DB'] = 'contacts'
app.config['MYSQL_HOST'] = '35.195.246.187'
mysql.init_app(app)

@app.route('/')
@app.route('/<name>')
def statichtml(name=None):
    return render_template('index.html', name=name)

# The first route to access the webservice from http://35.190.217.3:5000/ 
#@pp.route("/add") this will create a new endpoints that can be accessed using http://external-ip:5000/add
@app.route("/list")
def hello(): # Name of the method
    cur = mysql.connection.cursor() #create a connection to the SQL instance
    cur.execute('''SELECT * FROM contacts''') # execute an SQL statment
    rv = cur.fetchall() #Retreive all rows returend by the SQL statment
    return render_template('index.html', name=str(rv))     #Return the data in a string format

@app.route("/add/<name>/<surname>")
def add(name=None, surname=None):
    cur= mysql.connection.cursor()
    insert_stmt = (
                 "INSERT INTO contacts (name, surname) "
                 "VALUES (%s, %s)")
    data=(name,surname)
    cur.execute(insert_stmt, data)
    mysql.connection.commit()
    return render_template('index.html', name="New Record is added to the database")  

@app.route("/update/<name>/<surname>")
def update(name=None, surname=None):
    cur=mysql.connection.cursor()
    update_stmt = (
        "UPDATE students SET name = %s " 
        "WHERE surname = %s")
    data=(name,surname)
    cur.execute(update_stmt, data)
    mysql.connection.commit()
    return render_template('index.html', name="User recored was updated")      #Return the data in a string format

@app.route("/delete/<name>")
def delete(name=None):
    cur=mysql.connection.cursor()
    delstatmt = "DELETE FROM students WHERE name = ' {} ' ".format(name)
    print(delstatmt)                
   
    cur.execute(delstatmt)
    mysql.connection.commit()
    return render_template('index.html', name="User recored was deleted")      #Return the data in a string format

if __name__ == "__main__":
        app.run(host='0.0.0.0', port='5000') 


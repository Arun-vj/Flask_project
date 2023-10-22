from flask import Flask,render_template,redirect,request,url_for
from flask_mysqldb import MySQL

app = Flask(__name__)

app.config['MYSQL_HOST'] = 'localhost'
app.config['MYSQL_USER'] = 'root'
app.config['MYSQL_PASSWORD'] = 'Admin'
app.config['MYSQL_DB'] = 'mydb'
app.config['MYSQL_CURSORCLASS'] = 'DictCursor'

mysql = MySQL(app)

#mysql connection
@app.route("/")
def home():
    con = mysql.connection.cursor()
    qry = "select * from employee"
    con.execute(qry)
    res = con.fetchall()
    return render_template("index.html",carry=res)

#add user
@app.route("/addemp/",methods=["GET","POST"])
def addemp():
    if request.method == "POST":
        name = request.form['ename']
        job = request.form['job']
        salary = request.form['sal']
        con = mysql.connection.cursor()
        qry = "insert into employee(name,job_role,salary) values(%s,%s,%s)"
        con.execute(qry,[name,job,salary])
        mysql.connection.commit()
        con.close()  
        return redirect(url_for('home'))
    return render_template("addemp.html")

#edituser
@app.route("/editemp<string:id>",methods=["GET","POST"])
def editemp(id):
    con = mysql.connection.cursor()
    if request.method == "POST":
        name = request.form['ename']
        job = request.form['job']
        salary = request.form['sal']
        con = mysql.connection.cursor()
        qry = "update employee set name=%s,job_role=%s,salary =%s where id=%s"
        con.execute(qry,[name,job,salary,id])
        mysql.connection.commit()
        con.close()  
        return redirect(url_for('home'))
    qry = "select * from employee where id=%s"
    con.execute(qry,[id])
    res = con.fetchone()
    return render_template("editemp.html",carry=res)

#delete user

@app.route("/deleteemp<string:id>",methods=["GET","POST"])
def deleteemp(id):
    con = mysql.connection.cursor()
    qry = "delete from employee where id=%s"
    con.execute(qry,[id])
    mysql.connection.commit()
    con.close()
    return redirect(url_for('home'))

if __name__ == "__main__":
    app.run(debug=True)
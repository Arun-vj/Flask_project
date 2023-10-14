from flask import Flask,render_template,redirect,url_for,request
from flask_mysqldb import MySQL


app = Flask(__name__)

app.config['MYSQL_HOST'] = 'localhost'
app.config['MYSQL_USER'] = 'arunvj'
app.config['MYSQL_PASSWORD'] = '@run'
app.config['MYSQL_DB'] = 'MyDB'
app.config['MYSQL_CURSORCLASS'] = 'DictCursor'

mysql = MySQL(app)

#mysql connection
@app.route("/")
def home():
    con = mysql.connection.cursor()
    qry = "select * from employee"
    con.execute(qry)
    res = con.fetchall()
    return render_template("home.html",datas=res)

#add user
@app.route("/adduser/",methods=["GET","POST"])
def adduser():
    if request.method == "POST":
        name = request.form['name']
        job = request.form['job']
        salary = request.form['salary']
        con = mysql.connection.cursor()
        qry = "insert into employee(name,job_role,salary) values(%s,%s,%s)"
        con.execute(qry,[name,job,salary])
        mysql.connection.commit()
        con.close()  
        return redirect(url_for('home'))
    return render_template("adduser.html")

#edituser
@app.route("/edituser<string:id>",methods=["GET","POST"])
def edituser(id):
    con = mysql.connection.cursor()
    if request.method == "POST":
        name = request.form['name']
        job = request.form['job']
        salary = request.form['salary']
        con = mysql.connection.cursor()
        qry = "update employee set name=%s,job_role=%s,salary =%s where id=%s"
        con.execute(qry,[name,job,salary,id])
        mysql.connection.commit()
        con.close()  
        return redirect(url_for('home'))
    qry = "select * from employee where id=%s"
    con.execute(qry,[id])
    res = con.fetchone()
    return render_template("edituser.html",datas=res)

#delete user

@app.route("/deleteuser<string:id>",methods=["GET","POST"])
def deleteuser(id):
    con = mysql.connection.cursor()
    qry = "delete from employee where id=%s"
    con.execute(qry,id)
    mysql.connection.commit()
    con.close()
    return redirect(url_for('home'))

if __name__ == "__main__":
    app.run(debug=True)
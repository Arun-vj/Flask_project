from flask import Flask,render_template,request,redirect,url_for
from flask_mysqldb import MySQL

app = Flask(__name__)

#mysql connections
app.config["MYSQL_HOST"] = 'localhost'
app.config["MYSQL_USER"] = 'root'
app.config["MYSQL_PASSWORD"] = 'Admin'
app.config["MYSQL_DB"] = 'mydb'
app.config["MYSQL_CURSORCLASS"] = 'DictCursor'

mysql = MySQL(app)


#login page
@app.route("/")
def login():
    return render_template("login.html")

#database open
@app.route("/database")
def emp_db():
    con = mysql.connection.cursor()
    qry = "select * from employee"
    con.execute(qry)
    data = con.fetchall()
    return render_template("datas.html",output=data)


#addemp
@app.route("/addemp",methods=["GET","POST"])
def addemp():
    if request.method=="POST":
        u = request.form['uname']
        j = request.form['uJob_role']
        s = request.form['usalary']
        con = mysql.connection.cursor()
        qry = "insert into employee (name,job_role,salary) values(%s,%s,%s)"
        usr = [u,j,s]
        con.execute(qry,usr)
        mysql.connection.commit()
        con.close()
        return redirect(url_for('emp_db'))
    return render_template ("addemp.html")



#editemployee
@app.route("/editemp<string:id>",methods=["GET","POST"])
def editemp(id):
    if request.method=="POST":
        u = request.form['uname']
        j = request.form['uJob_role']
        s = request.form['usalary']
        con = mysql.connection.cursor()
        qry = "update employee set name=%s,job_role=%s,salary=%s where id=%s"
        usr = [u,j,s,id]
        con.execute(qry,usr)
        mysql.connection.commit()
        con.close()
        return redirect(url_for('emp_db'))
    con = mysql.connection.cursor()
    qry = "select * from employee where id=%s"
    con.execute(qry,[id])
    data = con.fetchone()
    return render_template("editemp.html",res=data)


@app.route("/delemp<string:id>",methods=["GET","POST"])
def delemp(id):
    con = mysql.connection.cursor()
    qry = "delete from employee where id=%s"
    con.execute(qry,[id])
    mysql.connection.commit()
    con.close()
    return redirect(url_for('emp_db'))

#validate
@app.route("/",methods=["GET","POST"])
def validate():
    con = mysql.connection.cursor()
    name = request.form['user']
    password = request.form['pass']
    qry = "select  * from user where username=%s and passwd=%s"
    user = [name,password]
    con.execute(qry,user)
    data = con.fetchone()
    if data is None:
        return "Invalid username and password"
    else:
        return redirect(url_for('emp_db'))

#signup page
@app.route("/signup")
def signup():
    return render_template("signup.html")


@app.route("/signup",methods=["Get","POST"])
def adduser():
    if request.method=="POST":
        u = request.form['suser']
        p = request.form['spass']
        con = mysql.connection.cursor()
        qry = "insert into user (username,passwd) values(%s,%s)"
        usr = [u,p]
        con.execute(qry,usr)
        mysql.connection.commit()
        con.close()
        return redirect(url_for('login'))
    return render_template('signup.html')



if __name__ == "__main__":
    app.run(debug=True)


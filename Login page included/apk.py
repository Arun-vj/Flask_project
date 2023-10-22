from flask import Flask,render_template,redirect,url_for,flash,request

from flask_mysqldb import MySQL

app = Flask(__name__)

#mysql connections
app.config['MYSQL_HOST']='localhost'
app.config['MYSQL_USER']='root'
app.config['MYSQL_PASSWORD']='Admin'
app.config['MYSQL_DB']='mydb'
app.config['MYSQL_CURSORCLASS']='DictCursor'

mysql=MySQL(app)
@app.route("/")
def sigup():
    return render_template("login.html")

#home page
@app.route("/home")
def home():
    con = mysql.connection.cursor()
    qry = "select * from employee"
    con.execute(qry)
    res = con.fetchall()
    return render_template("home.html",datas=res)

#edit user
@app.route("/edituser<string:id>",methods=["GET","POST"])
def edituser(id):
    con = mysql.connection.cursor()
    if request.method == "POST":
        uname = request.form['name']
        ujob_role = request.form['job']
        salary = request.form['sal']
        con = mysql.connection.cursor()
        qry = "update employee set name=%s,job_role=%s,salary=%s where id=%s"
        user = [uname,ujob_role,salary,id]
        con.execute(qry,user)
        mysql.connection.commit()
        con.close()
        return redirect(url_for('home'))
    qry="select * from employee where id=%s"
    con.execute(qry,[id])
    res = con.fetchone()
    return render_template("edituser.html",datas=res)

#delete user
@app.route("/deleteuser<string:id>",methods=['GET','POST'])
def deleteuser(id):
    con = mysql.connection.cursor()
    qry = "delete from employee where id=%s"
    con.execute(qry,[id])
    mysql.connection.commit()
    con.close()
    return redirect(url_for('home'))

#adduser
@app.route("/adduser",methods=["GET","POST"])
def adduser():
    if request.method == "POST":
        uname = request.form['name']
        ujob_role = request.form['job']
        salary = request.form['sal']
        con = mysql.connection.cursor()
        qry = "insert into employee (name,job_role,salary) values(%s,%s,%s)"
        user = [uname,ujob_role,salary]
        con.execute(qry,user)
        mysql.connection.commit()
        con.close()
        return redirect(url_for('home'))
    return render_template("adduser.html")


#validate user 
@app.route("/",methods=["GET","POST"])
def Authenticate():
    username = request.form['user']
    passwd = request.form['passwd']
    con = mysql.connection.cursor()
    qry = "select * from user where username=%s and passwd=%s"
    sql = [username,passwd]
    con.execute(qry,sql)
    data = con.fetchone()
    if data is None:
        return "Invalid username and password"
    else:
        return redirect("home")
    
#Run the app
if __name__ =="__main__":
    app.run(debug=True)


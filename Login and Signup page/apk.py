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
        return "hi welcome"

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
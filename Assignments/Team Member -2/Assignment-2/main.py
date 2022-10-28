from flask import Flask,render_template
import ibm_db
try:
    conn = ibm_db.connect("DATABASE=bludb;HOSTNAME=98538591-7217-4024-b027-8baa776ffad1.c3n41cmd0nqnrk39u98g.databases.appdomain.cloud;PORT=30875;SECURITY=SSL;SSLServerCertificate=DigiCertGlobalRootCA.crt;UID=bkp88188;PWD=6kMh6xYbM0hAwn8D",'','')
    print(conn)
except:
    print(ibm_db.conn_errormsg())

app = Flask(__name__)

@app.route("/")
def index():
    return render_template("index.html")
@app.route("/home")
def HomePage():
    return "<p>Home Page!</p>"
@app.route("/about")
def AboutPage():
    return "<p>About Page!</p>"
@app.route("/login")
def LoginPage():
    return render_template("login.html")
@app.route("/signup")
def SignupPage():
    return render_template("signup.html")
@app.route("/forgotpwd")
def ForgotPwdPage():
    return render_template("forgotpwd.html")
@app.route("/docs")
def DocumentationPage():
    return render_template("docs.html")
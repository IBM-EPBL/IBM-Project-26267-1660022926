from flask import Flask, render_template, request, session, redirect, url_for
import ibm_db

try:
    conn = ibm_db.connect(
        "DATABASE=bludb;HOSTNAME=98538591-7217-4024-b027-8baa776ffad1.c3n41cmd0nqnrk39u98g.databases.appdomain.cloud;PORT=30875;SECURITY=SSL;SSLServerCertificate=DigiCertGlobalRootCA.crt;UID=bkp88188;PWD=6kMh6xYbM0hAwn8D",
        '', '')
    print(conn)
except:
    print(ibm_db.conn_errormsg())

app = Flask(__name__)
app.secret_key = 'a'


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


@app.route("/forgotpassword", methods=['GET', 'POST'])
def forgotpassword():
    if request.method == 'POST':
        email = request.form['email']
        password = request.form['npassword']
        sql = "select * from users where email=?"
        stmt = ibm_db.prepare(conn, sql)
        ibm_db.bind_param(stmt, 1, email)
        ibm_db.execute(stmt)
        account = ibm_db.fetch_assoc(stmt)
        if account:
            sql1 = "update users set password=? where email=?"
            stmt = ibm_db.prepare(conn, sql1)
            ibm_db.bind_param(stmt, 1, password)
            ibm_db.bind_param(stmt, 2, email)

            ibm_db.execute(stmt)
            return render_template('forgotpwd.html', msg="Password Changed")
        else:
            return render_template('forgotpwd.html', msg="Incorrect Email")


@app.route("/docs")
def DocumentationPage():
    return render_template("docs.html")


@app.route('/addrec', methods=['POST', 'GET'])
def addrec():
    if request.method == 'POST':

        username = request.form['name']
        email = request.form['email']
        password = request.form['password']

        sql = "SELECT * FROM users WHERE username =?"
        stmt = ibm_db.prepare(conn, sql)
        ibm_db.bind_param(stmt, 1, username)
        ibm_db.execute(stmt)
        account = ibm_db.fetch_assoc(stmt)

        if account:
            return render_template('signup.html', msg="You are already a member, please login")
        else:
            insert_sql = "INSERT INTO users VALUES (?,?,?)"
            prep_stmt = ibm_db.prepare(conn, insert_sql)
            ibm_db.bind_param(prep_stmt, 1, username)
            ibm_db.bind_param(prep_stmt, 2, email)
            ibm_db.bind_param(prep_stmt, 3, password)
            ibm_db.execute(prep_stmt)

        return render_template('signup.html', msg="User Created Successfuly..")


@app.route('/authenticate', methods=['POST', 'GET'])
def authenticate():
    global userId
    if request.method == 'POST':

        username = request.form['username']
        password = request.form['password']

        sql = "SELECT * FROM users WHERE username =? AND password=?"
        stmt = ibm_db.prepare(conn, sql)
        ibm_db.bind_param(stmt, 1, username)
        ibm_db.bind_param(stmt, 2, password)
        ibm_db.execute(stmt)
        account = ibm_db.fetch_assoc(stmt)

        if account:
            session['loggedin'] = True
            session['id'] = account['USERNAME']
            userId = account['USERNAME']
            session['username'] = account['USERNAME']
            return render_template('docs.html', msg="Logged in Successfully!!")
        else:
            msg = "Incorrect username/password"
        return render_template('login.html', msg=msg)





@app.route('/logout')
def logout():
    session.pop('loggedin', None)
    session.pop('id', None)
    session.pop('username', None)
    return render_template('login.html')


@app.route('/dashboard')
def DashboardPage():
    return render_template('dashboard.html')


@app.errorhandler(404)
def page_not_found(e):
    return render_template('404.html')


@app.route('/bbregister')
def bbregister():
    return render_template('bbregister.html')


@app.route('/bblogin')
def bblogin():
    return render_template('bblogin.html')

@app.route('/doregister')
def doregister():
    return render_template('doregister.html')


@app.route('/dologin')
def dologin():
    return render_template('dologin.html')


@app.route('/bbaddrec', methods=['POST', 'GET'])
def bbaddrec():
    if request.method == 'POST':

        username = request.form['bbname']
        email = request.form['bbemail']
        password = request.form['password']
        city = request.form['city']
        state = request.form['state']
        pincode = request.form['pincode']
        contact = request.form['contact']

        sql = "SELECT * FROM bbusers WHERE bbname =?"
        stmt = ibm_db.prepare(conn, sql)
        ibm_db.bind_param(stmt, 1, username)
        ibm_db.execute(stmt)
        account = ibm_db.fetch_assoc(stmt)

        if account:
            return render_template('bbregister.html', msg="You are already a member, please login")
        else:
            insert_sql = "INSERT INTO bbusers VALUES (?,?,?,?,?,?,?)"
            prep_stmt = ibm_db.prepare(conn, insert_sql)
            ibm_db.bind_param(prep_stmt, 1, username)
            ibm_db.bind_param(prep_stmt, 2, email)
            ibm_db.bind_param(prep_stmt, 3, password)
            ibm_db.bind_param(prep_stmt, 4, city)
            ibm_db.bind_param(prep_stmt, 5, state)
            ibm_db.bind_param(prep_stmt, 6, pincode)
            ibm_db.bind_param(prep_stmt, 7, contact)
            ibm_db.execute(prep_stmt)

        return render_template('bbregister.html', msg="User Created Successfuly..")

@app.route('/bbauthenticate', methods=['POST', 'GET'])
def bbauthenticate():
    global userId
    if request.method == 'POST':

        bbname = request.form['bbname']
        password = request.form['bbpassword']
        email = request.form['bbemail']

        sql = "SELECT * FROM bbusers WHERE bbname =? AND password=? AND email=?"
        stmt = ibm_db.prepare(conn, sql)
        ibm_db.bind_param(stmt, 1, bbname)
        ibm_db.bind_param(stmt, 2, password)
        ibm_db.bind_param(stmt, 3, email)
        ibm_db.execute(stmt)
        account = ibm_db.fetch_assoc(stmt)

        if account:
            session['loggedin'] = True
            session['id'] = account['BBNAME']
            userId = account['BBNAME']
            session['bbname'] = account['BBNAME']
            return render_template('donor_list.html', msg="Logged in Successfully!!")
        else:
            msg = "Incorrect username/password"
        return render_template('bblogin.html', msg=msg)

@app.route('/donorlist')
def donorlist():
    donors = []
    sql = "SELECT * FROM dousers"
    stmt = ibm_db.exec_immediate(conn, sql)
    dictionary = ibm_db.fetch_both(stmt)
    while dictionary != False:
        # print ("The Name is : ",  dictionary)
        donors.append(dictionary)
        dictionary = ibm_db.fetch_both(stmt)
    if donors:
        return render_template('donor_list.html',donors=donors)

# @app.route('/list')
# def list():
#   students = []
#   sql = "SELECT * FROM Students"
#   stmt = ibm_db.exec_immediate(conn, sql)
#   dictionary = ibm_db.fetch_both(stmt)
#   while dictionary != False:
#     # print ("The Name is : ",  dictionary)
#     students.append(dictionary)
#     dictionary = ibm_db.fetch_both(stmt)
#
#   if students:
#     return render_template("list.html", students = students)


@app.route('/dolog', methods=['POST', 'GET'])
def dolog():
    global userId
    if request.method == 'POST':
        password = request.form['password']
        email = request.form['email']

        sql = "SELECT * FROM dousers WHERE email =? AND password=?"
        stmt = ibm_db.prepare(conn, sql)
        ibm_db.bind_param(stmt, 1, email)
        ibm_db.bind_param(stmt, 2, password)

        ibm_db.execute(stmt)
        account = ibm_db.fetch_assoc(stmt)

        if account:
            session['loggedin'] = True
            session['id'] = account['EMAIL']
            userId = account['EMAIL']
            session['email'] = account['EMAIL']
            return render_template('donor_list.html', msg="Logged in Successfully!!")
        else:
            msg = "Incorrect username/password"
        return render_template('dologin.html', msg=msg)

@app.route('/doregi', methods=['POST', 'GET'])
def doregi():
    if request.method == 'POST':

        username = request.form['name']
        email = request.form['email']
        password = request.form['password']
        city = request.form['city']
        state = request.form['state']
        pincode = request.form['pincode']
        contact = request.form['contact']
        blood = request.form['bg']

        sql = "SELECT * FROM dousers WHERE username =?"
        stmt = ibm_db.prepare(conn, sql)
        ibm_db.bind_param(stmt, 1, username)
        ibm_db.execute(stmt)
        account = ibm_db.fetch_assoc(stmt)

        if account:
            return render_template('doregister.html', msg="You are already a member, please login")
        else:
            insert_sql = "INSERT INTO dousers VALUES (?,?,?,?,?,?,?,?)"
            prep_stmt = ibm_db.prepare(conn, insert_sql)
            ibm_db.bind_param(prep_stmt, 1, username)
            ibm_db.bind_param(prep_stmt, 2, email)
            ibm_db.bind_param(prep_stmt, 3, password)
            ibm_db.bind_param(prep_stmt, 4, city)
            ibm_db.bind_param(prep_stmt, 5, state)
            ibm_db.bind_param(prep_stmt, 6, pincode)
            ibm_db.bind_param(prep_stmt, 7, contact)
            ibm_db.bind_param(prep_stmt, 8, blood)
            ibm_db.execute(prep_stmt)

        return render_template('doregister.html', msg="User Created Successfuly..")
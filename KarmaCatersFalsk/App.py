from flask import Flask, render_template,redirect,session, make_response,request
from flaskext.mysql import MySQL
from flask_mail import Mail, Message
from werkzeug.utils import secure_filename

import os

app = Flask(__name__)        

app.secret_key = 'sample_project'

mysql = MySQL()
# DB config
app.config['MYSQL_DATABASE_USER'] = 'root'
app.config['MYSQL_DATABASE_PASSWORD'] = ''
app.config['MYSQL_DATABASE_HOST'] = 'localhost'
app.config['MYSQL_DATABASE_DB'] = 'karmaCaters'

# main config
app.config['MAIL_SERVER'] = 'smtp.gmail.com'
# app.config['MAIL_PORT'] = 465   #email-portnumber for ssl
app.config['MAIL_PORT'] = 587  #email-portnumber for tls
app.config['MAIL_USERNAME'] = 'karma.caters007@gmail.com'
app.config['MAIL_PASSWORD'] = 'karma@123'
app.config['MAIL_USE_TLS'] = True
app.config['MAIL_USE_SSL'] = False
mail = Mail(app)

mysql.init_app(app)

def getData(sql,vals=0):
    con = mysql.connect()
    cur = con.cursor()
    res = ''
    if(vals == 0):
        cur.execute(sql)
    else:
        cur.execute(sql,vals)
    res = cur.fetchall()
    cur.close()
    con.close()
    return res

def setData(sql,vals=0):
    con = mysql.connect()
    cur = con.cursor()
    if(vals == 0):
        cur.execute(sql)
    else:
        cur.execute(sql,vals)
    con.commit()
    res = cur.rowcount
    return res

@app.route("/")
def index():
    msg = ""
    sql = "select * from items"
    res = getData(sql)
    if res:return render_template("public/home.html", res = res)
    else:
        msg = "No data here..!"
        return render_template("public/home.html", msg = msg)


@app.route('/review', methods=["POST"])
def reView():
    if request.method == "POST":
        data = request.form
        sql = "select ifnull(max(id),0)+1 from feedback"
        id = getData(sql)
        id = id[0]
        sql = "insert into feedback values(%s, %s, %s, %s)"
        vals = (id, data['name'], data['email'], data['feeds'])
        res = setData(sql,vals)
        _to = [''+data['email']+'']
        mseg = Message("Karma Caters", sender = 'karma.caters007@gmail.com', recipients = _to)
        mseg.body = "Thankyou for your valuable response.. \n %s"%(data['name'].capitalize())
        mail.send(mseg)
        return redirect('/')
    else:
        msg = "Something went wrong..!"
        return render_template('public/home.html',msg=msg)

@app.route('/Gallery')
def gallery():
    sql = "select * from upload"
    res = getData(sql)
    msg = ""
    if len(res)>0:
        photo = []
        for r in res:
            ext = r[2].split(".")
            ext = ext[-1].upper()
            if ext == "JPG" or ext == "PNG" or ext == "GIF":
                photo.append(r)
        return render_template("public/Gallery.html", photo = photo)
    else:
        msg = "No photos here..!"
        return render_template('public/Gallery.html', msg1 = msg)

@app.route('/Gallery/photo/<int:id>')
def photo(id):
    sql = "select * from upload where uid = %s"%id
    res = getData(sql)
    return render_template('public/media.html', res = res)

@app.route('/close')
def close():
    return redirect('/Gallery')

@app.route("/Gallery/videos")
def video():
    sql = "select * from upload"
    res = getData(sql)
    msg = ""
    if len(res)>0:
        vedio = []
        for r in res:
            ext = r[2].split(".")
            ext = ext[-1].lower()
            if ext == "mp4" or ext == "mov" or ext == "3gp":
                vedio.append(r)
        return render_template("public/Gallery.html", video = vedio)
    else:
        msg = "No Vedio here..!"
        return render_template('public/Gallery.html', msg1 = msg)

@app.route('/Gallery/media/<int:id>')
def media(id):
    sql = "select * from upload where uid = %s"%id
    res = getData(sql)
    return render_template('public/media.html', v = res)

@app.route('/booking/<int:id>')
def booking(id):
    sql = "select * from items where id =%s"%id
    res = getData(sql)
    return render_template('public/booking.html',res1 = res)

@app.route('/BookingInfo/<int:id>', methods = ["POST"])
def bookDetails(id):
    msg = ""
    if request.method == "POST":
        data = request.form
        sql = "select ifnull(max(bid),0)+1 from booking"
        bid = getData(sql)[0][0]
        sql = "insert into booking values(%s, %s, %s, %s, %s, %s, %s, %s, %s, CURRENT_TIMESTAMP, 0 )"
        vals = (bid, id, data['name'], data['email'], data['contact'], data['place'], data['qunt'], data['date'], data['time'])
        setData(sql,vals)
        sql = "SELECT b.name,i.item,b.place,DATE_FORMAT(b.date,'%%d-%%M-%%Y'),TIME_FORMAT(b.time,'%%h:%%i'),b.quantity,DATE_FORMAT(b.currentdatetime, '%%d-%%M-%%Y') FROM booking b JOIN items i on i.id = b.oid WHERE b.bid = %s"%bid
        item = getData(sql) 
        _topic = "Dear %s \n We have received your order for %s. The ordered details are listed below: \n item  \t :%s \n Place \t : %s \n Date \t :%s \n Time \t : %s \n Quantity \t : %s \n Your order with above mentioned details are waiting for the approval by the Karma Caters \n \t further contact call : 8547579358 | 8089459358\n With regards \n KARMA CATERS \n Date \t : %s "%(item[0][0].title(), item[0][1].title(), item[0][1].title(), item[0][2], item[0][3], item[0][4], item[0][5], item[0][6])
        print("topic",_topic)
        _sub = "Karma Caters Order Placed for %s"%item[0][1].title()
        _to = [''+data['email']+'']
        mseg = Message(_sub, sender = 'karma.caters007@gmail.com', recipients = _to)
        mseg.body = _topic
        mail.send(mseg)
        return redirect("/")
    msg = "Something went wrong..!"
    return redirect('/booking/<%s>'%id)

"""Admin section"""
@app.route('/Admin')
def admin():
    if 'uid' in session and 'role' in session:
        return redirect('/'+session['role']+'/home')
    else:
        return render_template('Admin/login.html')

@app.route('/login', methods = ["POST"])
def login():
    if 'uid' in session and 'role' in session:
        return redirect('/'+session['role']+'/home')
    msg = ''
    if request.method == 'POST':
        data = request.form
        sql = "select log_id,role,username,password from login where username=%s and password=%s"
        vals = (data['email'],data['pswd'])
        res = getData(sql,vals)
        if len(res):
            # resp = make_response(render_template('Admin/login.html'))
            # resp.set_cookie('uid', res[0][0])
            # resp.set_cookie('role', res[0][1])
            # resp.set_cookie('user', res[0][2])
            session['uid'] = res[0][0]
            session['role'] = res[0][1]
            session['user'] = res[0][2]
            role = request.cookies.get('role')
            return redirect('/'+res[0][1]+'/home')
        else:
            msg = 'Invalid login details'
    return render_template('Admin/login.html',msg=msg)

@app.route('/Admin/home')
def adminHome():
    msg = ""
    if 'user' in session and 'uid' in session and 'role' in session:
        sql = "select * from upload"
        res = getData(sql)
        user = session['user']
        return render_template('Admin/menu.html',user = user, res = res)
    else:msg = 'Invalid login details'
    return render_template('Admin/login.html',msg=msg)

@app.route('/Admin/Booking')
def adminBokking():
    if 'user' in session and 'uid' in session and 'role' in session:
        sql = "SELECT b.bid, b.name, b.email, b.contact, i.item,b.place,b.quantity, DATE_FORMAT(b.date,'%d-%M-%Y'), TIME_FORMAT(b.time,'%h:%i'), DATE_FORMAT(b.currentdatetime,'%d-%M-%Y') FROM booking b JOIN items i on i.id = b.oid where checked = 0 ORDER BY b.currentdatetime DESC"
        new = getData(sql)
        sql = "SELECT b.bid, b.name, b.email, b.contact, i.item,b.place,b.quantity, DATE_FORMAT(b.date,'%d-%M-%Y'), TIME_FORMAT(b.time,'%h:%i'), DATE_FORMAT(b.currentdatetime,'%d-%M-%Y') FROM booking b JOIN items i on i.id = b.oid where checked = 1 ORDER BY b.currentdatetime DESC"
        res = getData(sql)
        return render_template('Admin/Booking.html', new = new, res = res)
    else:
        return render_template('Admin/login.html')

@app.route('/Admin/approved/<int:id>')
def adminApproved(id):
    if 'user' in session and 'uid' in session and 'role' in session:
        sql = "update booking set checked = 1 where bid = %s"%id
        setData(sql)
        sql = "SELECT b.name,i.item,b.place,DATE_FORMAT(b.date,'%%d-%%M-%%Y'),TIME_FORMAT(b.time,'%%h:%%i'),b.quantity,LEFT(b.currentdatetime, 10), b.email FROM booking b JOIN items i on i.id = b.oid WHERE b.bid = %s"%id
        item = getData(sql) 
        _topic = "Dear %s \n We have received your order for %s. The order details are listed below: \n item  \t :%s \n Place \t : %s \n Date \t :%s \n Time \t : %s \n Quantity \t : %s \n Your order is approved by the Karma Caters with above mentioned details, We are happy to serve you with joy....\n \t further contact call : 8547579358 | 8089459358 , hope you are fine.. and ones again Thankyou for your booking..\n With regards \n KARMA CATERS \n Date \t : %s "%(item[0][0].title(), item[0][1].title(), item[0][1].title(), item[0][2], item[0][3], item[0][4], item[0][5], item[0][6])
        print("topic",_topic)
        _sub = "Karma Caters Order Placed for %s"%item[0][1].title()
        _to = [''+item[0][7]+'']
        mseg = Message(_sub, sender = 'karma.caters007@gmail.com', recipients = _to)
        mseg.body = _topic
        mail.send(mseg)
        return redirect('/Admin/Booking')
    else:
        return render_template('Admin/login.html')


@app.route('/Admin/edit')
def adminEdit():
    if 'user' in session and 'uid' in session and 'role' in session:
        return render_template('Admin/edit.html')
    else:return render_template('Admin/login.html')

@app.route('/Admin/editProfile', methods=['POST'])
def adminProfile():
    if 'user' in session and 'uid' in session and 'role' in session:
        msg = ""
        id = session['uid']
        if request.method == "POST":
            data = request.form
            sql = "select password from login where log_id = %s and password = %s"
            vals = (id, data['opswd'])
            res = getData(sql, vals)
            if len(res):
                if data['npswd'] == data['cpswd']:
                    sql = "update login set username = %s, password = %s where log_id = %s"
                    vals = (data['email'], data['npswd'], id)
                    setData(sql, vals)
                    session['user'] = data['email'] 
                    user = session['user']
                    return render_template('Admin/menu.html',user = user)
                else: msg = "password must not match..!"
            else: msg = "incorrept password..!"
        return render_template("Admin/edit.html", msg = msg)
    else:msg = 'Invalid login details'
    return render_template('Admin/login.html',msg=msg)

@app.route('/Admin/uploads')
def adminUpload():
    if 'user' in session and 'uid' in session and 'role' in session:
        return render_template("Admin/uploads.html")
    else:return render_template('Admin/login.html')

@app.route('/Admin/addpost', methods = ['POST'])
def adminAddpost():
    if 'user' in session and 'uid' in session and 'role' in session:
        msg = ""
        if request.method == 'POST':
            data = request.form['descr']
            file = request.files['file']
            sql = "select ifnull(max(uid),0)+1 from upload"
            pid = getData(sql)[0][0]
            fname = file.filename.split('.')[-1]
            fname = '%s.%s' % (pid,fname)
            sql = "insert into upload values(%s, %s, %s, current_date,current_time)"
            vals = (pid, data, fname)
            setData(sql,vals)
            file.save('static/uploads/'+secure_filename(fname))
            return redirect('/Admin/uploads')
        return render_template("Admin/uploads.html")
    else:return render_template('Admin/login.html')

@app.route('/Admin/Editpost/<int:id>', methods = ["POST"])
def adminEditPost(id):
    if 'user' in session and 'uid' in session and 'role' in session:
        msg = ""
        if request.method == 'POST':
            data = request.form['descr']
            file = request.files['file']
            sql = "select img from upload where uid = %s"%id
            r = getData(sql)
            os.remove('static/uploads/%s'%r[0][0])
            fname = file.filename.split('.')[-1]
            fname = '%s.%s' % (id,fname)
            sql = "update upload set discription = %s, img = %s where uid = %s"
            vals = (data, fname, id)
            setData(sql,vals)
            file.save('static/uploads/'+secure_filename(fname))
            return redirect('/Admin/home')
        sql = "select * from upload where uid = %s"%id
        res = getData(sql)
        return render_template("Admin/UpEdit.html", res = res)
    else:return render_template('Admin/login.html')

@app.route('/Admin/reviews')
def adminReview():
    if 'user' in session and 'uid' in session and 'role' in session:
        sql = "select * from feedback"
        res = getData(sql)
        return render_template('Admin/review.html', res = res)
    else:return render_template('Admin/login.html')

@app.route('/Admin/claerReview')
def adminClaerReview():
    if 'user' in session and 'uid' in session and 'role' in session:
        msg = ""
        sql = "delete from feedback"
        setData(sql)
        msg = "No Reviews here..!"
        return render_template('Admin/review.html', msg = msg)
    else:return render_template('Admin/login.html')
    
@app.route('/Admin/ViewItems')
def adminItemView():
    if 'user' in session and 'uid' in session and 'role' in session:
        sql = 'select * from items'
        res = getData(sql)
        return render_template('Admin/AddItem.html', res = res)
    else:return render_template('Admin/login.html')

@app.route('/Admin/AddItems', methods = ["POST"])
def adminAddItem():
    if 'user' in session and 'uid' in session and 'role' in session:
        if request.method == "POST":
            data = request.form['descr']
            file = request.files['file']
            sql = "select ifnull(max(id),0)+1 from items"
            pid = getData(sql)[0][0]
            fname = file.filename.split('.')[-1]
            fname = '%s.%s' % (pid,fname)
            sql = "insert into items values(%s, %s, %s)"
            vals = (pid, data, fname)
            setData(sql, vals)
            file.save('static/Items/'+secure_filename(fname))
            return redirect('/Admin/ViewItems')
        return render_template("Admin/review.html")
    else:return render_template('Admin/login.html')

@app.route('/Admin/deleteItem/<int:id>')
def adminEditItem(id):
    if 'user' in session and 'uid' in session and 'role' in session:
        sql = 'select img from items where id = %s'%id
        r = getData(sql)
        sql = "delete from items where id = %s"%id
        setData(sql)
        os.remove('static/Items/%s'%r[0][0])
        sql = 'select * from items'
        res = getData(sql)
        return render_template('Admin/AddItem.html', res = res)
    else:return render_template('Admin/login.html')

@app.route('/Admin/UploadDel/<int:id>')
def adminDeleteUploads(id):
    if 'user' in session and 'uid' in session and 'role' in session:
        sql = "select img from upload where uid = %s"%id
        r = getData(sql)
        sql = "delete from upload where uid = %s"%id
        setData(sql)
        os.remove('static/uploads/%s'%r[0][0])
        sql = "select * from upload"
        res = getData(sql)
        user = session['user']
        return render_template('Admin/menu.html',user = user, res = res)
    else:return render_template('Admin/login.html')

@app.route('/Admin/EditView/<int:id>')
def adminUpEdit(id):
    if 'user' in session and 'uid' in session and 'role' in session:
        sql = "select * from upload where uid = %s"%id
        res = getData(sql)
        return render_template('Admin/UpEdit.html', res = res)
    else:return render_template('Admin/login.html')

@app.route('/Admin/logout')
def logout():
    del session['uid']
    del session['role']
    del session['user']
    session.pop('uid', None)
    session.pop('role', None)
    session.pop('user', None)
    print("logout")
    return redirect('/')


if __name__ == '__main__':
   app.run(debug = True)
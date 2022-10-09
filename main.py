import datetime
from datetime import datetime
from flask import Flask, render_template, request, redirect, url_for, session, flash
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.secret_key = "hi"
app.config["SQLALCHEMY_DATABASE_URI"] = 'sqlite:///users.sqlite3'
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
db = SQLAlchemy(app)


#DB config-----------------------------------------------------------------

class users(db.Model):
    _id = db.Column("id", db.Integer, primary_key=True)
    name = db.Column(db.String(255))
    password = db.Column(db.String(255))

    def __init__(self, name, password):
        self.name = name
        self.password = password

class posts(db.Model):
    _id = db.Column("id", db.Integer, primary_key=True)
    title = db.Column(db.String(255))
    text = db.Column(db.String(500))

    def __init__(self, title, text):
        self.title = title
        self.text = text

class follow(db.Model):
    user = db.Column(db.String(255), db.ForeignKey('users.name'), primary_key=True)
    follower = db.Column(db.String(255), db.ForeignKey('users.name'), primary_key=True)

    def __init__(self, user1, user2):
        self.user = user1
        self.follower = user2

class make_post(db.Model):
    _id = db.Column("id", db.Integer, db.ForeignKey('posts.id'), primary_key=True)
    user = db.Column(db.String(255), db.ForeignKey('users.name'), primary_key=True)
    date = db.Column(db.DateTime)

    def __init__(self, user, idP, date):
        self.user = user
        self._id = idP
        self.date = date

#routes---------------------------------------------------------------------
@app.route("/", methods=['POST', 'GET'])
def login():
    if request.method == 'POST':
        user = request.form["name"]
        password = request.form["password"]
        find = users.query.filter_by(name=user).first()
        if find:
            if find.password == password:
                session["user"] = user
                session["password"] = password
            else:
                return redirect(url_for("login"))
        else:
            usr = users(user, password)
            db.session.add(usr)
            db.session.commit()

        return redirect(url_for("user"))
        
    if "user" in session:
        return redirect(url_for("user"))
    return render_template('login.html')


@app.route("/user/", methods=['GET'])
def user():
    if "user" in session:
        user = {}
        user["name"] = session["user"]
        return render_template('users.html', user=user)
    return redirect(url_for("login"))

@app.route("/home/", methods=['POST', 'GET'])
def home():
    if "user" in session:
        return render_template('index.html')
    return redirect(url_for("login"))

@app.route("/logout/")
def logout():
    session.pop("user", None)
    session.pop("password", None)
    flash("Get out!", "info")
    return redirect(url_for("login"))

@app.route("/makepost/", methods=['POST'])
def make():
    print(request.json)
    return {"msg": "oi"}
    date = datetime.now()
    getPost = make_post.query.filter_by(date=date)
    if getPost:
        print("Já fez post hj")
    else:
        title = request.form["title"]
        text = request.form["text"]

        post = posts(title, text)
        db.session.add(post)
        db.session.commit()

        make = make_post(session["user"], post._id, date)
        db.session.add(make)
        db.session.commit()
    

#debug mode-----------------------------------------------------------------
if __name__ == '__main__':
    db.create_all()
    app.run(debug=True, port=3000)
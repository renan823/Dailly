import datetime
from datetime import datetime
from flask import Flask, render_template, request, redirect, url_for, session, make_response, jsonify
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.sql import extract

app = Flask(__name__)
app.secret_key = "hi"
app.config["SQLALCHEMY_DATABASE_URI"] = 'sqlite:///dailly.sqlite3'
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
    user = db.Column(db.Integer, db.ForeignKey('users.name'), primary_key=True)
    follower = db.Column(db.Integer, db.ForeignKey('users.name'), primary_key=True)

    def __init__(self, user1, user2):
        self.user = user1
        self.follower = user2

class make_post(db.Model):
    _id = db.Column("id", db.Integer, db.ForeignKey('posts.id'), primary_key=True)
    user = db.Column(db.Integer, db.ForeignKey('users.name'), primary_key=True)
    date = db.Column(db.DateTime, default=datetime.utcnow())

    def __init__(self, user, idP):
        self.user = user
        self._id = idP


#functions------------------------------------------------------------------
def countFollowers(user):
    return follow.query.filter_by(follower=user).count()

def countFollowing(user):
    return follow.query.filter_by(user=user).count()

def countPosts(user):
    return make_post.query.filter_by(user=user).count()

def searchUser(name):
    search = "%{}%".format(name)
    return users.query.filter(users.name.like(search)).all()

def getUserName(user):
    user = users.query.filter_by(_id = user).first()
    return user.name

def getFollowers(user):
    return follow.query.filter_by(user=user).all()

def getFollowing(user):
    return follow.query.filter_by(follower=user).all()

def getUsers(req):
    users = searchUser(req["name"])

    resultFollowers = []
    followers = getFollowing(session["id"])
    for follower in followers:
        resultFollowers.append(follower)

    resultUsers = []
    for user in users:
        if user._id != session["id"]:
            flag = True
            for follower in followers:
                if int(user._id) == int(follower.follower):
                    flag = False
                    break
            if flag:
                resultUsers.append({"name": user.name, "_id": user._id, })
    return resultUsers

def getPostsByUser(user):
    postList = []
    preResult = make_post.query.filter_by(user=user).all()
    for result in preResult:
        user = getUserName(result.user)
        post = posts.query.filter_by(_id = result._id).first()
        postList.append({"title": post.title, "text": post.text, "user": user})
    return postList

def getAllPosts():
    resultFollowers = []
    followers = getFollowers(session["id"])
    for follower in followers:
        resultFollowers.append(follower)

    resultPosts = []
    
    for follower in resultFollowers:
        posts = getPostsByUser(follower.follower)
        if len(posts) != 0:
            resultPosts.append(posts)
    return resultPosts


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
                session["id"] = find._id
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
        user["followers"] = countFollowers(session["id"])
        user["following"] = countFollowing(session["id"])
        user["posts"] = countPosts(session["id"])
        return render_template('users.html', user=user)
    return redirect(url_for("login"))

@app.route("/home/", methods=['GET'])
def home():
    if "user" in session:
        return render_template('index.html')
    return redirect(url_for("login"))

@app.route("/logout/")
def logout():
    session.pop("user", None)
    session.pop("password", None)

    return redirect(url_for("login"))

@app.route("/post/new/", methods=['POST'])
def make():
    req = request.get_json(force=True)
    date = datetime.now()
    getPost = make_post.query.filter_by(user=session["id"]).filter(extract('day', make_post.date) == date.day).all()
    
    if getPost:
        return make_response(jsonify({"msg": "Você já fez um post hoje!", "status": "BAD"}), 200)
    else:
        post = posts(req["title"], req["text"])
        db.session.add(post)
        db.session.commit()

        make = make_post(session["id"], post._id)
        db.session.add(make)
        db.session.commit()

    return make_response(jsonify({"msg": "Post publicado!", "status": "OK"}), 200)
    
@app.route("/search/", methods=['POST'])
def search():
    req = request.get_json(force=True)
    resultUsers = getUsers(req)

    return make_response(jsonify({"users": resultUsers}), 200)

@app.route("/follower/", methods=['POST'])
def follower():
    req = request.get_json(force=True)

    newFollow = follow(session["id"], req["user"])
    db.session.add(newFollow)
    db.session.commit()

    return make_response(jsonify({"status": "OK"}), 200)

@app.route("/user/followers/", methods=['POST'])
def getUserFollowers():
    followers = countFollowers(session["id"])
    following = countFollowing(session["id"])
    posts = countPosts(session["id"])

    return make_response(jsonify({"followers": followers, "following": following, "posts": posts,"status": "OK"}), 200)

@app.route("/post/get/", methods=['POST'])
def getPosts():
    return make_response(jsonify({"posts": getAllPosts(), "status": "OK"}), 200)

#debug mode-----------------------------------------------------------------
if __name__ == '__main__':
    db.create_all()
    app.run(debug=True, port=3000)

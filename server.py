import json
from flask import Flask, render_template , request , redirect , url_for
from modules.user import users_sessions
import os

with open("login.json") as file:
    login_data = json.load(file)['users']

app = Flask(__name__,template_folder="Template")
app.config["SESSION_PERMANENT"] = False
app.config["SESSION_TYPE"] = "filesystem"
# Session(app)

session = dict()

@app.route("/login",methods=["GET","POST"])
def login():
    if request.method == "POST":
        username = request.form.get("username")
        password = request.form.get("pass")
        ipaddress = request.remote_addr
        if {username:password} in login_data:
            user = users_sessions.user(username,ipaddress)
            return redirect(url_for(".share_content",username=user.username,session=user.session))
    return render_template("login form/index.html")

@app.route("/share")
def share_content():
    try:
        username = request.args["username"]
        session = request.args["session"]
    except:
        return redirect("/login")
    if session in users_sessions.user_id:
        contents = os.listdir("./share")
        return render_template("share page/index.html",content=contents,username=username,session=session)
    else:
        return redirect("/login")
    

app.run(debug=True) 
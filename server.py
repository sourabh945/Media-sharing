import json
from flask import Flask, render_template , request , redirect , url_for
from modules.user import users_sessions
import os

################## database exposer #######################

with open("database/login.json") as file:
    login_data = json.load(file)['users']

with open("database/admin.json") as file:
    admin_login = json.load(file)['admin']

##########################################################

app = Flask(__name__,template_folder="Template")
app.config["SESSION_PERMANENT"] = False
app.config["SESSION_TYPE"] = "filesystem"

################ web pages ################################

@app.route("/")
def home():
    return redirect("/login")

### admin login page ###

@app.route("/adminlogin" , methods=["GET","POST"])
def admin():
    if request.method == "POST":
        username = request.form.get("username")
        password = request.form.get("pass")
        ipaddress = request.remote_addr
        if {username:password} in admin_login:
            user = users_sessions.user("admin",ipaddress)
            return redirect('.share')
    return render_template("admin login/index.html")

### member login page ###

@app.route("/login",methods=["GET","POST"])
def login():
    if request.method == "POST":
        username = request.form.get("username")
        password = request.form.get("pass")
        ipaddress = request.remote_addr
        if {username:password} in login_data:
            user = users_sessions.user(username,ipaddress)
            return share_content(user)
    return render_template("login form/index.html")

@app.route("/share")
def share_content(user):
    if user.session in users_sessions.user_id:
        contents = os.listdir("./share")
        return render_template("share page/index.html",content=contents,username=user.username,session=user.session)
    else:
        return redirect("/login")




if __name__ == "__main__":

    app.run(debug=True) 
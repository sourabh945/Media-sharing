import json
from flask import Flask, render_template , request , redirect 
from modules.user import users_module
from modules.listdir import ls
import os
import datetime 


################## user defined parameters ###################

re_login_time = 1 # time after the re-login is required to access the files in hours

folder_path = "./share"


################## database exposer #######################

with open("database/login.json") as file:
    login_data = json.load(file)

with open("database/admin.json") as file:
    admin_login = json.load(file)['admin']

##########################################################

app = Flask(__name__,template_folder="Template")
app.config["SESSION_PERMANENT"] = False

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
            user = users_module.user("admin",ipaddress)
            return folder(user,folder_path)
    return render_template("admin login/index.html")

### member login page ###

@app.route("/login",methods=["GET","POST"])
def login():
    if request.method == "POST":
        username = request.form.get("username")
        password = request.form.get("pass")
        ipaddress = request.remote_addr
        if username in login_data.keys() and login_data[username] == password:
            user = users_module.user(username,ipaddress)
            return (folder(user,folder_path))
        else:
            return 
    return render_template("login form/index.html")

### share page ###

@app.route("/content")
def folder(user,path):
    if (datetime.datetime.now() - user.time_of_login).seconds > re_login_time*60*60: 
        user.logout()
        return redirect("/login")
    if user.session_id in users_module.session_ids:
        contents = ls(path)
        return render_template("share page/index.html",content=contents,username=user.username,session=user.session_id,path=path)


if __name__ == "__main__":

    app.run(debug=True) 
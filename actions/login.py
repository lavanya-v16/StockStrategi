from flask import Flask, render_template, redirect, url_for, Blueprint, request,flash
from werkzeug.security import generate_password_hash, check_password_hash
import sqlite3
from db_manager import LoginManager,DatabaseManager

login_action = Blueprint("login_action", __name__)

@login_action.route("/login",methods=["POST"])
def login():
    db_manager=DatabaseManager('database.db')
    login_manager=LoginManager(db_manager)
    l=[]
    user=request.form.get("name")
    pswd=request.form.get("pswd")
    password_hash = generate_password_hash(pswd)
    login=request.form.get("login")
    listofusers= login_manager.get_user(user)
    usernames = [row[0] for row in listofusers]
    print(usernames)
    listofpassword=login_manager.get_password(user)
    userpasswords=[row[0] for row in listofpassword]
    if (login and user in usernames):
        if check_password_hash(userpasswords[0],pswd):
            return redirect(url_for("transaction_route.transaction_input",username=user))
        else:
            flash("Invalid password")
            return render_template("app_pages/home.html")
    else:
        print(listofusers)
        flash("Invalid username")
        return render_template("app_pages/home.html")



#login to create
#login to transaction_input
from flask import Flask,redirect, url_for, Blueprint, request,flash
from werkzeug.security import generate_password_hash
import sqlite3
from db_manager import UserManager,DatabaseManager

create_action=Blueprint("create_action", __name__)


@create_action.route("/create",methods=["POST"])
def create():
    db_manager=DatabaseManager('database.db')
    user_manager=UserManager(db_manager)
    checker=0
    user=request.form.get("name")
    pswd=request.form.get("pswd")
    print(user,"user")
    password_hash = generate_password_hash(pswd)
    create=request.form.get("create")
    namesindb=user_manager.get_user()
    if namesindb==[]:
            user_manager.insert_user(user,password_hash)
            flash("Account created successfully! Please log in.")
            return redirect(url_for("home"))
    else:
        checker=0
        for i in range(len(namesindb)):
            if namesindb[i][0]==user:
                checker=100
                flash("Account already exists")
                break
        if checker==0:
            user_manager.insert_user(user,password_hash)
            flash("Account created successfully! Please log in.")

        return redirect(url_for("home"))



#create to home
from flask import Flask, render_template, redirect, url_for, Blueprint, request,flash
from werkzeug.security import generate_password_hash, check_password_hash
import sqlite3

login_route = Blueprint("login_route", __name__)

con=sqlite3.connect('database.db',check_same_thread=False)
cur=con.cursor()

@login_route.route("/login",methods=["POST","GET"])
def login():
    if request.method=="POST":
            l=[]
            user=request.form.get("name")
            pswd=request.form.get("pswd")
            password_hash = generate_password_hash(pswd)
            login=request.form.get("login")
            cur.execute('SELECT username from USER1 where username=?',(user,))
            listofusers=cur.fetchall()
            usernames = [row[0] for row in listofusers]
            print(usernames)
            cur.execute('select password_hash from USER1 where username=?',(user,))
            listofpassword=cur.fetchall()
            userpasswords=[row[0] for row in listofpassword]
            # print("userpasswords", userpasswords[0])
            #
            # print("passwordhash",password_hash)
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

    return render_template("app_pages/home.html")


#login to create
#login to transaction_input
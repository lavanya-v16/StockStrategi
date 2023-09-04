from flask import Flask, render_template, redirect, url_for, Blueprint, request,flash
from werkzeug.security import generate_password_hash
import sqlite3

create_route=Blueprint("create_route", __name__)

con=sqlite3.connect('database.db',check_same_thread=False)
cur=con.cursor()

@create_route.route("/create",methods=["POST","GET"])
def create():
    if request.method=="POST":
        checker=0
        user=request.form.get("name")
        pswd=request.form.get("pswd")
        print(user,"user")
        password_hash = generate_password_hash(pswd)
        create=request.form.get("create")
        cur.execute("Select * from User1")
        namesindb=cur.fetchall()
        print(namesindb)
        if namesindb==[]:
                cur.execute('INSERT INTO USER1 (username, password_hash) VALUES(?,?)',(user,password_hash))
                con.commit()
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
                cur.execute('INSERT INTO USER1 (username, password_hash) VALUES(?,?)',(user,password_hash))
                con.commit()
                flash("Account created successfully! Please log in.")

            return redirect(url_for("home"))

    return render_template("app_pages/create.html")


#create to home
from flask import Flask, render_template,Blueprint
import sqlite3


login_route = Blueprint("login_route", __name__)

@login_route.route("/login",methods=["GET"])
def login():
    return render_template("app_pages/home.html")


#login to create
#login to transaction_input
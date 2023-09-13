from flask import Flask, render_template, Blueprint
import sqlite3

create_route=Blueprint("create_route", __name__)


@create_route.route("/create",methods=["GET"])
def create():
    return render_template("app_pages/create.html")


#create to home
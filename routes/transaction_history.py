from flask import Flask, render_template, redirect, url_for, Blueprint, request,flash
from werkzeug.security import generate_password_hash, check_password_hash
import sqlite3

transactionhistory_route = Blueprint("transactionhistory_route", __name__)

con=sqlite3.connect('database.db',check_same_thread=False)
cur=con.cursor()

@transactionhistory_route.route("/transaction history/<username>", methods=["POST", "GET"])
def transaction_history(username):
    if request.method=="POST":
        back=request.form.get("goback")
        if back:
            print("inside back")
            return redirect(url_for("transaction_route.transaction_input",username=username))
    con.row_factory = sqlite3.Row
    cur.execute("SELECT rowid, * from Stockuser where username=?", (username,))
    rows = cur.fetchall()
    print(rows)
    return render_template("app_pages/transaction_history.html", rows=rows)
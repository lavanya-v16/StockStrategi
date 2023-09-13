from flask import Flask, redirect, url_for, Blueprint, request,flash
import sqlite3

transactionhistory_action = Blueprint("transactionhistory_action", __name__)


@transactionhistory_action.route("/transaction history/<username>", methods=["POST"])
def transaction_history(username):
    print("actions")
    back=request.form.get("goback")
    log=request.form.get("logout")
    if back:
        print("inside back")
        return redirect(url_for("transaction_route.transaction_input",username=username))
    if log:
        return redirect(url_for("home"))
    
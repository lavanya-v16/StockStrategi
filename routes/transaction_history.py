from flask import Flask, render_template, Blueprint
import sqlite3
from db_manager import DatabaseManager, StockManager

transactionhistory_route = Blueprint("transactionhistory_route", __name__)


@transactionhistory_route.route("/transaction history/<username>", methods=["GET"])
def transaction_history(username):
    print("hi")
    db_manager = DatabaseManager('database.db')
    stock_manager = StockManager(db_manager)
    rows=stock_manager.get_stock_user(username)
    print("bye")
    return render_template("app_pages/transaction_history.html", rows=rows)

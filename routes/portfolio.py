from flask import Flask, render_template, redirect, url_for, Blueprint, request,flash
from werkzeug.security import generate_password_hash
import sqlite3
import yfinance as yf
from datetime import datetime

portfolio_route=Blueprint("portfolio_route", __name__)

con=sqlite3.connect('database.db',check_same_thread=False)
cur=con.cursor()


@portfolio_route.route("/portfolio/<username>",methods=["POST", "GET"])
def portfolio(username):
        sumlist=[]
        print("helooooo from calc")
        con.row_factory=sqlite3.Row
        cur.execute("SELECT rowid, * from Portfoliouser where username=?",(username,))
        rows=cur.fetchall()
        if request.method=="POST":
            b=request.form.get("back")
            if b:
                print("inside back")
                return redirect(url_for("transaction_route.transaction_input",username=username))
        costpricesum=cur.execute("Select sum(buyprice) from Portfoliouser where username=?",(username,))
        costpricesum=cur.fetchall()
        todayvaluesum=cur.execute("Select sum(VALUE_CMP) from Portfoliouser where username=?",(username,))
        todayvaluesum=cur.fetchall()
        profitlosssum=cur.execute("Select sum(PROFIT_LOSS) from Portfoliouser where username=?",(username,))
        profitlosssum=cur.fetchall()
        if profitlosssum:
                percentvalue=round((profitlosssum[0][0]/costpricesum[0][0])*100,2)
                sumlist.append(costpricesum[0][0])
                sumlist.append(todayvaluesum[0][0])
                sumlist.append(profitlosssum[0][0])
                sumlist.append(percentvalue)
                return render_template("app_pages/portfolio.html",rows=rows,sumlist=sumlist)     #all the entries are stored in b and sent to the template
        else:
              msg="no record found"
              return render_template("app_pages/portfolio.html",error=msg)     #all the entries are stored in b and sent to the template
              
        


#portfolio to transaction input
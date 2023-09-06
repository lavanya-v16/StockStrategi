from flask import Flask, render_template, redirect, url_for, Blueprint, request, flash
from werkzeug.security import generate_password_hash
import sqlite3
import yfinance as yf
from datetime import datetime

transaction_route = Blueprint("transaction_route", __name__)

con = sqlite3.connect('database.db', check_same_thread=False)
cur = con.cursor()

k = []


@transaction_route.route("/transaction/<username>", methods=["POST", "GET"])
def transaction_input(username):
    flag = 0
    Action = ''
    if request.method == "POST":
        try:
            transaction_history = request.form.get("thistory")
            buy = request.form.get("buy")
            sell = request.form.get("sell")
            logout = request.form.get("logout")
            if buy:
                Action = 'Buy'
                sname = request.form["stock-name"]
                sqty = request.form["stock-quantity"]
                sdate = request.form["start-date"]
                l = []
                l.append(sname)
                l.append(sqty)
                l.append(sdate)
                flag = -1
                buyprice = cp_calc(sdate, sqty, sname, flag)  # buy price
                print(buyprice, "buyprice of ", sqty)
                flag = 0
                costprice = cp_calc(sdate, sqty, sname, flag)  # cost price
                print(costprice)
                flag = 1
                todayvalue = cp_calc(sdate, sqty, sname, flag)  # shares current price
                flag = 2
                currenttotal = cp_calc(sdate, sqty, sname, flag)  # total amount now wrt current price
                pl = round(currenttotal - costprice, 2)  # profit or loss
                l.append(costprice)
                l.append(todayvalue)
                l.append(currenttotal)
                l.append(pl)
                k.append(l)
                print(k)
                cur.execute(
                    "INSERT INTO Stockuser(username,stockname,qty,buydate,todayvalue,buyprice) VALUES (?,?,?,?,?,?)",
                    (username, sname, sqty, sdate, buyprice, costprice))
                print("inserted into stock")
                cur.execute("Select * from Portfoliouser where username=?", (username,))
                prow = cur.fetchall()
                print(prow)
                if prow == []:
                    print("hi this is prow creation")
                    cur.execute(
                        "INSERT INTO Portfoliouser(username,stockname,qty,todayvalue,buyprice,CMP,VALUE_CMP,PROFIT_LOSS) VALUES (?,?,?,?,?,?,?,?)",
                        (username, sname, sqty, buyprice, costprice, todayvalue, currenttotal, pl))
                    con.commit()
                else:
                    entrycount = 0
                    # i[0]=username prow[i][1]=stockname i[2]=qty i[3]=todayvalue i[4]=buyprice i[5]=cmp i[6]=vcmp i[7]=pl
                    for i in range(len(prow)):
                        print("sname", prow[i][1])
                        if prow[i][1] == sname:
                            entrycount = 100
                            print("sname inside", sname)
                            print(prow[i][2])
                            print(sqty)
                            total_quantity = int(sqty) + int(prow[i][2])
                            print("total_quantity", total_quantity)
                            print("value fetched", prow[i][3])
                            buyprice_port = round(
                                ((buyprice * int(sqty)) + (prow[i][3] * int(prow[i][2]))) / total_quantity, 2)
                            print(buyprice_port)
                            costprice_port = round(buyprice_port * total_quantity, 2)
                            print("costprice_port", costprice_port)
                            stock_name = yf.Ticker(sname)
                            end_date = datetime.now().strftime('%Y-%m-%d')
                            stock_name_history = stock_name.history(start=sdate, end=end_date)
                            cmprice = round(stock_name_history.Close[-1], 2)  # todays value of stock
                            print("cmp", cmprice)
                            vcmp = round(cmprice * total_quantity, 2)  # total value of entire investment
                            pl = round(vcmp - costprice_port, 2)
                            print(vcmp, costprice_port, pl)
                            cur.execute(
                                "UPDATE Portfoliouser SET username=(?),stockname=(?),qty=(?),todayvalue=(?),buyprice=(?),CMP=(?),VALUE_CMP=(?),PROFIT_LOSS=(?) Where stockname=(?)",
                                (username, sname, total_quantity, buyprice_port, costprice_port, cmprice, vcmp, pl,sname))
                            print("updated")
                            con.commit()
                            break
                    if entrycount == 0:
                        cur.execute(
                            "INSERT INTO Portfoliouser(username,stockname,qty,todayvalue,buyprice,CMP,VALUE_CMP,PROFIT_LOSS) VALUES (?,?,?,?,?,?,?,?)",
                            (username, sname, sqty, buyprice, costprice, todayvalue, currenttotal, pl))
                        print("didnt exist so added")
                con.commit()
                msg = "Record added successfully"
                print(msg)
                con.row_factory = sqlite3.Row
                cur.execute("SELECT rowid, * from Portfoliouser where username=?", (username,))
                rows = cur.fetchall()
                return render_template("app_pages/transaction_input.html",rows=rows)
            if sell:
                print("SELLLLLL")
                sname = request.form["stock-name"]
                sqty = request.form["stock-quantity"]
                sdate = request.form["start-date"]
                negativeqty=int('-'+sqty)           #negative of the number
                print(sname,sqty,sdate,"from sell")
                Action = "Sell"
                flag = 1
                todayvalue = cp_calc(sdate, sqty, sname, flag)  # shares current price
                print("type",type(negativeqty))
                print(todayvalue)
                flag = 2
                currenttotal = cp_calc(sdate, sqty, sname, flag)  # total amount now wrt current price
                print(currenttotal)
                print("printing: ",username,sname,negativeqty,sdate,todayvalue,currenttotal) #, sname, negativeqty, sdate, buyprice, costprice)
                sell_option(username,sname,negativeqty,sdate,todayvalue,currenttotal)
                cur.execute("Select * from Portfoliouser where username=?", (username,))
                prow = cur.fetchall()
                print(prow)
                if prow == []:
                    print("error")
                    return redirect(url_for("transaction_route.transaction_input", username=username))
                else:
                    entrycount = 0
                    # i[0]=username prow[i][1]=stockname i[2]=qty i[3]=todayvalue i[4]=buyprice i[5]=cmp i[6]=vcmp i[7]=pl
                    for i in range(len(prow)):
                        print("sname", prow[i][1])
                        if prow[i][1] == sname:
                            entrycount = 100
                            print("sname inside", sname)
                            print(prow[i][2])
                            print(sqty)
                            total_quantity = negativeqty + int(prow[i][2])   #subtracting the sold qty from total qty
                            print("total_quantity", total_quantity)
                            print("value fetched", prow[i][3])
                            costprice_port = round(prow[i][3] * total_quantity, 2)   #multiplying reduced qty with exisitng avg cp for new total investment
                            print("costprice_port", costprice_port)
                            stock_name = yf.Ticker(sname)
                            end_date = datetime.now().strftime('%Y-%m-%d')
                            stock_name_history = stock_name.history(start=sdate, end=end_date)
                            cmprice = round(stock_name_history.Close[-1], 2)  # todays value of stock
                            print("cmp", cmprice)
                            vcmp = round(cmprice * total_quantity, 2)  # total value of entire investment
                            pl = round(vcmp - costprice_port, 2)  #unrealized profit
                            print(vcmp, costprice_port, pl)
                            print("error:",prow[i][3])
                            pl_relaized=(abs(negativeqty)*cmprice)-(abs(negativeqty)*prow[i][3]) #realized profit
                            cur.execute(
                                "UPDATE Portfoliouser SET username=(?),stockname=(?),qty=(?),buyprice=(?),CMP=(?),VALUE_CMP=(?),PROFIT_LOSS=(?) Where stockname=(?)",
                                (username, sname, total_quantity, costprice_port, cmprice, vcmp, pl,sname))
                            print("updated")
                            con.commit()
                            cur.execute("INSERT INTO Profitloss(username,stockname, qty, buydate, sellprice , PROFIT_LOSS ) VALUES (?,?,?,?,?,?)",(username,sname,sqty,sdate,cmprice,pl_relaized))
                            con.commit()
                            break
                    if entrycount == 0:
                        cur.execute(
                            "INSERT INTO Portfoliouser(username,stockname,qty,todayvalue,buyprice,CMP,VALUE_CMP,PROFIT_LOSS) VALUES (?,?,?,?,?,?,?,?)",
                            (username, sname, sqty, buyprice, costprice, todayvalue, currenttotal, pl))
                        print("didnt exist so added")
                return redirect(url_for("transaction_route.transaction_input", username=username))
                

            if transaction_history:
                return redirect(url_for("transactionhistory_route.transaction_history",username=username))
            if logout:
                print("logout")
                return redirect(url_for("home"))
            else:
                Flask.abort(404)
            return redirect(url_for("transaction_route.transaction_input", username=username))
        except:
            con.rollback()
            msg = "error in insert"
        finally:
            if buy:
                con.row_factory = sqlite3.Row
                cur.execute("SELECT rowid, * from Portfoliouser where username=?", (username,))
                rows = cur.fetchall()
                return render_template("app_pages/transaction_input.html", list_of_stock=k, rows=rows)
    else:
        con.row_factory = sqlite3.Row
        cur.execute("SELECT rowid, * from Portfoliouser where username=?", (username,))
        rows = cur.fetchall()
        return render_template("app_pages/transaction_input.html",rows=rows)

def sell_option(username, sname, negativeqty, sdate, todayvalue, currenttotal):
    Action='Sell'
    print("inside sell function",username, sname, negativeqty, sdate, todayvalue, currenttotal)
    cur.execute("INSERT INTO Stockuser(username,stockname,qty,buydate,todayvalue,buyprice) VALUES (?,?,?,?,?,?)",(username, sname, negativeqty, sdate, todayvalue, currenttotal))
    con.commit()
    print("sell", Action)
    con.row_factory = sqlite3.Row
    cur.execute("SELECT rowid, * from Portfoliouser where username=?", (username,))
    rows = cur.fetchall()
    return render_template("app_pages/transaction_input.html",rows=rows)
    

def cp_calc(date, qty, name, flag):
    print("hi frm cp")
    stock_name = yf.Ticker(name)
    end_date = datetime.now().strftime('%Y-%m-%d')
    stock_name_history = stock_name.history(start=date, end=end_date)
    if flag == -1:
        returnvalue = round(stock_name_history.Close[0], 2)
        return returnvalue
    if flag == 0:
        returnvalue =round(float(qty) * stock_name_history.Close[0], 2)
        return returnvalue
    if flag == 1:
        print("flag1")
        returnvalue = round(stock_name_history.Close[-1], 2)
        return returnvalue
    else:
        print("flag2")
        returnvalue = round(float(qty) * stock_name_history.Close[-1], 2)
        return returnvalue


def displaydb(username):
    print("helooooo")
    con.row_factory = sqlite3.Row
    cur.execute("SELECT rowid, * from Stockuser where username=?", (username,))
    rows = cur.fetchall()
    print(rows)
    return render_template("app_pages/transaction_input.html", list_of_stock=k, rows=rows)

# transaction input to home
# transaction input to portfolio
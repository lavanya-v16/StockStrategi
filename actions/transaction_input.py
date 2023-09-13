from flask import Flask, render_template, redirect, url_for, Blueprint, request
import sqlite3
import yfinance as yf
from datetime import datetime
from db_manager import DatabaseManager, StockManager,PortfolioManager,ProfitlossManager

transaction_action = Blueprint("transaction_action", __name__)


@transaction_action.route("/transaction/<username>", methods=["POST"])
def transaction_input(username):
    k=[]
    db_manager = DatabaseManager('database.db')
    stock_manager = StockManager(db_manager)
    portfolio_manager = PortfolioManager(db_manager)
    profitloss_manager=ProfitlossManager(db_manager)
    try:
        transaction_history = request.form.get("thistory")
        buy = request.form.get("buy")
        sell = request.form.get("sell")
        logout = request.form.get("logout")
        insights=request.form.get("insights")
        if buy:
            sname = request.form["stock-name"]
            sqty = request.form["stock-quantity"]
            sdate = request.form["start-date"]
            l = []
            l.extend([sname,sqty,sdate])
            buyprice = cp_calc(sdate, sqty, sname, flag=-1)  # buy price
            costprice = cp_calc(sdate, sqty, sname, flag=0)  # cost price
            todayvalue = cp_calc(sdate, sqty, sname, flag=1)  # shares current price
            currenttotal = cp_calc(sdate, sqty, sname, flag=2)  # total amount now wrt current price
            pl = round(currenttotal - costprice, 2)  # profit or loss
            l.extend([costprice,todayvalue,currenttotal,pl])
            k.append(l)
            stock_manager.insert_stock_user(username,sname, sqty, sdate, buyprice, costprice)
            prow=portfolio_manager.get_portfolio_user(username)
            if prow == []:
                portfolio_manager.insert_portfolio_user(username,sname, sqty, buyprice, costprice, todayvalue, currenttotal, pl)
            else:
                entrycount = 0
                # i[0]=username prow[i][1]=stockname i[2]=qty i[3]=todayvalue i[4]=buyprice i[5]=cmp i[6]=vcmp i[7]=pl
                for i in range(len(prow)):
                    if prow[i][1] == sname:
                        entrycount = 100
                        total_quantity = int(sqty) + int(prow[i][2])
                        buyprice_port = round(
                            ((buyprice * int(sqty)) + (prow[i][3] * int(prow[i][2]))) / total_quantity, 2)
                        costprice_port = round(buyprice_port * total_quantity, 2)
                        cmprice=cp_calc(sdate, sqty, sname, flag=1)
                        vcmp = round(cmprice * total_quantity, 2)  # total value of entire investment
                        pl = round(vcmp - costprice_port, 2)
                        portfolio_manager.update_portfolio_user(username, sname, total_quantity,buyprice_port, costprice_port, cmprice, vcmp, pl)
                        break
                if entrycount == 0:
                    portfolio_manager.insert_portfolio_user(username, sname, sqty, buyprice, costprice, todayvalue, currenttotal, pl)
            rows=portfolio_manager.get_portfolio_user(username)
            total_investment=portfolio_manager.get_buyprice_total(username)
            total_investment=round(total_investment[0][0],2)

            total_current_value=portfolio_manager.get_cmp_total(username)
            total_current_value=round(total_current_value[0][0],2)
            return render_template("app_pages/transaction_input.html",rows=rows,total_investment=total_investment,
                           total_current_value=total_current_value)
        if sell:
            sname = request.form["stock-name"]
            sqty = request.form["stock-quantity"]
            sdate = request.form["start-date"]
            negativeqty=int('-'+sqty)           #negative of the number
            todayvalue = cp_calc(sdate, sqty, sname, flag=1)  # shares current price
            currenttotal = cp_calc(sdate, sqty, sname, flag=2)  # total amount now wrt current price
            sell_option(username,sname,negativeqty,sdate,todayvalue,currenttotal)
            prow=portfolio_manager.get_portfolio_user(username)
            if prow == []:
                return redirect(url_for("transaction_route.transaction_input", username=username))
            else:
                entrycount = 0
                # i[0]=username prow[i][1]=stockname i[2]=qty i[3]=todayvalue i[4]=buyprice i[5]=cmp i[6]=vcmp i[7]=pl
                for i in range(len(prow)):
                    if prow[i][1] == sname:
                        entrycount = 100
                        total_quantity = negativeqty + int(prow[i][2])   #subtracting the sold qty from total qty
                        costprice_port = round(prow[i][3] * total_quantity, 2)   #multiplying reduced qty with exisitng avg cp for new total investment
                        cmprice=cp_calc(sdate, sqty, sname, flag=1)
                        vcmp = round(cmprice * total_quantity, 2)  # total value of entire investment
                        pl = round(vcmp - costprice_port, 2)  #unrealized profit
                        pl_relaized=(abs(negativeqty)*cmprice)-(abs(negativeqty)*prow[i][3]) #realized profit
                        portfolio_manager.update_portfolio_user(username, sname, total_quantity, costprice_port, cmprice, vcmp, pl)
                        profitloss_manager.insert_profitloss(username,sname,sqty,sdate,cmprice,pl_relaized)
                        break
                if entrycount == 0:
                    
                    portfolio_manager.insert_portfolio_user(username, sname, sqty, buyprice, costprice, todayvalue, currenttotal, pl)
            return redirect(url_for("transaction_route.transaction_input", username=username))
            
        if transaction_history:
            return redirect(url_for("transactionhistory_route.transaction_history",username=username))
        if logout:
            return redirect(url_for("home"))
        if insights:
            print("this is insights")
            return redirect(url_for("insights_route.insights",username=username))
        return redirect(url_for("transaction_route.transaction_input", username=username))
    except:
        msg = "error in insert"


def sell_option(username, sname, negativeqty, sdate, todayvalue, currenttotal):
    db_manager = DatabaseManager('database.db')
    stock_manager = StockManager(db_manager)
    portfolio_manager = PortfolioManager(db_manager)
    stock_manager.insert_stock_user(username, sname, negativeqty, sdate, todayvalue, currenttotal)
    rows=portfolio_manager.get_portfolio_user(username)
    return render_template("app_pages/transaction_input.html",rows=rows)
    
def cp_calc(date, qty, name, flag):
    stock_name = yf.Ticker(name)
    print(type(stock_name))
    print("52weekhighhh",stock_name.info["fiftyTwoWeekHigh"])
    end_date = datetime.now().strftime('%Y-%m-%d')
    stock_name_history = stock_name.history(start=date, end=end_date)
    if flag == -1:
        returnvalue = round(stock_name_history.Close[0], 2)
        return returnvalue
    if flag == 0:
        returnvalue =round(float(qty) * stock_name_history.Close[0], 2)
        return returnvalue
    if flag == 1:
        returnvalue = round(stock_name_history.Close[-1], 2)
        return returnvalue
    else:
        returnvalue = round(float(qty) * stock_name_history.Close[-1], 2)
        return returnvalue



# transaction input to home
# transaction input to portfolio
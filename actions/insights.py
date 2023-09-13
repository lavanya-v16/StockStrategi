from flask import Flask, render_template, Blueprint,redirect,url_for,request,jsonify
from db_manager import DatabaseManager,Insights
import yfinance as yf
from datetime import datetime

insights_action=Blueprint("insights_action",__name__)

@insights_action.route("/insights/<username>",methods=["POST"])
def insights(username):
    l=[]
    o=[]
    p=[]
    q=[]
    db_manager = DatabaseManager('database.db')
    insights_manager=Insights(db_manager)
    print("hi")
    interactive=request.form.get("interactive")
    option=request.form.get("option")
    submit=request.form.get("submit-insight")
    names=insights_manager.get_fiftytwo()
    for i in names:
        l.append(i[0])
    print(l)
    for i in l:
        stock_name = yf.Ticker(i)
        a=stock_name.info["fiftyTwoWeekHigh"]
        b=stock_name.info["fiftyTwoWeekLow"]
        end_date = datetime.now().strftime('%Y-%m-%d')
        stock_name_history = stock_name.history(period="1d")
        c=round(stock_name_history.Close[-1], 2)
        o.append(a)
        p.append(b)
        q.append(c)
        irow=insights_manager.get_fiftytwo()
        if irow==[]:
            insights_manager.insert_fiftytwo(i,a,b,c)
        else:
            entrycount = 0
            for j in range(len(irow)):
                if irow[j][0] == i:
                    print(irow[j][0])
                    entrycount=100
                    insights_manager.update_fiftytwo(a,b,c)
            if entrycount==0:
                insights_manager.insert_fiftytwo(i,a,b,c)
    if interactive:
        render_template("app_pages/interactive_insights.html",sname=l,high=o, low=p, cmp=q)
    if submit:
        value= insights_manager.get_singlerow(option)
        print("value",value)
        render_template("app_pages/interactive_insights.html",sname=l,value=value)

    return redirect(url_for("insights_route.insights",username=username))
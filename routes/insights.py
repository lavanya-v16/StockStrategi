from flask import Flask, render_template, Blueprint
from db_manager import DatabaseManager,Insights
import yfinance as yf
from datetime import datetime

insights_route=Blueprint("insights_route",__name__)

@insights_route.route("/insights/<username>",methods=["GET"])
def insights(username):
    db_manager = DatabaseManager('database.db')
    insights_manager=Insights(db_manager)
    l=[]
    k=[]
    m=[]
    n=[]
    o=[]
    p=[]
    q=[]
    r=[]
    m1=[]
    n1=[]
    db_manager=DatabaseManager('database.db')
    insights_manager=Insights(db_manager)
    distr=insights_manager.get_distribution(username)  # percent of different stock based on investment amt
    for sname,distribution in distr:
        l.append(sname)
        k.append(distribution)
    insights_manager=Insights(db_manager)
    distr=insights_manager.get_top(username)   # list of all stocka in descednign order of profit/loss
    for sname1,pl in distr:
        m.append(sname1)
        n.append(pl)
    m1=m[-3:]      # losers
    n1=n[-3:]
    m=m[:3]        #gainers
    n=n[:3]
    plpercent=insights_manager.pl_percent(username)   # finding profit loss percent , computations done in db manager
    print(plpercent)


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
    for i in range(len(p)):
        if ((o[i]+p[i])//2) > q[i]:
            r.append(l[i])
    
    return render_template("app_pages/insights.html",sname=l,distribution=k, top_sname=m, top_price=n, last_sname=m1, 
                           last_price=n1,pl=plpercent,high=o, low=p, cmp=q )
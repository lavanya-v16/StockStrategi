from flask import Flask, redirect,url_for,request,render_template, flash
from routes.login import login_route
from routes.create import create_route
from routes.transaction_input import transaction_route
from routes.portfolio import portfolio_route

app=Flask(__name__)
app.register_blueprint(login_route)
app.register_blueprint(create_route)
app.register_blueprint(transaction_route)
app.register_blueprint(portfolio_route)


app.config['SECRET_KEY']='random key'



@app.route("/",methods=["GET"])
def home():
    return redirect("/login")
    

if __name__=="__main__":
    app.run(debug=True)
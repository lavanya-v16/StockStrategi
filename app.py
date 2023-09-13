from flask import Flask, redirect,url_for,request,render_template, flash
from routes.login import login_route
from routes.create import create_route
from routes.transaction_input import transaction_route
from routes.transaction_history import transactionhistory_route
from routes.insights import insights_route
from actions.create import create_action
from actions.login import login_action
from actions.transaction_history import transactionhistory_action
from actions.transaction_input import transaction_action
from actions.insights import insights_action

app=Flask(__name__)
app.register_blueprint(login_route)
app.register_blueprint(create_route)
app.register_blueprint(transaction_route)
app.register_blueprint(transactionhistory_route)
app.register_blueprint(insights_route)
app.register_blueprint(create_action)
app.register_blueprint(login_action)
app.register_blueprint(transactionhistory_action)
app.register_blueprint(transaction_action)
app.register_blueprint(insights_action)



app.config['SECRET_KEY']='random key'



@app.route("/",methods=["GET"])
def home():
    return redirect("/login")
    

if __name__=="__main__":
    app.run(debug=True)
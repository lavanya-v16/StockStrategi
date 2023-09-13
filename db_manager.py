import sqlite3

class DatabaseManager:
    def __init__(self,db_name):
        self.connection=sqlite3.connect(db_name,check_same_thread=False)
        self.cursor=self.connection.cursor()

    def execute(self,query,args):
        self.cursor.execute(query,args)
        self.connection.commit()
        return self.cursor.fetchall()
    
    def execute_no_arg(self,query):
        self.cursor.execute(query)
        self.connection.commit()
        return self.cursor.fetchall()
    
    def create_table(self,table_name):
        print("hii:",table_name)
        create_table_queries={
            "Stockuser": """
                        CREATE TABLE IF NOT EXISTS Stockuser(
                        username txt ,
                        stockname TXT NOT NULL , 
                        qty INT NOT NULL, 
                        buydate TEXT NOT NULL,
                        todayvalue REAL,
                        buyprice REAL
                        );
                    """,
            "Portfoliouser":"""
                        CREATE TABLE IF NOT EXISTS Portfoliouser(
                        username txt, 
                        stockname TXT , 
                        qty INT ,
                        todayvalue REAL, 
                        buyprice REAL, 
                        CMP REAL, 
                        VALUE_CMP REAL, 
                        PROFIT_LOSS REAL
                        );
                    """,
            "Profitloss":"""
                        CREATE TABLE IF NOT EXISTS Profitloss(
                        username TXT, 
                        stockname TXT ,
                        qty INT , 
                        buydate TEXT ,
                        sellprice REAL,
                        PROFIT_LOSS REAL
                        );
                    """,
            "User1":"""
                        CREATE TABLE IF NOT EXISTS User1(
                        username TXT unique primary key,
                        password_hash text not null
                        );
                    """,
            "FiftyTwoWeek":"""
                        CREATE TABLE IF NOT EXISTS FiftyTwoWeek(
                        stockname TXT unique primary key,
                        High REAL,
                        Low REAL,
                        CMP REAL
                        );
                    """
        }

        create_query=create_table_queries.get(table_name)
        print(create_query)
        if create_query:
            self.execute_no_arg(create_query)
        else:
            raise ValueError(f"Table name'{table_name}' not found")
        
    def drop_table(self,table_name):
        drop_table_query=f"DROP TABLE IF EXISTS {table_name};"
        self.execute_no_arg(drop_table_query)


class StockManager:
    def __init__(self,db_manager):
        self.db=db_manager

    def insert_stock_user(self,username,stockname,qty,buydate,todayvalue,buyprice):
        self.db.execute("INSERT INTO Stockuser(username,stockname,qty,buydate,todayvalue,buyprice) VALUES (?,?,?,?,?,?)",(username,stockname,qty,buydate,todayvalue,buyprice))

    def get_stock_user(self,username):
        return self.db.execute("SELECT * FROM Stockuser where username=? ORDER BY rowid DESC",(username,))
    

class PortfolioManager:
    def __init__(self,db_manager):
        self.db=db_manager

    def insert_portfolio_user(self,username,stockname,qty,todayvalue,buyprice,CMP,VALUE_CMP,PROFIT_LOSS):
        self.db.execute("INSERT INTO Portfoliouser(username,stockname,qty,todayvalue,buyprice,CMP,VALUE_CMP,PROFIT_LOSS) VALUES(?,?,?,?,?,?,?,?)",(username,stockname,qty,todayvalue,buyprice,CMP,VALUE_CMP,PROFIT_LOSS))

    def update_portfolio_user(self, username, stockname, qty,todayvalue, buyprice, CMP, VALUE_CMP, PROFIT_LOSS):
        self.db.execute(
            "UPDATE Portfoliouser SET qty=?, todayvalue=?, buyprice=?, CMP=?, VALUE_CMP=?, PROFIT_LOSS=? WHERE stockname=? AND username=?",
            (qty,todayvalue, buyprice, CMP, VALUE_CMP, PROFIT_LOSS, stockname, username))

    def get_portfolio_user(self, username):
        return self.db.execute("SELECT * from Portfoliouser where username=?", (username,))
    
    def get_buyprice_total(self,username):
        return self.db.execute("SELECT SUM(buyprice) from Portfoliouser where username=?",(username,))
    
    def get_cmp_total(self,username):
        return self.db.execute("SELECT SUM(VALUE_CMP) from Portfoliouser where username=?",(username,))
    
class ProfitlossManager:
    def __init__(self,db_manager):
        self.db=db_manager
    
    def insert_profitloss(self,username,sname,sqty,sdate,cmprice,pl_relaized):
        self.db.execute("INSERT INTO Profitloss(username,stockname, qty, buydate, sellprice , PROFIT_LOSS ) VALUES (?,?,?,?,?,?)",(username,sname,sqty,sdate,cmprice,pl_relaized))
    
class UserManager:
    def __init__(self,db_manager):
        self.db=db_manager

    def insert_user(self,user,password_hash):
        self.db.execute("INSERT INTO USER1 (username, password_hash) VALUES(?,?)",(user,password_hash))

    def get_user(self):
        return self.db.execute_no_arg("SELECT * FROM User1")
    
    
class LoginManager:
    def __init__(self,db_manager):
        self.db=db_manager

    def get_user(self,username):
        return self.db.execute("SELECT * FROM User1 where username=?",(username,))
    
    def get_password(self,username):
        return self.db.execute("SELECT password_hash from USER1 where username=?",(username,))
    
class Insights:
    def __init__(self,db_manager):
        self.db=db_manager
    def get_distribution(self,username):
        return self.db.execute("SELECT STOCKNAME, BUYPRICE from Portfoliouser where username=? ORDER BY BUYPRICE DESC",(username,))
    def get_top(self,username):
        return self.db.execute("SELECT STOCKNAME, PROFIT_LOSS from Portfoliouser where username=? ORDER BY PROFIT_LOSS DESC",(username,))
    def pl_percent(self,username):
        a=self.db.execute("SELECT * FROM Portfoliouser where username=?",(username,))
        l=[]
        c=self.db.execute("SELECT SUM(buyprice) from Portfoliouser where username=?",(username,))
        for i in range(len(a)):
            b=((a[i][7]/c[0][0])*100)
            l.append(b)
        return l
    def insert_fiftytwo(self,stockname,high,low,cmp):
        self.db.execute("INSERT INTO FIFTYTWOWEEK VALUES(?,?,?,?)",(stockname,high,low,cmp))
    def get_fiftytwo(self):
        return self.db.execute_no_arg("SELECT * FROM FIFTYTWOWEEK")
    def update_fiftytwo(self,high,low,cmp):
        self.db.execute("UPDATE FIFTYTWOWEEK SET HIGH=?, LOW=?, CMP=?",(high,low,cmp))
    
    def get_singlerow(self,stockname):
        return self.db.execute("SELECT * FROM FIFTYTWOWEEK WHERE STOCKNAME=?",(stockname,))
    
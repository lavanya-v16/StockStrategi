# import sqlite3

# conn=sqlite3.connect('database.db')
# print("Connected to database succesfully")
        
# conn.execute('CREATE TABLE Stockuser(username txt ,stockname TXT NOT NULL , qty INT NOT NULL, buydate TEXT NOT NULL,todayvalue REAL, buyprice REAL)')
# print("db created succesfully")
        
# conn.close()

# ########################################################################

# import sqlite3

# conn=sqlite3.connect('database.db')
# print("Connected to database succesfully")
# conn.execute('CREATE TABLE Portfoliouser(username txt, stockname TXT , qty INT ,todayvalue REAL, buyprice REAL, CMP REAL, VALUE_CMP REAL, PROFIT_LOSS REAL )')
# print("db created succesfully")
        
# conn.close()

# #####################################################################

# import sqlite3

# conn=sqlite3.connect('database.db')
# print("Connected to database succesfully")
        
# conn.execute('CREATE TABLE User1 (username TXT unique primary key, password_hash text not null )')
# print("db created succesfully")
        
# conn.close()

##########################################################################

import sqlite3

conn=sqlite3.connect('database.db')
print("Connected to database succesfully")
        
conn.execute('CREATE TABLE Profitloss (username TXT, stockname TXT , qty INT , buydate TEXT ,sellprice REAL, PROFIT_LOSS REAL )')
print("db created succesfully")
        
conn.close()
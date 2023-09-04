import sqlite3

conn=sqlite3.connect('database.db')
print("Connected to database succesfully")
conn.execute('DROP TABLE Stockuser')

print("db dropped succesfully")
        
conn.close()

#####################################################################

import sqlite3

conn=sqlite3.connect('database.db')
print("Connected to database succesfully")
conn.execute('DROP TABLE Portfoliouser')

print("db dropped succesfully")
        
conn.close()

##################################################################

import sqlite3

conn=sqlite3.connect('database.db')
print("Connected to database succesfully")
conn.execute('DROP TABLE User1')

print("db dropped succesfully")
        
conn.close()

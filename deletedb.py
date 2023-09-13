# import sqlite3

# conn=sqlite3.connect('database.db')
# print("Connected to database succesfully")
# conn.execute('DROP TABLE Stockuser')

# print("db dropped succesfully")
        
# conn.close()

#####################################################################

# import sqlite3

# conn=sqlite3.connect('database.db')
# print("Connected to database succesfully")
# conn.execute('DROP TABLE Portfoliouser')

# print("db dropped succesfully")
        
# conn.close()

##################################################################

# import sqlite3

# conn=sqlite3.connect('database.db')
# print("Connected to database succesfully")
# conn.execute('DROP TABLE User1')

# print("db dropped succesfully")
        
# conn.close()

##################################################################


# import sqlite3

# conn=sqlite3.connect('database.db')
# print("Connected to database succesfully")
# conn.execute('DROP TABLE Profitloss')

# print("db dropped succesfully")
        
# conn.close()

from db_manager import DatabaseManager

db_manager=DatabaseManager('database.db')
# db_manager.drop_table('Stockuser')
# db_manager.drop_table('Portfoliouser')
# db_manager.drop_table('Profitloss')
# db_manager.drop_table('User1')

db_manager.drop_table('FiftyTwoWeek')
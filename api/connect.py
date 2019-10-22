import sqlite3

#Database connection
def connection(db):
    con = None
    try:
        con = sqlite3.connect(db)
    except con.Error as e:
        print(e)
    
    return con

#close connection
def close_con(con):
    con.close()
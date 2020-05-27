import MySQLdb

def conn_f():
    con = MySQLdb.connect(
        user="root",
        password="1031",
        host="localhost",
        db="todo_app",
        charset="utf8"
    )
    return con

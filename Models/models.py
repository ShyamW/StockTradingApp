import sqlite3

def insertUser(username,password, email):
    db = sqlite3.connect("Stocks.db")
    cursor = db.cursor()
    cursor.execute("INSERT INTO userinfo(username,password,email) VALUES (?,?,?)", (username, password, email))
    db.commit()
    db.close()

def checkIfUserExists(username):
    db = sqlite3.connect("Stocks.db")
    cursor = db.cursor()
    cursor.execute("SELECT * From userinfo WHERE username = ?", (username))
    user = cursor.fetchall()
    db.close()
    return user.count() > 0

def getAllUsers():
    #todo
    return ""


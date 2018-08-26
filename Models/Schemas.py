import sqlite3

def initializeDatabse():
    with sqlite3.connect("Stocks.db") as database:
        cursor = database.cursor()

    cursor.execute('''
    CREATE TABLE IF NOT EXISTS userinfo(
    username VARCHAR(50) PRIMARY KEY, 
    password VARCHAR(50) NOT NULL,
    email VARCHAR(50) NOT NULL);
    ''')

    cursor.execute('''
    INSERT INTO userinfo(username,password,email)
    VALUES("ilike100","12345","buckeye@osu.edu")
    ''')
    database.commit()

    cursor.execute("SELECT * FROM userinfo")
    print(cursor.fetchall())




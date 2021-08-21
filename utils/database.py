import mysql.connector
from mysql.connector import errorcode

def createEmailTable(cnx):
    cursor = cnx.cursor(dictionary = True)
    query1 = '''CREATE TABLE IF NOT EXISTS emails (
                email varchar(250) NOT NULL,
                password varchar(250) NOT NULL,
                proxy varchar(250) NOT NULL,
                available int NOT NULL
            )'''
    try:
        cursor.execute(query1)
    except:
        print("Table exists")

def getConnect():
    config = {
        'user': 'root',
        'password': '',
        'host': '127.0.0.1',
        'port': 3306,
        'database': 'coinmarketcap',
        'raise_on_warnings': True
    }

    try:
        cnx = mysql.connector.connect(**config)
        return cnx
    except mysql.connector.Error as err:
        if err.errno == errorcode.ER_ACCESS_DENIED_ERROR:
            print('Something is wrong with your user name or password')
        elif err.errno == errorcode.ER_BAD_DB_ERROR:
            print('Database does not exist')
        else:
            print(err)

def registerEmail(cnx, email, password, proxy, value):
    cursor = cnx.cursor(dictionary = True)
    query = f"INSERT INTO emails(email, password, proxy, available) VALUES ('{email}', '{password}', '{proxy}', {value})"
    cursor.execute(query)
    
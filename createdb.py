import mysql.connector
from mysql.connector import errorcode

if __name__ == "__main__":
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
    except mysql.connector.Error as err:
        if err.errno == errorcode.ER_ACCESS_DENIED_ERROR:
            print('Something is wrong with your user name or password')
        elif err.errno == errorcode.ER_BAD_DB_ERROR:
            print('Database does not exist')
        else:
            print(err)
    else:
        cursor = cnx.cursor(dictionary = True)
        query1 = '''CREATE TABLE IF NOT EXISTS emails (
                    id int PRIMARY KEY AUTO_INCREMENT,
                    email varchar(250) NOT NULL,
                    password varchar(250) NOT NULL,
                    proxy varchar(250) NOT NULL,
                    available int NOT NULL
                )'''
        # query2 = '''CREATE TABLE IF NOT EXISTS pages (
        #             id int PRIMARY KEY AUTO_INCREMENT,
        #             name varchar(250) NOT NULL,
        #             url varchar(250) NOT NULL,
        #             type varchar(250) NOT NULL
        #         )'''

        # query3 = '''CREATE TABLE IF NOT EXISTS keywords (
        #             id int PRIMARY KEY AUTO_INCREMENT,
        #             keyword varchar(250) NOT NULL,
        #             type varchar(250) NOT NULL
        #         )'''
        
        # query4 = '''CREATE TABLE IF NOT EXISTS coins (
        #             id int PRIMARY KEY AUTO_INCREMENT,
        #             name varchar(250) NOT NULL,
        #             url varchar(250) NOT NULL
        #         )'''

        # query5 = '''CREATE TABLE IF NOT EXISTS buttons (
        #             id int PRIMARY KEY AUTO_INCREMENT,
        #             name varchar(250) NOT NULL,
        #             xpath varchar(250) NOT NULL
        #         )'''

        try:
            cursor.execute(query1)
            # cursor.execute(query2)
            # cursor.execute(query3)
            # cursor.execute(query4)
            # cursor.execute(query5)
        except:
            print("Table exists")
        finally:
            with open('database/emails.txt', 'r') as f:
                emails = f.read()
            emails = emails.split('\n')

            insert_stmt = (
                'INSERT INTO emails(email, password, proxy, available)'
                'VALUES (%s, %s, %s, %d)'
            )
            data = (email, password, proxy, 0)
            cursor.execute(insert_stmt, data)
            cnx.commit()
            cnx.close()
import logging
import threading
import time
import sys
import os

from selenimuwire import webdriver
from twocaptcha import TwoCaptcha

import mysql.connector
from mysql.connector import errorcode

from utils.genRandom import getRandomNumber
from utils.signup import signup
from utils.verify import verify

def register(email, password, proxy_username, proxy_pwd, ip_address, port):
    proxy_options = {
        'proxy': {
            'https': 'https://' + proxy_username + ':' + proxy_pwd + '@' + ip_address + ':' + port,
        }
    }
    chrome_options = webdriver.ChromeOptions()
    chrome_options.add_argument('--incognito')

    driver = webdriver.Chrome('./chromedriver', seleniumwire_options = proxy_options, chrome_options = chrome_options)
    driver.maximize_window()

    if not signup(driver, email, password):
        return

    verify(driver, email, password)

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
        try:
            cursor.execute(query1)
        except:
            print("Table exists")
        finally:
            insert_stmt = (
                'INSERT INTO emails(email, password, proxy, available)'
                'VALUES (%s, %s, %s, %d)'
            )
            data = (email, password, proxy, 1)
            cursor.execute(insert_stmt, data)
            cnx.commit()
            cnx.close()
    driver.close()

if __name__ == "__main__":
    threads = list()
    for index in range(2):
        logging.info("Main   : create and start thread %d.", index)
        x = threading.Thread(target=register, args=(email, password, proxy))
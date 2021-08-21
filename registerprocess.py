import logging
import threading
import time
import sys
import os

from seleniumwire import webdriver
from twocaptcha import TwoCaptcha

import mysql.connector
from mysql.connector import errorcode

from utils.genRandom import getRandomNumber
from utils.signup import signup
from utils.verify import verify
from utils.readAssets import readEmails, readProxies
from utils.database import getConnect, createEmailTable, registerEmail


def register(email, password, proxy):
    proxy_options = {
        'proxy': {
            'https': 'https://' + proxy,
            'http': 'http://' + proxy,
            'no_proxy': 'localhost,127.0.0.1'
        }
    }
    chrome_options = webdriver.ChromeOptions()
    chrome_options.add_argument('--incognito')

    driver = webdriver.Chrome('./chromedriver', seleniumwire_options = proxy_options, chrome_options = chrome_options)
    driver.maximize_window()

    cnx = getConnect()
    createEmailTable(cnx)

    if not signup(driver, email, password):
        registerEmail(cnx, email, password, proxy, 0)
        cnx.commit()
        cnx.close()
        return

    code = verify(driver, email, password)
    if code != 1:
        registerEmail(cnx, email, password, proxy, code)
        cnx.commit()
        cnx.close()
        return

    registerEmail(cnx, email, password, proxy, 1)
    cnx.commit()
    cnx.close()
    driver.close()

if __name__ == "__main__":
    threads = list()
    emails, passwords = readEmails()
    proxies = readProxies()

    for index in range(2):
        x = threading.Thread(target=register, args=(emails[index+6], passwords[index+6], proxies[index+6]))
        threads.append(x)
        x.start()
        time.sleep(getRandomNumber(1, 10))

    for index, thread in enumerate(threads):
        logging.info("Main    : before joining thread %d.", index)
        thread.join()
        logging.info("Main    : thread %d done", index)
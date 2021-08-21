import logging
import threading
import time
import sys
import os

from seleniumwire import webdriver
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

from twocaptcha import TwoCaptcha

import mysql.connector
from mysql.connector import errorcode

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

    driver = webdriver.Chrome('../chromedriver', seleniumwire_options = proxy_options, chrome_options = chrome_options)
    driver.maximize_window()

    passed = False

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
                    email varchar(250) NOT NULL,
                    password varchar(250) NOT NULL,
                    proxy varchar(250) NOT NULL,
                    available int NOT NULL
                )'''
        try:
            cursor.execute(query1)
        except:
            print("Table exists")

    ##############################################

    driver.get('https://coinmarketcap.com')
    time.sleep(2)

    driver.find_element_by_class_name('cEEOTh').click()
    time.sleep(2)

    driver.find_element_by_css_selector('input[type="email"]').send_keys(email)
    driver.find_element_by_css_selector('input[type="password"]').send_keys(password)
    print('account info entered')

    sys.path.append(os.path.dirname(os.path.dirname(os.path.realpath(__file__))))
    api_key = os.getenv('APIKEY_2CAPTCHA', 'd655075cd2cb09d2520bad77635180af')

    solver = TwoCaptcha(api_key)

    print('>>>>>>>: start getting a token for a while, please wait ...')
    while True:
        try:
            result = solver.recaptcha(
                sitekey = '6LfSEDIbAAAAAEyHtxj2xtEA8It6gSi6s4_PNxwI',
                url = 'https://coinmarketcap.com',
                invisible = 1)

        except Exception as e:
            query = f"INSERT INTO emails(email, password, proxy, available) VALUES ('{email}', '{password}', '{proxy}', 0)"
            cursor.execute(query)
            cnx.commit()
            cnx.close()

        else:
            form_token = result['code']
            break
    print('>>>>>>>: got a token!')
    print(form_token)

    driver.find_element_by_class_name('ffwHVz').click()
    time.sleep(2)

    try:
        driver.find_element_by_id('vsELS')
    except:
        passed = False
    else:
        passed = True
    
    time.sleep(2)

    if not passed:
        # put the token in the textarea
        write_token_js = f'document.getElementById("g-recaptcha-response").innerHTML = "{form_token}";'
        driver.execute_script(write_token_js)        

        time.sleep(2)

        try:
            # excute callback function
            callback_js = f'___grecaptcha_cfg.clients[0].R.R.callback("{form_token}");'
            driver.execute_script(callback_js)
        except:
            print('Recaptcha is not shown!')
            query = f"INSERT INTO emails(email, password, proxy, available) VALUES ('{email}', '{password}', '{proxy}', 0)"
            cursor.execute(query)
            cnx.commit()
            cnx.close()
        finally:
            time.sleep(3)

    ##############################################

    driver.get('https://outlook.office365.com/mail/inbox')
    time.sleep(10)

    try:
        element = WebDriverWait(driver, 120).until
        (
            EC.url_contains('login.microsoftonline.com/common/oauth2/authorize')
        )
    finally:
        driver.find_element_by_css_selector('input[type="email"]').send_keys(email)
        time.sleep(1)
        driver.find_element_by_css_selector('input[type="submit"]').click()
        time.sleep(10)
        driver.find_element_by_css_selector('input[type="password"]').send_keys(password) #passwordBrowserPrefill
        time.sleep(1)
        driver.find_element_by_css_selector('input[type="submit"]').click()
        print('Login Entered')
        time.sleep(5)
        driver.find_element_by_xpath('//*[@id="idBtn_Back"]').click()
        time.sleep(30)
        print('logged in')
        try:
            driver.find_element_by_class_name('ms-Dialog-button--close').click()  #press escape to remove popup
        except:
            pass
        time.sleep(7)
        print('removed popup')
        driver.find_element_by_xpath('//span[contains(text(),"Verify your CoinMarketCap account")]').click()
        time.sleep(5)
        parent_handle = driver.window_handles[0]
        time.sleep(1)
        driver.find_element_by_xpath('//a[normalize-space()="Click here to verify account"]').click()
        time.sleep(8)
        child_handle = [x for x in driver.window_handles if x != parent_handle][0]
        driver.switch_to.window(child_handle)
        time.sleep(5)
        print('verified account')

    print('------------------------123---------------------------')
    driver.close()
    print('------------------------456---------------------------')

    query = f"INSERT INTO emails(email, password, proxy, available) VALUES ('{email}', '{password}', '{proxy}', 1)"
    cursor.execute(query)
    cnx.commit()
    cnx.close()

if __name__ == "__main__":
    register('ElijahMalachi13268@outlook.com', 'SQU07oad', 'ylfrixuf:8ajqezchxeqh@185.212.160.131:7146')
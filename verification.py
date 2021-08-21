import logging
import threading
import time
import sys
import os

from seleniumwire import webdriver
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

def verification(email, password, proxy):

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

if __name__ == "__main__":
    emails, passwords = readEmails()
    proxies = readProxies()
    count = 0
    while True:
        threads = list()
        for index in range(5):
            if count > len(emails) - 1:
                break
            x = threading.Thread(target=verification, args=(emails[count], passwords[count], proxies[count]))
            threads.append(x)
            x.start()
            count+=1

        for index, thread in enumerate(threads):
            logging.info("Main    : before joining thread %d.", index)
            thread.join()
            logging.info("Main    : thread %d done", index)
    register('ElijahMalachi13268@outlook.com', 'SQU07oad', 'ylfrixuf:8ajqezchxeqh@185.212.160.131:7146')
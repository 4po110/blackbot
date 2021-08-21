import logging
import time
import sys
import os

from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

def verify(driver, email, password):

    driver.get('https://outlook.office365.com/mail/inbox')
    time.sleep(10)

    try:
        element = WebDriverWait(driver, 120).until
        (
            EC.url_contains('login.microsoftonline.com/common/oauth2/authorize')
        )
        driver.find_element_by_css_selector('input[type="email"]').send_keys(email)
        time.sleep(1)
        driver.find_element_by_css_selector('input[type="submit"]').click()
        time.sleep(10)
        driver.find_element_by_css_selector('input[type="password"]').send_keys(password) #passwordBrowserPrefill
        time.sleep(1)
        driver.find_element_by_css_selector('input[type="submit"]').click()
        print('Login Entered')
        time.sleep(10)
        try:
            driver.find_element_by_xpath('//*[@id="idBtn_Back"]').click()
        except:
            print('email verification needed')
            return -1
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
        time.sleep(10)
        child_handle = [x for x in driver.window_handles if x != parent_handle][0]
        driver.switch_to.window(child_handle)
        time.sleep(5)
        print('verified account')
    except:
        return 0
    return 1
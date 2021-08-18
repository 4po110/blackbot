import logging
import time
import sys
import os

from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

def verify(driver, email, password):

    driver.get('https://outlook.office365.com/mail/inbox')

    try:
        element = WebDriverWait(driver, 120).until
        (
            EC.url_contains('login.microsoftonline.com/common/oauth2/authorize')
        )
    finally:
        driver.find_element_by_id('i0116').send_keys(email)
        time.sleep(2)
        driver.find_element_by_xpath('//*[@id="idSIButton9"]').click()
        time.sleep(10)
        driver.find_element_by_id('i0118').send_keys(password) #passwordBrowserPrefill
        time.sleep(2)
        driver.find_element_by_xpath('//*[@id="idSIButton9"]').click()
        print('Login Entered')

        time.sleep(10)
        driver.find_element_by_xpath('//*[@id="idBtn_Back"]').click()
        time.sleep(7)
        driver.execute_script('window.stop();')  #press escape to remove popup
        time.sleep(7)
        driver.find_element_by_xpath('//span[contains(text(),"Verify your CoinMarketCap account")]').click()
        time.sleep(10)
        parent_handle = driver.window_handles[0]
        time.sleep(8)
        driver.find_element_by_xpath('//a[normalize-space()="Click here to verify account"]').click()
        time.sleep(8)
        child_handle = [x for x in driver.window_handles if x != parent_handle][0]
        driver.switch_to.window(child_handle)
        time.sleep(5)

        driver.get('https://httpbin.org/ip')
        time.sleep(5)
        driver.close()
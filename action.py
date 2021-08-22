import time
from selenium import webdriver

from utils import getRandomNumber, getRandomBool, getRandomLetter, generateFakeActivities, generateMainActivities

def action():

    proxy_options = {
        'proxy': {
            'https': 'https://' + proxy,
            'http': 'http://' + proxy,
            'no_proxy': 'localhost,127.0.0.1'
        }
    }
    chrome_options = webdriver.ChromeOptions()

    driver = webdriver.Chrome('./chromedriver', seleniumwire_options = proxy_options, chrome_options = chrome_options)
    driver.maximize_window()

    cnx = getConnect()

    fNumber1 = getRandomNumber(0, 10) # the number of fake activity before main activities
    mNumber = getRandomNumber(5, 10) # the number of main activity that affects trending ranking
    fNumber2 = getRandomNumber(0, 10) # the number of fake activity after main activities

    fActivities1 = generateFakeActivities(fNumber1) # the order of fake activities before main
    # mActivities = generateMainActivities(mNumber) # the order of main activities
    # fActivities2 = generateFakeActivities(fNumber2) # the order of fake activities after main

    Activities = fActivities1 # + mActivities + fActivities2

    for type, act, delay in Activities:
        if type == 'page':
            driver.get(act)
        if type == 'click':
            driver.find_element_by_class_name(act).click()
        if type == 'search':
            if getRandomBool() == 1: # enable wrong character
                for i in range(len(act)):
                    driver.find_element_by_class_name('').send_keys(act[:i+1])
                    time.sleep(getRandomNumber(8, 50)/100)
                    driver.find_element_by_class_name('').send_keys(act[:i+1] + getRandomLetter())
                    time.sleep(getRandomNumber(8, 50)/100)
                    driver.find_element_by_class_name('').send_keys(act[:i+1])
                    time.sleep(getRandomNumber(8, 50)/100)
            else: # disable wrong character
                for i in range(len(act)):
                    driver.find_element_by_class_name('').send_keys(act[:i+1])
                    time.sleep(getRandomNumber(8, 50)/100)
        time.sleep(delay)
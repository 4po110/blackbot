import time
from seleniumwire import webdriver

from utils.login import login
from utils.genRandom import getRandomNumber, getRandomBool, getRandomLetter, generateFakeActivities, generateMainActivities

def action(token, email, password, proxy, no_proxy=False):

    proxy_options = {
        'proxy': {
            'https': 'https://' + proxy,
            'http': 'http://' + proxy,
            'no_proxy': 'localhost,127.0.0.1'
        }
    }
    chrome_options = webdriver.ChromeOptions()
    if not no_proxy:
        driver = webdriver.Chrome('./chromedriver', seleniumwire_options = proxy_options, chrome_options = chrome_options)
    else:
        driver = webdriver.Chrome('./chromedriver', chrome_options = chrome_options)
    driver.maximize_window()

    islogged = login(driver, email, password)

    fNumber1 = getRandomNumber(0, 10) # the number of fake activity before main activities
    mNumber = getRandomNumber(5, 10) # the number of main activity that affects trending ranking
    fNumber2 = getRandomNumber(0, 10) # the number of fake activity after main activities

    fActivities1 = generateFakeActivities(fNumber1, islogged) # the order of fake activities before main
    mActivities = generateMainActivities(token, mNumber, islogged) # the order of main activities
    fActivities2 = generateFakeActivities(fNumber2, islogged) # the order of fake activities after main

    Activities = fActivities1 + mActivities + fActivities2

    for type, act, delay in Activities:
        print((type, act, delay))
        if type == 'page':
            driver.get(act)
        if type == 'click':
            
            action = webdriver.ActionChains(driver)
            tag, attr, value = act.split(',')

            if not value in ['+2%', 'bgsJxO']:
                driver.execute_script("window.scrollTo(0, Math.round(document.body.scrollHeight/2));")
                time.sleep(3)
                driver.execute_script("window.scrollTo(0, Math.round(document.body.scrollHeight));")
                time.sleep(3)

            if attr == 'class':
                element = driver.find_element_by_class_name(value)
                action.move_to_element(element).click().perform()
            elif attr == 'text':
                element = driver.find_element_by_xpath(f'//{tag}[contains(text(),"{value}")]')
                action.move_to_element(element).click().perform()
            else:
                element = driver.find_element_by_css_selector(f'{tag}[{attr}="{value}"]')
                action.move_to_element(element).click().perform()
        if type == 'search':
            for i in range(len(act)):
                driver.find_element_by_class_name('bzyaeu-3').send_keys(act[i])
                time.sleep(getRandomNumber(8, 50)/100)
        time.sleep(delay)

if __name__ == "__main__":
    action('poocoin', 'qcryptobase@gmail.com', 'tiger1019', '0', True)
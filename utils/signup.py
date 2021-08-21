import logging
import time
import sys
import os

from twocaptcha import TwoCaptcha

from utils.genRandom import getRandomNumber


def signup(driver, email, password):

    driver.get('https://coinmarketcap.com')
    time.sleep(getRandomNumber(2, 6))

    driver.find_element_by_class_name('cEEOTh').click()
    time.sleep(getRandomNumber(2, 6))

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
            return False
        else:
            form_token = result['code']
            break
    print('>>>>>>>: got a token!')

    driver.find_element_by_class_name('ffwHVz').click()
    time.sleep(getRandomNumber(2, 6))

    passed = False

    try:
        driver.find_element_by_xpath('//div[contains(text(), "ve sent you an activation email")]')
    except:
        passed = False
    else:
        return True
    
    if not passed:
        # put the token in the textarea
        write_token_js = f'document.getElementById("g-recaptcha-response").innerHTML = "{form_token}";'
        driver.execute_script(write_token_js)        

        time.sleep(getRandomNumber(2, 4))

        try:
            # excute callback function
            callback_js = f'___grecaptcha_cfg.clients[0].R.R.callback("{form_token}");'
            driver.execute_script(callback_js)
            time.sleep(3)
        except:
            print('Recaptcha is not shown!')
            return False
        else:
            try:
                driver.find_element_by_xpath('//div[contains(text(), "ve sent you an activation email")]')
            except:
                return False
            return True
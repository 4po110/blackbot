# @author: Kapil
# @date: Aug 5, 2021

from selenium import webdriver
import time
import sys
import os
from twocaptcha import TwoCaptcha

email_address = 'GabrielMiguel9083@outlook.com'
password = 'OLT46ppu'

chrome_options = webdriver.ChromeOptions()
chrome_options.add_argument('--incognito')

driver = webdriver.Chrome('./chromedriver', chrome_options = chrome_options)
driver.maximize_window()
driver.get('https://coinmarketcap.com')

# now wait let load the comments
time.sleep(5)

driver.find_element_by_xpath('//button[contains(text(), "Log In")]').click()

time.sleep(5)

# put account info
driver.find_element_by_xpath('//input[@type="email"]').send_keys(email_address)

driver.find_element_by_xpath('//input[@type="password"]').send_keys(password)

# get a token from 2captcha
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
    sys.exit(1)

  else:
    form_token = result['code']
    break
print('>>>>>>>: got a token!')
print(form_token)

# click login button
driver.find_element_by_class_name('ffwHVz').click()
print('asdfasdf')
time.sleep(3)

# put the token in the textarea
write_token_js = f'document.getElementById("g-recaptcha-response").innerHTML = "{form_token}";'
driver.execute_script(write_token_js)
time.sleep(3)

try:
  # excute callback function
  callback_js = f'___grecaptcha_cfg.clients[0].R.R.callback("{form_token}");'
  driver.execute_script(callback_js)
  time.sleep(3)
except:
  print('Recaptcha is not shown!')
finally:
	time.sleep(200)
	driver.close()
# @author: Kapil
# @date: Aug 5, 2021

email_address = 'yzhong99113@gmail.com'
password = 'lucky123!@#'
data_sitekey = '6LfSEDIbAAAAAEyHtxj2xtEA8It6gSi6s4_PNxwI'

from selenium import webdriver
import time
import sys
import os
from twocaptcha import TwoCaptcha

driver = webdriver.Chrome('./chromedriver')
driver.get('https://coinmarketcap.com')

# now wait let load the comments
time.sleep(5)

login_btn_elem = driver.find_element_by_xpath('//*[@class="main-content"]/div[1]/div[1]/div/div[2]/button[1]')
login_btn_elem.click()

time.sleep(5)

# put account info
email_input = driver.find_element_by_xpath('//input[@type="email"]')
email_input.send_keys(email_address)

password_input = driver.find_element_by_xpath('//input[@type="password"]')
password_input.send_keys(password)

# get a token from 2captcha
sys.path.append(os.path.dirname(os.path.dirname(os.path.realpath(__file__))))
api_key = os.getenv('APIKEY_2CAPTCHA', '6a875602020398f4a81d901d1527614c')

solver = TwoCaptcha(api_key)

print('>>>>>>>: start getting a token for a while, please wait ...')
while True:
  try:
    result = solver.recaptcha(
      sitekey = data_sitekey,
      url = 'https://coinmarketcap.com',
      invisible = 1)

  except Exception as e:
    sys.exit(e)

  else:
    form_token = result['code']
    break
print('>>>>>>>: got a token!')
print(form_token)

# click login button
login_confirm_btn = driver.find_element_by_xpath('//div[contains(@class, "modalWrpper")]/div/div[2]/div[6]/button')
login_confirm_btn.click()
time.sleep(3)

# put the token in the textarea
write_token_js = f'document.getElementById("g-recaptcha-response").innerHTML = "{form_token}";'
driver.execute_script(write_token_js)
time.sleep(3)

try:
  # excute callback function
  callback_js = f'___grecaptcha_cfg.clients[0].S.S.callback("{form_token}");'
  driver.execute_script(callback_js)
except:
  print('Recaptcha is not shown!')
finally:
	time.sleep(200)
	driver.close()
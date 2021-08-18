# @updated by: Kapil
# @date: Aug 11, 2021

email_address = 'WilliamCamden14904@outlook.com'
password = 'ONH17rqk'
data_sitekey = '6LfSEDIbAAAAAEyHtxj2xtEA8It6gSi6s4_PNxwI'

from seleniumwire import webdriver
import time
import sys
import os
from twocaptcha import TwoCaptcha

# replace 'user:pass@ip:port' with your information
proxy_options = {
	'proxy': {
		'http': 'http://ylfrixuf:8ajqezchxeqh@85.209.130.24:7565',
		'https': 'https://ylfrixuf:8ajqezchxeqh@85.209.130.24:7565',
		'no_proxy': 'localhost,127.0.0.1'
	}
}

# replace 'your_absolute_path' with your chrome binary's aboslute path
chrome_options = webdriver.ChromeOptions()
chrome_options.add_argument('--incognito')

driver = webdriver.Chrome('./chromedriver', seleniumwire_options = proxy_options, chrome_options = chrome_options)
driver.maximize_window()
# driver.get('https://httpbin.org/ip')
driver.get('https://coinmarketcap.com')

# now wait let load the comments
time.sleep(5)

# click "Sign Up" button
driver.find_element_by_class_name('cEEOTh').click()
time.sleep(5)

# put account info
driver.find_element_by_css_selector('input[type="email"]').send_keys(email_address)
driver.find_element_by_css_selector('input[type="password"]').send_keys(password)
print('account info entered')

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

# click "Create An Account" button
driver.find_element_by_class_name('ffwHVz').click()
time.sleep(3)

# put the token in the textarea
write_token_js = f'document.getElementById("g-recaptcha-response").innerHTML = "{form_token}";'
driver.execute_script(write_token_js)
time.sleep(3)

try:
	# excute callback function
	callback_js = f'___grecaptcha_cfg.clients[0].o.o.callback("{form_token}");'
	driver.execute_script(callback_js)
except:
  print('Recaptcha is not shown!')
finally:
	time.sleep(200)
	driver.close()

# driver.find_element_by_class_name('x_es-button').click()
# time.sleep(20)
#close the driver
# driver.close()
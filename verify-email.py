# @updated by: Kapil
# @date: Aug 11, 2021

email_address = 'WilliamCamden14904@outlook.com'
password = 'ONH17rqk'
ip_address = '209.127.191.180'
port = '9279'
proxy_username = 'rbtzbfww'
proxy_pwd = 'd9w9v8lx5w5s'

from seleniumwire import webdriver
import time
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import mysql.connector
from mysql.connector import errorcode

# replace 'user:pass@ip:port' with your information
proxy_options = {
  'proxy': {
		'http': 'http://' + proxy_username + ':' + proxy_pwd + '@' + ip_address + ':' + port,
		'https': 'https://' + proxy_username + ':' + proxy_pwd + '@' + ip_address + ':' + port,
		'no_proxy': 'localhost,127.0.0.1'
	}
}

chrome_options = webdriver.ChromeOptions()
chrome_options.add_argument('--incognito')

driver = webdriver.Chrome('./chromedriver', seleniumwire_options = proxy_options, chrome_options = chrome_options)
driver.maximize_window()
driver.get('https://outlook.office365.com/mail/inbox')

try:
	element = WebDriverWait(driver, 120).until
	(
		EC.url_contains('login.microsoftonline.com/common/oauth2/authorize')
	)
finally:
	driver.find_element_by_id('i0116').send_keys(email_address)
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

	driver.switch_to.window(parent_handle)
	driver.get('https://httpbin.org/ip')
	time.sleep(5)

	# Storing information into database

	# connect to Mysql
	config = {
		'user': 'root',
		'password': 'root',
		'host': '127.0.0.1',
		'port': 8889,
		'database': 'coinmarketcap_bot',
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
		create_table_query = '''CREATE TABLE IF NOT EXISTS users (
															Email_address varchar(250) NOT NULL,
															Password varchar(250) NOT NULL,
															Ip_address varchar(250) NOT NULL,
															Port varchar(250) NOT NULL,
															Proxy_username varchar(250) NOT NULL,
															Proxy_pwd varchar(250) NOT NULL
														)'''
		try:
			cursor.execute(create_table_query)
		except:
			print('Table exist')
		finally:
			insert_stmt = (
				'INSERT INTO users(Email_address, Password, Ip_address, Port, Proxy_username, Proxy_pwd)'
				'VALUES (%s, %s, %s, %s, %s, %s)'
			)
			data = (email_address, password, ip_address, port, proxy_username, proxy_pwd)
			cursor.execute(insert_stmt, data)
			cnx.commit()
			cnx.close()

			driver.close()
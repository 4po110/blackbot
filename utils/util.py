def getUrl(type, str):
    if type == 'currency':
        return f'https://coinmarketcap.com/currencies/{str}/'

def getRanking(driver, currency):

    driver.get('https://coinmarketcap.com/trending-cryptocurrencies')
    time.sleep(3)

    for i in range(30):
        name = driver.find_element_by_xpath(f'//tbody/tr[{i+1}]/td[3]/a').get_attribute('href')
        if name == getUrl('currency', currency):
            return i + 1
    return -1
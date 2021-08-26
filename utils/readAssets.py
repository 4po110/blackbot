from utils.util import getUrl

def readEmails():
    with open('database/newemails.txt', 'r') as f:
        data = f.read()
    data = data.split('\n')
    emails = list()
    passwords = list()

    for line in data:
        emails.append(line.split(',')[0])
        passwords.append(line.split(',')[1])
    
    return emails, passwords

def readProxies():
    with open('database/proxies.txt', 'r') as f:
        data = f.read()
    data = data.split('\n')
    proxies = list()

    for line in data:
        [ip, port, user, pwd] = line.split(':')
        proxies.append(f'{user}:{pwd}@{ip}:{port}')

    return proxies

def readFmail():
    with open('database/femails.txt', 'r') as f:
        data = f.read()
    
    data = data.split('\n')
    emails = list()
    passwords = list()
    proxies = list()

    for line in data:
        emails.append(line.split(' ')[0])
        passwords.append(line.split(' ')[1])
        proxies.append(line.split(' ')[2])
    return emails, passwords, proxies

def readExchanges():
    with open('database/exchanges.txt', 'r') as f:
        data = f.read()
    data = data.split('\n')
    exchanges = list()

    for line in data:
        exchanges.append(line)
    return exchanges

def readCurrencies():
    with open('database/currencies.txt', 'r') as f:
        data = f.read()
    data = data.split('\n')
    currencies = list()

    for line in data:
        currencies.append(getUrl('currency', line))

    return currencies

def readPages():
    with open('database/pages.txt', 'r') as f:
        data = f.read()
    data = data.split('\n')
    pages = list()

    for line in data:
        pages.append(line)

    return pages

def readMainPages(token):
    with open('database/mainpages.txt', 'r') as f:
        data = f.read()
    data = data.split('\n')
    pages = list()
    pages.append(getUrl('currency', token))

    for line in data:
        pages.append(getUrl('currency', f'{token}/{line}'))

    return pages

def readMainClicks():
    with open('database/mainclicks.txt', 'r') as f:
        data = f.read()
    data = data.split('\n')
    clicks = list()

    for line in data:
        clicks.append(line)

    return clicks

def readKeywords():
    with open('database/keywords.txt', 'r') as f:
        data = f.read()
    data = data.split('\n')
    keywords = list()

    for line in data:
        keywords.append(line)

    return keywords
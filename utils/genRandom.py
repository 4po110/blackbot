from random import randrange, choice, shuffle
import time
import string

from utils.util import getUrl
from utils.readAssets import readCurrencies, readExchanges, readPages, readMainPages, readMainClicks, readKeywords

def getRandomNumber(fr, to):
    return randrange(fr, to, 1)

def getRandomBool():
    return randrange(0, 2, 1)

def getRandomLetter():
    return choice(string.ascii_letters)

def generateFakeActivities(fn, islogged):
    pages = readPages()
    exchanges = readExchanges()
    currencies = readCurrencies()
    links = pages + currencies + exchanges
    series = list()
    for i in range(fn):
        link = links[getRandomNumber(0, len(links))]
        if link == 'https://coinmarketcap.com/watchlist/' and not islogged:
            continue
        series.append(('page', link, getRandomNumber(3, 10)))
    return series

def generateMainActivities(token, mn, islogged):
    pages = readMainPages(token)
    clicks = readMainClicks()
    keywords = readKeywords()
    series = list()
    series.append(('click', 'div,class,fmdlWD', getRandomNumber(1, 4)))
    series.append(('search', keywords[getRandomNumber(0, len(keywords))], getRandomNumber(1, 4)))
    series.append(('click', 'p,text,POOCOIN', getRandomNumber(4, 10)))

    sh = [x for x in range(len(pages))]
    ch = [x for x in range(len(clicks))]
    shuffle(sh)
    shuffle(ch)
    for i in sh:
        series.append(('page', pages[i], getRandomNumber(5, 10)))
        if i == 0:
            for j in ch:
                if clicks[j] == "button,text,Submit estimate":
                    if not islogged:
                        continue
                    series.append(('click', clicks[j], getRandomNumber(5, 10)))
                    series.append(('click', 'button,text,+2%', getRandomNumber(5, 10)))
                    series.append(('click', 'button,class,bgsJxO', getRandomNumber(5, 10)))
                else:
                    series.append(('click', clicks[j], getRandomNumber(5, 10)))
    return series

def getRandomAccount():
    with open('database/proxies.txt', 'r') as f:
        proxies = f.read()
    proxies = proxies.split('\n')
    with open('database/emails.txt', 'r') as f:
        emails = f.read()
    emails = emails.split('\n')

    return account
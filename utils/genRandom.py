from random import randrange, choice
import time
import string

def getRandomNumber(fr, to):
    return randrange(fr, to, 1)

def getRandomBool():
    return randrange(0, 2, 1)

def getRandomLetter():
    return choice(string.ascii_letters)

def generateFakeActivities(fn):
    with open('database/pages.txt', 'r') as f:
        pages = f.read()
    pages = pages.split('\n')
    series = []
    for i in range(fn):
        series.append(('page', pages[getRandomNumber(0, len(pages))], getRandomNumber(3, 7)))
    return series

def generateMainActivities(mn):
    for i in range(mn):
        pass
    return series

def getRandomAccount():
    with open('database/proxies.txt', 'r') as f:
        proxies = f.read()
    proxies = proxies.split('\n')
    with open('database/emails.txt', 'r') as f:
        emails = f.read()
    emails = emails.split('\n')

    return account
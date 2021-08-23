import logging
import threading
import time

from action import action
from utils.genRandom import getRandomNumber
from utils.readAssets import readEmails, readProxies

if __name__ == "__main__":
    emails, passwords = readEmails()
    proxies = readProxies()
    threads = list()
    count = 0
    while True:
        threads = list()
        for index in range(1):
            if count > len(proxies) - 1:
                break
            if count > len(emails) - 1:
                email = 'None'
                password = 'None'
            else:
                email = emails[count]
                password = passwords[count]
            x = threading.Thread(target=action, args=('poocoin', email, password, proxies[count]))
            threads.append(x)
            x.start()
            count+=1
            time.sleep(20)
        

        for index, thread in enumerate(threads):
            logging.info("Main    : before joining thread %d.", index)
            thread.join()
            logging.info("Main    : thread %d done", index)
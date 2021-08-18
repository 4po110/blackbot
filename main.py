import logging
import threading
import time

from action import action
from utils import getRandomNumber

if __name__ == "__main__":

    threads = list()
    for index in range(2):
        logging.info("Main    : create and start thread %d.", index)
        x = threading.Thread(target=action)
        threads.append(x)
        x.start()
        time.sleep(getRandomNumber(1, 10))

    for index, thread in enumerate(threads):
        logging.info("Main    : before joining thread %d.", index)
        thread.join()
        logging.info("Main    : thread %d done", index)
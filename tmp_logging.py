#### https://blog.csdn.net/bigcarp/article/details/123122336

import logging
import sys
import os
import time
def newLoger(name):
    loger = logging.getLogger(name)
    loger.setLevel(logging.INFO)
    logging_format = logging.Formatter("[%(name)s][%(asctime)s]:%(message)s", "%H:%M:%S")
    handler = logging.StreamHandler(sys.stdout)
    handler.setFormatter(logging_format)
    loger.addHandler(handler)
    return loger

# rootLoger = logging.getLogger()
# print("rootLoger = ", rootLoger)
# print(f"rootLoger 的 handler 数量：{len(rootLoger.handlers)}")

# tom = newLoger("")
# print(f"root 的 handler 数量：{len(rootLoger.handlers)}")

# tom = newLoger("tom")
# print(f"root 的 handler 数量：{len(rootLoger.handlers)}")

# jack = newLoger("")
# print(f"tom 的 handler 数量：{len(tom.handlers)}")
# print(f"root 的 handler 数量：{len(rootLoger.handlers)}")

# jack = newLoger("jack")
# print(f"tom 的 handler 数量：{len(tom.handlers)}")
# print(f"jack 的 handler 数量：{len(tom.handlers)}")
# print(f"root 的 handler 数量：{len(rootLoger.handlers)}")

class Player:
    def __init__(self, account):
        self.account: str = account
        self.log = newLoger(self.account)
    def hi(self):
        self.log.info(f"hi, {self.log.name}")
        time.sleep(1)
tom = Player("tom")
tom.hi()

jack = Player('')
jack.hi()

jack = Player('jack')
jack.hi()

mike = Player('')
mike.hi()

tom.hi()








#### https://blog.csdn.net/ithomer/article/details/16985379

# import logging
# import logging.handlers

# LOG_FILE = 'tst.log'
# handler = logging.handlers.RotatingFileHandler(LOG_FILE, maxBytes=1024*1024, backupCount=5)

# fmt = '%(asctime)s - %(filename)s:%(lineno)s - %(name)s - %(levelname)s - %(message)s'
# formatter = logging.Formatter(fmt)
# handler.setFormatter(formatter)

# logger = logging.getLogger('tst')
# logger.addHandler(handler)
# logger.setLevel(logging.DEBUG)

# logger.info('info msg')
# logger.debug('debug msg')


import logging
import logging.handlers
def main():
    logger = logging.getLogger()
    logger.setLevel(logging.DEBUG)
    handler = logging.handlers.TimedRotatingFileHandler('tst.log', 'D')
    fmt = logging.Formatter("%(asctime)s - %(pathname)s - %(filename)s - %(funcName)s - %(lineno)s - %(levelname)s - %(message)s")
    handler.setFormatter(fmt)
    logger.addHandler(handler)
    logger.debug("debug msg")
    logger.info("info msg")
    logger.warn("warn msg")
    logger.warning("warning msg")
    logger.error("error msg")
    logger.fatal("fatal msg")
    logger.critical("critical msg")
if __name__ == "__main__":
    main()

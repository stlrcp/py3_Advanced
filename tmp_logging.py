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

#!/usr/bin/python3
# -*- coding: UTF-8 -*-
# filename: log.py
# version: 4.0.2
# description: logging
# useage: from log import log

from prettytable import PrettyTable
from datetime import datetime
from pytz import timezone
from concurrent.futures import ThreadPoolExecutor
import os
import time
from sms import sms

class logging():
    def __init__(self):
        self.list = []
        self.check_dir()
        self.start()
    def check_dir(self):
        if os.path.exists('log') == False:
            os.makedirs('log')
    def start(self):
        pool = ThreadPoolExecutor(max_workers=1)
        pool.submit(self.write)
    def write(self):
        print('log正在记录')
        while True:
            #print('runnning')
            if len(self.list) == 0:
                time.sleep(5)
            else:
                filename = self.list[0][0]
                message = self.list[0][1]
                with open('log/%s.log' % filename , 'a') as f:
                    f.write(message)
                self.list.remove(self.list[0])
    def stocklist(self, text, show):
        message = '%s  %s\n' % (datetime.now(timezone('Asia/Shanghai')).strftime("%Y-%m-%d %H:%M:%S"), text)
        if show == 1:
            print(text)
        json = ('stocklist', message)
        self.list.append(json)
    def worklist(self, text, show):
        message = '%s  %s\n' % (datetime.now(timezone('Asia/Shanghai')).strftime("%Y-%m-%d %H:%M:%S"), text)
        if show == 1:
            print(text)
        json = ['worklist', message]
        self.list.append(json)
    # temp
    def suspend(self, text, show):
        message = '%s  %s\n' % (datetime.now(timezone('Asia/Shanghai')).strftime("%Y-%m-%d %H:%M:%S"), text)
        if show == 1:
            print(text)
        json = ['suspend', message]
        self.list.append(json)





def read(filename, line=10):
    table = PrettyTable(["Time", "Message"])
    with open("log/%s.log" % filename) as f:
        txt = f.readlines()
    if len(txt) < line:
        line = len(txt)
    for i in range(line):
        i = - (i + 1)
        text = txt[i].replace('\n', '')
        time = text[:19]
        message = text[21:]
        table.add_row([time, message])
    print(table)


def log(filename, show=1, sms=0):
    def decorate(func):
        def wrapper(*args, **kwargs):
            message = func(*args, **kwargs)
            if message != None:
                getattr(logging, filename)(message, show=show)
                if sms == 1:
                    sms.send(message)
        return wrapper
    return decorate


@log('stocklist')
def test():
    message = 'This is a test log message!'
    return message



logging = logging()


if __name__ != '__main__':
    #import code
    #code.interact(banner = "", local = locals())
    pass

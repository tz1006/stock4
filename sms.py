#!/usr/bin/python3
# -*- coding: UTF-8 -*- 
# filename: worklist.py
# version: 2.0.0
# description: sms.py


import nexmo
import time
import os
from datetime import datetime
from concurrent.futures import ThreadPoolExecutor


class sms():
    sleep = 2
    number = 16018666656
    key = 'd1258708'
    secret = 'No1secret'
    def __init__(self, phone):
        self.phone = phone
        self.list = []
        self._login()
        self.start()
    def _login(self):
        self._client = nexmo.Client(key=self.key, secret=self.secret)
        message = '登录短信客户端'
        self.log(message)
    def start(self):
        message = '开启发送短信'
        pool = ThreadPoolExecutor(max_workers=1)
        pool.submit(self.starter)
        self.log(message)
    def starter(self):
        self.status = True
        while self.status == True:
            if len(self.list) == 0:
                time.sleep(2)
            else:
                text = self.list[0]
                self.send_sms(text)
    def stop(self):
        self.status = False
        message = '停止发送短信'
        self.log(message)
    def send(self, text):
        self.list.append(text)
    def send_sms(self, text, debug=0):
        c = 0
        result = None
        while result != '0':
            #print(c)
            if c == 5:
                status = '失败'
                break
            result = self._client.send_message({
            'from': self.number,
            'to': self.phone,
            'text': text,
            'type': 'unicode'
            })['messages'][0]['status']
            if debug == 1:
                return result
            status = '成功'
            c += 1
        message = '发送%s：%s' % (status, text)
        self.log(message)
        self.list.remove(text)
    def log(self, message):
        text = '%s  %s\n' % (datetime.now().strftime("%Y-%m-%d %H:%M:%S"), message)
        print(message)
        if os.path.exists('log') == False:
            os.makedirs('log')
        with open('log/sms.log', 'a') as f:
            f.write(text)
    def help(self):
        print('''sms.list\nsms.send(number, text)\n/log
            ''')


sms = sms(16266039979)

if __name__ != '__main__':
    #print(__name__)
    #print('sms = sms(16266039979)')
    pass


#sms = sms(16267318573)
#sms.send('001')
#sms.send('002')
#sms.send('003')
#sms.send('004')
#sms.send('005')




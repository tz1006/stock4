#!/usr/bin/python3
# -*- coding: UTF-8 -*-
# filename: worklist.py
# version: 4.0.0
# description: worklist


from datetime import datetime
from pytz import timezone
from concurrent.futures import ThreadPoolExecutor, as_completed
from tqdm import tqdm
import pandas as pd
import psycopg2
import os
import time



from log import log
from checktime import checktime
#from stocklist import sl
import tradetest


class worklist():
    max_workers = 100
    def __init__(self):
        self.list = []
        self.__li = []
        self.wave_list = []
        self.stock = sl.stock[:]
        self.df = []
    @log('worklist')
    def start(self, min_wave=7, max_wave=10.5):
        message = '开始扫描'
        self.status = True
        pool = ThreadPoolExecutor(max_workers=1)
        pool.submit(self.wave, min_wave, max_wave)
        return message
    def stop(self):
        wl.status = False
        print(self.status)
        print('wait')
    @log('worklist')
    def wave(self, min_wave, max_wave):
        while self.status == True:
            self.wave_checker(min_wave, max_wave)
            time.sleep(0.1)
        message = '扫描停止'
        return message
    @log('worklist')
    def wave_checker(self, min_wave, max_wave):
        #self.__li.clear()
        self.df = pd.DataFrame(columns =['股票', '涨幅', '价格'])
        start_time = datetime.now()
        futures = []
        with ThreadPoolExecutor(max_workers=self.max_workers) as executor:
            for i in self.stock:
                futures.append(executor.submit(self.check_wave, i, min_wave, max_wave))
            kwargs = {'total': len(futures)}
            for f in tqdm(as_completed(futures), **kwargs):
                pass
        end_time = datetime.now()
        timedelsta = (end_time - start_time).seconds
        if self.df.empty != True:
            print(self.df)
            message = '找到%s个涨幅大于%s的股票，耗时%s秒。' % (len(self.wave_list), min_wave, timedelsta)
        else:
            message = '未找到涨幅大于%s的股票，耗时%s秒。' % (min_wave, timedelsta)
        return message
    #return self.__li
    @log('worklist', show=0)
    def check_wave(self, instance, min_wave, max_wave):
        code = instance.code
        name = instance.name
        if code not in self.wave_list:
            wave = instance.wave()[0]
            if max_wave >= wave >= min_wave:
                tradetest.fast_buy(instance)
                price = instance.price()[0]
                message = '%s(%s)涨幅%s%%, 现价%s' %(name, code, wave, price)
                self.wave_list.append(code)
                self.df.loc[len(self.df)+1] = ['%s(%s)' %(name, code), wave, price]
                return message



@log('worklist')
def stop():
    wl.status = False
    print(wl.status)
    message = '状态%s, 等待线程结束' % wl.status
    return message



def prepare():
    tablename = datetime.now(timezone('Asia/Shanghai')).date().strftime('%b_%d_%Y')
    #tablename = '\'%s\'' % tablename
    tradetest.create_table('stock', tablename)


#wl = worklist()
#wl.start()


#wl.stop()
#wl.wave_checker(7,10.5)


checktime().wait(9,25,0)
prepare()
from stocklist import sl
wl = worklist()
checktime().wait(9,30,0)
wl.start()



if __name__ == '__main__':
    #import code
    #code.interact(banner = "", local = locals())
    pass
else:
    pass

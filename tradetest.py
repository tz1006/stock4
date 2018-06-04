#!/usr/bin/python3
# -*- coding: UTF-8 -*-
# filename: tradetest.py
# version: 4.0.0
# description: tradetest


from concurrent.futures import ProcessPoolExecutor
import psycopg2
import os
from datetime import datetime
from pytz import timezone

from stock import stock
from log import log

password = 'admin'


def create_db(dbname):
    if os.path.exists('database') == False:
        os.makedirs('database')
    con = psycopg2.connect(dbname='postgres',
        user='postgres', host='localhost',
        password=password)
    con.autocommit = True
    cur = con.cursor()
    cur.execute("CREATE DATABASE %s;" % dbname)
    print('创建数据库%s' % dbname)


# 在数据库'KDJ'中建立表 'test'/ TIME/ CODE/ NAME/ BS/ PRICE/ WAVE/ CLOSEWAVE/ MARKET
def create_table(dbname, tablename):
    try:
        create_db(dbname)
    except:
        pass
    con = psycopg2.connect(dbname=dbname,
        user='postgres', host='localhost',
        password=password)
    con.autocommit = True
    cur = con.cursor()
    cur.execute('''CREATE TABLE IF NOT EXISTS %s
        (TIME TEXT,
        CODE   char(6),
        NAME  TEXT,
        BS  TEXT,
        PRICE  decimal,
        WAVE  decimal,
        CLOSEWAVE  decimal);''' % tablename)
    print('创建表%s' % tablename)



def fast_buy(stock):
    pool =  ProcessPoolExecutor(max_workers=1)
    pool.submit(buy_stock, stock)


# code, name, bs, price, wave, market
def buy_stock(stock):
    dbname = 'stock'
    tablename = 'test'
    time = datetime.now(timezone('Asia/Shanghai')).strftime('%Y-%m-%d %H:%M:%S %Z')
    code = stock.code
    name = stock.name
    #print('正在写入 %s(%s)' % (code, name))
    bs = '买入'
    price = stock.price()[0]
    wave = stock.wave()[0]
    write_data(time, code, name, bs, price, wave)
    print(time, code, name, bs, price, wave)


def write_data(time, code, name, bs, price, wave):
    dbname = 'stock'
    tablename = 'test'
    time = '\'%s\'' % time
    code = '\'%s\'' % code
    name =  '\'%s\'' % name
    bs = '\'%s\'' % bs
    con = psycopg2.connect(dbname=dbname,
        user='postgres', host='localhost',
        password=password)
    con.autocommit = True
    cur = con.cursor()
    #print(code, name, price, average, time)
    cur.execute("INSERT INTO %s (TIME, CODE, NAME, BS, PRICE, WAVE) VALUES (%s, %s, %s, %s, %s, %s);" % (tablename, time, code, name, bs, price, wave))
    #message = '买入股票%s'
    print('写入 %s 数据成功！' % code)







#write_data('2018-03-20', '600122', '中国重工', '买入', 4.23, 3.99)






if __name__ == '__main__':
    import code
    code.interact(banner = "", local = locals())





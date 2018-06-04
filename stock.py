#!/usr/bin/python3
# -*- coding: UTF-8 -*- 
# filename: stock.py
# version: 1.0.1
# description: 股票

import requests
from datetime import datetime
from pytz import timezone
import json
from requests.packages.urllib3.exceptions import InsecureRequestWarning
requests.packages.urllib3.disable_warnings(InsecureRequestWarning)


class stock():
    def __init__(self, code):
        # 600123
        self.code = code
        # sh600123
        self.sscode = self._sscode()
        # 创业板
        #self.market = self.__market()
        # 兰花科创
        self.name = self._name()
        # True
        self.status = self._status()
        #self.open = gap(code)[0]
        #self.high = gap(code)[1]
        #self.low = gap(code)[2]
        #self.close = close(code)
        self.id = self._id()
    # sh600123
    def _sscode(self):
        code = str(self.code)
        if code[0]+code[1] =='60':
            code = 'sh%s' % code
        else:
            code = 'sz%s' % code
        return code
    # 停牌
    def _status(self):
        url = 'http://apiapp.finance.ifeng.com/stock/isopen?code=%s' % self.sscode
        with requests.session() as s:
            s.headers['connection'] = 'close'
            r = None
            while r == None:
                try:
                    r = s.get(url, timeout=5)
                except:
                    #print('Error!------------------------------------')
                    pass
        isopen = r.json()['data'][0]['isopen']
        if isopen == 1:
            return True
        else:
            return False
    # 股票名
    def _name(self):
        url = 'https://apiapp.finance.ifeng.com/getstockname?code=%s' % self.sscode
        with requests.session() as s:
            s.headers['connection'] = 'close'
            r = None
            while r == None:
                try:
                    r = s.get(url, timeout=5)
                except:
                    pass
        name = r.json()[self.code]
        return name
    # ID
    def _id(self):
        url = 'http://suggest.eastmoney.com/SuggestData/Default.aspx?type=1&input=%s' % self.code
        with requests.session() as s:
            s.headers['connection'] = 'close'
            r = None
            while r == None:
                try:
                    r = s.get(url, timeout=5)
                except:
                    pass
        index = r.text.split(',')[-2]
        id = '%s%s' % (self.code, index)
        return id
    # (价格, 均价)
    def price(self):
        url = 'https://api.finance.ifeng.com/aminhis/?code=%s&type=five' % self.sscode
        with requests.session() as s:
            s.headers['connection'] = 'close'
            r = None
            while r == None:
                try:
                    r = s.get(url, timeout=5, verify=False)
                except:
                    pass
        if r.text == '':
            #print('无法获取 %s 价格。' % stock_code)
            price = ''
            average = ''
        else:
            now = r.json()[-1]['record'][-1]
            # date
            date = now[0].split(' ')[0]
            # Price
            price = float(now[1])
            # diff
            diff = float(now[2])
            # Average
            average = float(now[4])
        return (price, average)
    # (涨幅, 价格波动)
    def wave(self):
        url = 'https://123.103.93.175/q.php?l=%s' % self.sscode
        #url = 'https://hq.finance.ifeng.com/q.php?l=%s' % self.sscode
        with requests.session() as s:
            s.headers['connection'] = 'close'
            r = None
            while r == None:
                try:
                    r = s.get(url, timeout=5, verify=False)
                except:
                    pass
        j = json.loads(r.text.split('=', 1)[1].split(';')[0])
        data = j[list(j)[0]]
        price = data[0]
        price_diff = data[2]
        wave = data[3]
        return (wave, price_diff)
    # 涨幅2
    # MA 当日 (ma5, ma10, ma20, ma30)
    def ma(self):
        now = datetime.now(timezone('Asia/Shanghai'))
        span = '%d%02d%02d' % (now.year, now.month, now.day)
        url = 'https://pdfm.eastmoney.com/EM_UBG_PDTI_Fast/api/js?id=%s&TYPE=k&rtntype=1&QueryStyle=2.2&QuerySpan=%s%%2C1&extend=ma' % (self.id, span)
        #print(url)
        with requests.session() as s:
            s.headers['connection'] = 'close'
            r = None
            while r == None:
                try:
                    r = s.get(url, timeout=5, verify=False)
                except:
                    pass
        if r.text == '({stats:false})':
            return
        else:
            date = r.text.split(',', 1)[0].split('(')[1]
            today = '%d-%02d-%02d' % (now.year, now.month, now.day)
            if date == today:
                ma_data = r.text.split('[')[1].split(']')[0].split(',')
                ma5 = float(ma_data[0])
                ma10 = float(ma_data[1])
                ma20 = float(ma_data[2])
                ma30 = float(ma_data[3])
                return(ma5, ma10, ma20, ma30)
            else:
                return
    # KDJ 当日 (k, d, j)
    def kdj(self):
        now = datetime.now(timezone('Asia/Shanghai'))
        span = '%d%02d%02d' % (now.year, now.month, now.day)
        url = 'https://pdfm.eastmoney.com/EM_UBG_PDTI_Fast/api/js?id=%s&TYPE=k&rtntype=1&QueryStyle=2.2&QuerySpan=%s%%2C1&extend=kdj' % (self.id, span)
        #print(url)
        with requests.session() as s:
            s.headers['connection'] = 'close'
            r = None
            while r == None:
                try:
                    r = s.get(url, timeout=5, verify=False)
                except:
                    pass
        if r.text == '({stats:false})':
            return
        else:
            date = r.text.split(',', 1)[0].split('(')[1]
            today = '%d-%02d-%02d' % (now.year, now.month, now.day)
            #today = '2018-03-15'
            if date == today:
                kdj_data = r.text.split('[')[1].split(']')[0].split(',')
                k = float(kdj_data[0])
                d = float(kdj_data[1])
                j = float(kdj_data[2])
                return(k, d, j)
            else:
            	return
    # MACD
    def macd(self):
        now = datetime.now(timezone('Asia/Shanghai'))
        span = '%d%02d%02d' % (now.year, now.month, now.day)
        url = 'https://pdfm.eastmoney.com/EM_UBG_PDTI_Fast/api/js?id=%s&TYPE=k&rtntype=1&QueryStyle=2.2&QuerySpan=%s%%2C1&extend=macd' % (self.id, span)
        #print(url)
        with requests.session() as s:
            s.headers['connection'] = 'close'
            r = None
            while r == None:
                try:
                    r = s.get(url, timeout=5, verify=False)
                except:
                    pass
        if r.text == '({stats:false})':
            return
        else:
            date = r.text.split(',', 1)[0].split('(')[1]
            today = '%d-%02d-%02d' % (now.year, now.month, now.day)
            #today = '2018-03-15'
            if date == today:
                macd_data = r.text.split('[')[1].split(']')[0].split(',')
                dif = float(macd_data[0])
                dea = float(macd_data[1])
                macd = float(macd_data[2])
                return(dif, dea, macd)
            else:
            	return
    def history(self):
        pass
    def help(self):
        print('''
        .code
        .name
        .status
        close
        open
        high
        low
        .price()
        .wave()
        .ma()
        .kdj()
        .macd
        .help
    ''')


if __name__ != '__main__':
    pass




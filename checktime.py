#!/usr/bin/python3
# -*- coding: UTF-8 -*-
# filename: checktime.py
# description: 等待，时间控制

from datetime import datetime, timedelta
from pytz import timezone
import time


class checktime():
    def before_close(self):
        now = datetime.now(timezone('Asia/Shanghai')).replace(tzinfo=None)
        # 当日闭市时间
        close = now.replace(hour=15, minute=00, second=0)
        if close > now:
            return True
        else:
            return False
    def wait(self, hour, minute, second):
        now = datetime.now(timezone('Asia/Shanghai')).replace(tzinfo=None)
        weekday = now.isoweekday()
        # 闭市之前
        if self.before_close() == True:
            # 周六周日
            if weekday > 5:
                day = 8 - weekday
                now = now + timedelta(days=day)
        # 闭市之后
        else:
            # 周一到周四, 周日（次日交易）
            if weekday < 5 or weekday == 7:
                day = 1
                now = now + timedelta(days=day)
            # 周五周六
            else:
                day = 8 - weekday
                now = now + timedelta(days=day)
        schedule_time = now.replace(hour=hour, minute=minute, second=second)
        sleep_time = (schedule_time - now).total_seconds()
        if sleep_time < 0:
            sleep_time = 0
        sleep_day = sleep_time // 86400
        sleep_hour = (sleep_time % 86400) // 3600
        sleep_minute = (sleep_time % 86400 % 3600) // 60
        sleep_second = (sleep_time % 86400 % 3600 % 60)
        message = '等待%d天%d小时%d分%d秒' % (sleep_day, sleep_hour, sleep_minute, sleep_second)
        print(message)
        #print(sleep_time)
        time.sleep(sleep_time)


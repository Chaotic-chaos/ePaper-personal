# -*- coding: utf-8 -*-
'''
Project:       /home/pi/Projects/persoanlCalendar/app
File Name:      timer.py
Author:        Chaos
Email:         life0531@foxmail.com
Date:          2021/10/24
Software:      Vscode
'''

import time, logging
from PIL import ImageFont

class TimeFlusher:
    def __init__(self, font_path) -> None:
        self.weekday = {
        "Mon": "周一",
        "Tue": "周二",
        "Wed": "周三",
        "Thu": "周四",
        "Fri": "周五",
        "Sat": "周六",
        "Sun": "周日"
        }
        self.font_big = ImageFont.truetype(font=font_path, size=55)
        self.font_small = ImageFont.truetype(font=font_path, size=16)

    def __call__(self, epd, drawer, last_time):
        current_time = time.strftime("%H:%M", time.localtime())
        if current_time == last_time:
            return False, last_time
        else:
            current_date = time.strftime("%Y-%m-%d;%a", time.localtime())
            current_date = ",   ".join([current_date.split(";")[0],self.weekday.get(current_date.split(";")[-1])])

            drawer.text((10, 10), current_time, font=self.font_big, fill=0)
            drawer.text((13, 80), current_date, font=self.font_small, fill=0)

            # draw a line
            drawer.rectangle((0, 105, epd.width, 110), fill=0)
            drawer.rectangle((170, 0, 175, 110), fill=0)

            logging.info(f"Time Flushing Successfully!")

            return True, current_time
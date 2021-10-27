# -*- coding: utf-8 -*-
'''
Project:       /home/pi/Projects/persoanlCalendar/app
File Name:     deve.py
Author:        Chaos
Email:         life0531@foxmail.com
Date:          2021/10/23
Software:      Vscode
'''

'''开发使用'''

import time
from waveshare_epd import epd4in2bc, epd4in2
from PIL import Image,ImageDraw,ImageFont
import logging
from schedule import repeat, every, run_pending

# set logger
LOG_FORMAT = "%(asctime)s - %(levelname)s - %(message)s"
DATE_FORMAT = "%m/%d/%Y %H:%M:%S %p"
logging.basicConfig(level=logging.INFO, format=LOG_FORMAT, datefmt=DATE_FORMAT)


font_path = "/home/pi/Projects/test_epaper/e-Paper/test_my/lib/Font.ttc"
# epd = epd4in2bc.EPD()
epd = epd4in2.EPD()
epd.init()
epd.Clear()
logging.info("e-paper initlized!")

# epd.Clear()
# logging.info("e-paper cleared!")

# image_b = Image.new('1', (epd.width, epd.height), 255)
# image_r = Image.new('1', (epd.width, epd.height), 0)
# font60 = ImageFont.truetype(font=font_path, size=60)
# font17 = ImageFont.truetype(font=font_path, size=17)

def flush_time(epd, drawer_b, drawer_r, last_time):
    weekday = {
        "Mon": "周 一",
        "Tue": "周 二",
        "Wed": "周 三",
        "Thu": "周 四",
        "Fri": "周 五",
        "Sat": "周 六",
        "Sun": "周 日"
    }
    font60 = ImageFont.truetype(font=font_path, size=60)
    font17 = ImageFont.truetype(font=font_path, size=17)

    current_time = time.strftime("%H:%M", time.localtime())
    if current_time == last_time:
        return False, last_time
    else:
        current_date = time.strftime("%Y-%m-%d;%a", time.localtime())
        current_date = ",    ".join([current_date.split(";")[0], weekday.get(current_date.split(";")[-1])])

        drawer_b.text((10, 10), current_time, font=font60, fill=0)
        drawer_b.text((13, 80), current_date, font=font17, fill=0)

        # draw a line
        drawer_b.rectangle((0, 105, epd.width, 110), fill=0)
        drawer_b.rectangle((170, 0, 175, 110), fill=0)

        logging.info(f"Time Flushing Successfully!")

        return True, current_time

class tasks_sequence:
    def __init__(self, epd) -> None:
        # self.image_b = image_b
        # self.image_r = image_r
        self.epd = epd
        # self.drawer_b = ImageDraw.Draw(self.image_b)
        # self.drawer_r = ImageDraw.Draw(self.image_r)
        self.last_time = 0

    def tasks(self):
        # generate new pic
        self.image_b = Image.new('1', (epd.width, epd.height), 255)
        self.image_r = Image.new('1', (epd.width, epd.height), 0)
        self.drawer_b = ImageDraw.Draw(self.image_b)
        self.drawer_r = ImageDraw.Draw(self.image_r)
         
        need_flush, self.last_time = flush_time(self.epd, self.drawer_b, self.drawer_r, self.last_time)

        if need_flush:
            self.epd.init()
            # self.epd.Clear()
            # self.epd.display(self.epd.getbuffer(self.image_b), self.epd.getbuffer(self.image_r))
            self.epd.display(self.epd.getbuffer(self.image_b))
            self.epd.sleep()

        return 


if __name__ == '__main__':
    # tasks = tasks_sequence(epd)
    # tasks.tasks()

    # every(3).seconds.do(tasks.tasks)
    # while True:
    #     run_pending()
    #     time.sleep(1)

    # image = Image.new("1", (epd.width, epd.height), 255)
    # image2 = Image.new("1", (10, 10), 255)
    font17 = ImageFont.truetype(font=font_path, size=17)

    # drawer = ImageDraw.Draw(image)
    # drawer2 = ImageDraw.Draw(image2)

    # drawer.rectangle((30, 30, 40, 40), fill=0)
    # epd.display(epd.getbuffer(image))

    # drawer2.text((0, 0), "hello", font=font17, fill=0)
    # epd.display(epd.getbuffer(image2))

    # import requests

    # requests.get(url="http://wttr.in/Chenggong+Kunming?2AFqTn")
    # print(1111)

    # print(time.mktime(time.strptime("08:00:00", "%H:%M:%S")))

    image = Image.new('1', (epd.width, epd.height), 255)
    drawer = ImageDraw.Draw(image)

    pic = Image.open("/home/pi/Projects/persoanlCalendar/utils/rain.bmp")
    image.paste(pic, (100, 100))
    drawer.text((175, 80), "Hello", font=font17, fill=0)
    epd.display(epd.getbuffer(image))

    # def test(**kargs):
    #     print(kargs['a'])

    # test(a=111)

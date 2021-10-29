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

from datetime import date
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
# epd = epd4in2.EPD()
# epd.init()
# epd.Clear()
# logging.info("e-paper initlized!")

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

    # image = Image.new('1', (epd.width, epd.height), 255)
    # drawer = ImageDraw.Draw(image)

    # pic = Image.open("/home/pi/Projects/persoanlCalendar/utils/rain.bmp")
    # image.paste(pic, (100, 100))
    # drawer.text((175, 80), "Hello", font=font17, fill=0)
    # epd.display(epd.getbuffer(image))

    # def test(**kargs):
    #     print(kargs['a'])

    # test(a=111)
    import datetime

    # l = datetime.datetime.now() - datetime.timedelta(minutes=10)
    # c = datetime.datetime.now()
    # print(c)

    # a = datetime.datetime.now()
    # time.sleep(2)
    # b = datetime.datetime.now()

    # print((b-a).seconds)
    # print(a, b)

    # import requests
    # headers = {
    #     "Authorization": "Bearer  EwBwA8l6BAAUwihrrCrmQ4wuIJX5mbj7rQla6TUAAcdAZYChRCRZcrpo0QHx1RJSc/ZHV1ZVzn3x66xtSxuLvXiMS9YU2Cb3a+Uy9HztCx32jD4AunMnoCUCipMRzhvpe9uGZz/dLmDQDE6kpngTg9b2hdltrXtDm8REiWqXJKRRZll8UsMHGZ9rsYZcx+kxM+jvhQKBf5Z5A3xzJmgd4+TX54q0/eDOGvP8uctVy5LZMVC1BMOU4fj4OTRrVXHNDwopK61m+t5nM1FSS9wKfM1pGtFhkP6SaV2qeDP3wSCDCyv09i427wtAx/VB+mg2Hq4H3p/dcJrR+yb0nhmmZJiC7ge0gC/7ub54HlHx4q27sQAHnWypC4TYK6pPWogDZgAACBsvkD55/tIFQAKqg6rWarfsqnZirMuosIaKRGahZwUgBDPO0hQBAaYF29YeAvDM0CaNPrYCzsS02q5MxLVe4tZWxdcUmYeJdrzkV/365gr5g0tAyEXE6EWsKZVnwwPKuAPXH3F8Bj9FEw055KBkMu5FIVrQ36Qp8ZiKDbZfkT3X8HVqCrGV+60UEXEQNR4MQKJBmBWoSuA4ZJkTzHetHfKInTKJb2hfDmYzaQ7OnJ0Sh5sBd7BB+698XnbKR5C2rigjuhAb+Zx0FlP2q3LCaWykR2lo31IBI7aKPCfSClS0N79CpktJuoKMpIfxhxJA4HoALsTCsxAFAHg/fQp0BRKacmmKhxmqMG6rx3YYuW6abgfrEx9CWh3PKRjwkfvxU0RctVmlqpy5ocawpexm/hdZAxK/YoCbxOa/5Za/aqikEn62wp/htavaSBUFjb72L3xce4j8i5PzJPMtegl5MYgk8G0E9Bbj4eaCU8V5897ESwHVFvHRSIZeNOX9sbyavY4t0ojlKLSwzmvGF+iASPxinLBJkIC0c0UXZ2YufBgo1hD+fE/PAUwj0IsFYh9KLidAb/F6XVwRXaVlYq/K73goiUkLjVz0Fuovn5hycb7KtNBvD9l9fWBM9bNyPyLRpXnpyXt3iL52l9mbEsLIT159GJXdsHN7EX+tXKnX49msGSJBe4sYT5FcRM5nhmokKDPEy5QtP/Gp6aDzyKsOOI3aQ/5f4kQrtqZR/mpCFO0jSxiuqX8UeL1Kv1aM+wAcGRKAQxWgObdNgadsAg=="
    # }
    # url = "https://graph.microsoft.com/beta/me/todo/lists/AQMkADAwATM0MDAAMS1kMzY1LTY0MTEALTAwAi0wMAoALgAAA2JAbHQOgLRBoOacz5TFflUBAMO9PI1aWgDBQJ2emHPLw1kAAAACFmCSdAAAAA==/tasks"

    # try:
    #     print(requests.post(url=url, headers=headers).status_code)
    # except:
    #     print(111)

    # a = {}

    # b = 111

    # a["test"] = []

    # # a["test"].append(b)
    # print(len(a['test']))
    import re

    task = "测试测试测试测试测试测试测试测试测试测试ces"

    a = "\n".join(re.findall(r".{5}", task))+f'\n{task[len(re.findall(r".{5}", task)*5):]}'
    print(a)


# -*- coding: utf-8 -*-
'''
Project:       /home/pi/Projects/persoanlCalendar/app
File Name:     weather.py
Author:        Chaos
Email:         life0531@foxmail.com
Date:          2021/10/26
Software:      Vscode
'''

from email.policy import default
from PIL import Image, ImageFont
import time
import requests
import logging
import datetime


class Weather:
    def __init__(self, font_path, city, key):
        self.base_url = "https://restapi.amap.com/v3/weather/weatherInfo"
        self.city = city
        self.settings = "extensions=all&output=json"
        self.font_big = ImageFont.truetype(font=font_path, size=40)
        self.font_small = ImageFont.truetype(font=font_path, size=16)
        self.font_tiny = ImageFont.truetype(font=font_path, size=10)
        self.key = key
        self.weather_res = {}
        self.weather_pic_path = {
            "rain": "/home/pi/Projects/persoanlCalendar/utils/rain.bmp",
            "cloud": "/home/pi/Projects/persoanlCalendar/utils/cloud.bmp",
            "sunny": "/home/pi/Projects/persoanlCalendar/utils/sunny.bmp",
            "default": "/home/pi/Projects/persoanlCalendar/utils/default.bmp"
        }
        self.last_report_time = 0

    def __call__(self, epd, drawer, **kargs):
        # get weather at 8:00-8:40, 11:00-11:40, 18:00-18:40, 22:00-22:40 every day
        remote_fulsh_time = []
        for i in range(4):
            durition = {}
            if i == 0:
                durition["start"] = datetime.datetime.strptime(str(datetime.datetime.now().date())+'08:00', '%Y-%m-%d%H:%M')
                durition["end"] = datetime.datetime.strptime(str(datetime.datetime.now().date())+'08:40', '%Y-%m-%d%H:%M')
                # remote_fulsh_time[i]["start"] = datetime.datetime.strptime(str(datetime.datetime.now().date())+'08:00', '%Y-%m-%d%H:%M')
                # remote_fulsh_time[i]["end"] = datetime.datetime.strptime(str(datetime.datetime.now().date())+'08:40', '%Y-%m-%d%H:%M')
                remote_fulsh_time.append(durition)
            elif i == 1:
                durition["start"] = datetime.datetime.strptime(str(datetime.datetime.now().date())+'11:00', '%Y-%m-%d%H:%M')
                durition["end"] = datetime.datetime.strptime(str(datetime.datetime.now().date())+'11:40', '%Y-%m-%d%H:%M')
                # remote_fulsh_time[i]["start"] = datetime.datetime.strptime(str(datetime.datetime.now().date())+'11:00', '%Y-%m-%d%H:%M')
                # remote_fulsh_time[i]["end"] = datetime.datetime.strptime(str(datetime.datetime.now().date())+'11:40', '%Y-%m-%d%H:%M')
                remote_fulsh_time.append(durition)
            elif i == 2:
                durition["start"] = datetime.datetime.strptime(str(datetime.datetime.now().date())+'18:00', '%Y-%m-%d%H:%M')
                durition["end"] = datetime.datetime.strptime(str(datetime.datetime.now().date())+'18:40', '%Y-%m-%d%H:%M')
                # remote_fulsh_time[i]["start"] = datetime.datetime.strptime(str(datetime.datetime.now().date())+'18:00', '%Y-%m-%d%H:%M')
                # remote_fulsh_time[i]["end"] = datetime.datetime.strptime(str(datetime.datetime.now().date())+'18:40', '%Y-%m-%d%H:%M')
                remote_fulsh_time.append(durition)
            elif i == 3:
                durition["start"] = datetime.datetime.strptime(str(datetime.datetime.now().date())+'22:00', '%Y-%m-%d%H:%M')
                durition["end"] = datetime.datetime.strptime(str(datetime.datetime.now().date())+'22:40', '%Y-%m-%d%H:%M')
                # remote_fulsh_time[i]["start"] = datetime.datetime.strptime(str(datetime.datetime.now().date())+'22:00', '%Y-%m-%d%H:%M')
                # remote_fulsh_time[i]["end"] = datetime.datetime.strptime(str(datetime.datetime.now().date())+'22:40', '%Y-%m-%d%H:%M')
                remote_fulsh_time.append(durition)
        permission_to_get_weather = False
        # 当前时间
        n_time = datetime.datetime.now()
        for t in remote_fulsh_time:
            if n_time > t["start"] and n_time < t["end"]:
                permission_to_get_weather = True

        if not permission_to_get_weather:
            # check if there's a history 
            if self.weather_res == {}:
                try:
                    self.weather_res = requests.get(url=f"{self.base_url}?key={self.key}&city={self.city}&{self.settings}").json()
                    self.last_report_time = self.weather_res["forecasts"][0]["reporttime"]
                    logging.debug("get weather successfully!")
                except Exception as e:
                    logging.warning("Get weather failed, use the history!")

            # draw history for the potential fulsh
            # draw line
            # drawer.rectangle((285, 0, 287, 110), fill=0)
            
            # draw all 
            # today's 
            # decide the pic
            if "雨" in self.weather_res["forecasts"][0]["casts"][0]["dayweather"]:
                pic = self.weather_pic_path["rain"]
            elif "晴" in self.weather_res["forecasts"][0]["casts"][0]["dayweather"]:
                pic = self.weather_pic_path["sunny"]
            elif "阴" in self.weather_res["forecasts"][0]["casts"][0]["dayweather"]:
                pic = self.weather_pic_path["cloud"]
            else:
                pic = self.weather_pic_path["default"]
            icon = Image.open(pic)
            kargs['image'].paste(icon, (230, 0, 285, 55))
            # draw city
            drawer.text((185, 5), f'{self.weather_res["forecasts"][0]["city"]}', font=self.font_tiny, fill=0)
            # draw date
            drawer.text((185, 80), f'{"-".join(self.weather_res["forecasts"][0]["casts"][0]["date"].split("-")[1:])},  {self.weather_res["forecasts"][0]["casts"][0]["dayweather"]}', font=self.font_small, fill=0)
            # draw temperture
            drawer.text((185, 35), f'{self.weather_res["forecasts"][0]["casts"][0]["daytemp"]}', font=self.font_big, fill=0)
            drawer.text((230, 60), f'  ~{self.weather_res["forecasts"][0]["casts"][0]["nighttemp"]}', font=self.font_small, fill=0)
            drawer.text((270, 63), f"℃", font=self.font_tiny, fill=0)
            # tomorrow
            # decide the pic
            if "雨" in self.weather_res["forecasts"][0]["casts"][0]["dayweather"]:
                pic = self.weather_pic_path["rain"]
            elif "晴" in self.weather_res["forecasts"][0]["casts"][0]["dayweather"]:
                pic = self.weather_pic_path["sunny"]
            elif "阴" in self.weather_res["forecasts"][0]["casts"][0]["dayweather"]:
                pic = self.weather_pic_path["cloud"]
            else:
                pic = self.weather_pic_path["default"]
            icon = Image.open(pic)
            kargs['image'].paste(icon, (epd.width-55, 0, epd.width, 55))
            # draw date
            drawer.text((300, 80), f'{"-".join(self.weather_res["forecasts"][0]["casts"][1]["date"].split("-")[1:])},  {self.weather_res["forecasts"][0]["casts"][0]["dayweather"]}', font=self.font_small, fill=0)
            # draw temperture
            drawer.text((300, 35), f'{self.weather_res["forecasts"][0]["casts"][1]["daytemp"]}', font=self.font_big, fill=0)
            drawer.text((345, 60), f'  ~{self.weather_res["forecasts"][0]["casts"][1]["nighttemp"]}', font=self.font_small, fill=0)
            drawer.text((385, 63), f"℃", font=self.font_tiny, fill=0)

            return False

        try:
            self.weather_res = requests.get(url=f"{self.base_url}?key={self.key}&city={self.city}&{self.settings}").json()
            logging.debug("get weather successfully!")
        except Exception as e:
            logging.error("Get weather failed, use the history!")

        # draw line
        # drawer.rectangle((285, 0, 287, 110), fill=0)

        # draw all
        # today's 
        # decide the pic
        if "雨" in self.weather_res["forecasts"][0]["casts"][0]["dayweather"]:
            pic = self.weather_pic_path["rain"]
        elif "晴" in self.weather_res["forecasts"][0]["casts"][0]["dayweather"]:
            pic = self.weather_pic_path["sunny"]
        elif "阴" in self.weather_res["forecasts"][0]["casts"][0]["dayweather"]:
            pic = self.weather_pic_path["cloud"]
        else:
            pic = self.weather_pic_path["default"]
        icon = Image.open(pic)
        kargs['image'].paste(icon, (230, 0, 285, 55))
        # draw city
        drawer.text((185, 5), f'{self.weather_res["forecasts"][0]["city"]}', font=self.font_tiny, fill=0)
        # draw date
        drawer.text((185, 80), f'{"-".join(self.weather_res["forecasts"][0]["casts"][0]["date"].split("-")[1:])},  {self.weather_res["forecasts"][0]["casts"][0]["dayweather"]}', font=self.font_small, fill=0)
        # draw temperture
        drawer.text((185, 35), f'{self.weather_res["forecasts"][0]["casts"][0]["daytemp"]}', font=self.font_big, fill=0)
        drawer.text((230, 60), f'  ~{self.weather_res["forecasts"][0]["casts"][0]["nighttemp"]}', font=self.font_small, fill=0)
        drawer.text((270, 63), f"℃", font=self.font_tiny, fill=0)
        # tomorrow
        # decide the pic
        if "雨" in self.weather_res["forecasts"][0]["casts"][0]["dayweather"]:
            pic = self.weather_pic_path["rain"]
        elif "晴" in self.weather_res["forecasts"][0]["casts"][0]["dayweather"]:
            pic = self.weather_pic_path["sunny"]
        elif "阴" in self.weather_res["forecasts"][0]["casts"][0]["dayweather"]:
            pic = self.weather_pic_path["cloud"]
        else:
            pic = self.weather_pic_path["default"]
        icon = Image.open(pic)
        kargs['image'].paste(icon, (epd.width-55, 0, epd.width, 55))
        # draw date
        drawer.text((300, 80), f'{"-".join(self.weather_res["forecasts"][0]["casts"][1]["date"].split("-")[1:])},  {self.weather_res["forecasts"][0]["casts"][0]["dayweather"]}', font=self.font_small, fill=0)
        # draw temperture
        drawer.text((300, 35), f'{self.weather_res["forecasts"][0]["casts"][1]["daytemp"]}', font=self.font_big, fill=0)
        drawer.text((345, 60), f'  ~{self.weather_res["forecasts"][0]["casts"][1]["nighttemp"]}', font=self.font_small, fill=0)
        drawer.text((385, 63), f"℃", font=self.font_tiny, fill=0)

        if self.last_report_time == self.weather_res["forecasts"][0]["reporttime"]:
            
            return True
            logging.debug("Weather need flush!")

        else:
            return False

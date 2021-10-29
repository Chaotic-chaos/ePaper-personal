# -*- coding: utf-8 -*-
'''
Project:       /home/pi/Projects/persoanlCalendar/app
File Name:     setup_screen.py
Author:        Chaos
Email:         life0531@foxmail.com
Date:          2021/10/29
Software:      Vscode
'''

'''draw lines to split up the screen'''

from PIL import ImageFont

class Starter:
    def __init__(self) -> None:
        pass

    def __call__(self, **kargs):
        # setup screen
        epd = kargs["epd"]
        drawer = kargs["drawer"]

        # draw lines
        # central line
        drawer.rectangle((0, 105, epd.width, 110), fill=0)
        # timer & weather
        drawer.rectangle((170, 0, 175, 110), fill=0)
        # down
        drawer.rectangle((300, 105, 305, epd.height), fill=0)
        # todoer's split lines
        drawer.rectangle((0, 155, 300, 156), fill=0)
        drawer.rectangle((0, 205, 300, 206), fill=0)
        drawer.rectangle((0, 255, 300, 256), fill=0)

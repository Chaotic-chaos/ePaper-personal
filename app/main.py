# -*- coding: utf-8 -*-
'''
Project:       /home/pi/Projects/persoanlCalendar/app
File Name:     main.py
Author:        Chaos
Email:         life0531@foxmail.com
Date:          2021/10/26
Software:      Vscode
'''

'''主入口文件'''

import argparse, logging, time
from waveshare_epd import epd4in2
from schedule import every, run_pending

from tasks import Tasks

# set logger
# set logger
LOG_FORMAT = "%(asctime)s - %(levelname)s - %(message)s"
DATE_FORMAT = "%m/%d/%Y %H:%M:%S %p"
logging.basicConfig(level=logging.DEBUG, format=LOG_FORMAT, datefmt=DATE_FORMAT)

parser = argparse.ArgumentParser()

parser.add_argument("--font-path", default="/home/pi/Projects/persoanlCalendar/utils/STHeiti-Medium-4.ttc")


args = parser.parse_args()

if __name__ == '__main__':
    # set epd
    epd = epd4in2.EPD()
    epd.init()
    epd.Clear()
    logging.info("e-paper initlized!")

    # setup tasker
    tasker = Tasks(epd=epd, font_path=args.font_path)
    tasker.setup_tasks()

    # run all task once
    tasker.run()

    # setup schduler
    # every(3).seconds.do(tasker.run)
    
    # # start tasks
    # while True:
    #     run_pending()
    #     time.sleep(1)
    
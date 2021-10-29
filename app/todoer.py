# -*- coding: utf-8 -*-
'''
Project:       /home/pi/Projects/persoanlCalendar/app
File Name:     todoer.py
Author:        Chaos
Email:         life0531@foxmail.com
Date:          2021/10/29
Software:      Vscode
'''

'''todo-list module'''

import datetime
from PIL import ImageFont

import requests
from requests.api import get
from requests.models import encode_multipart_formdata
from requests.sessions import TooManyRedirects
from waveshare_epd.epd4in2 import GRAY1


class Todoer:
    def __init__(self, **kargs) -> None:
        # setup this module

        # token releated
        self.refresh_url = "https://login.microsoftonline.com/consumers/oauth2/v2.0/token"
        self.client_id = kargs["client_id"]
        self.refresh_token = kargs["refresh_token"]
        self.client_secret = kargs["client_secret"]
        self.access_token = None

        # task releated
        self.task_list_ids = kargs["task_list_ids"]
        self.catagory_expression = kargs["catagory_expression"]
        self.get_list_url = "https://graph.microsoft.com/beta/me/todo/lists"
        self.tasks = []

        # record time
        self.last_udpate_time = datetime.datetime.now() - datetime.timedelta(minutes=10)

        # epaper releated
        self.font_path = kargs["font_path"]


    def __call__(self, **kargs):
        # in case first run there's no access_token
        self._get_access_token()
        # check if there's ten minutes since last update
        current_time = datetime.datetime.now()
        if (current_time - self.last_udpate_time).seconds >= 300:
            # more than 5 mins since last update, update the tasks
            # update tasks with listIDs
            self.tasks.clear()
            for name, id in self.task_list_ids.items():
                header = {"Authorization": f"Bearer {self.access_token}"}
                url = f"{self.get_list_url}/{id}/tasks"
                get_list_res = requests.get(url=url, headers=header)
                while get_list_res.status_code != 200:
                    # get tasks failed
                    # refresh token
                    self._get_access_token()
                    get_list_res = requests.get(url=url, headers=header)

                # decode the result
                for task in get_list_res.json()["value"]:
                    # check if hit 'completed' then break this loop
                    if task["status"] == "completed":
                        continue
                    # else, upadte the task list
                    self.tasks.append(f'{self.catagory_expression[name]}  {task["title"]}')
            self.last_udpate_time = datetime.datetime.now()
        
        # draw the screen
        # setup screen
        font_task = ImageFont.truetype(font=self.font_path, size=13)
        drawer = kargs["drawer"]
        epd = kargs["epd"]
        
        # draw tasks
        # calculate all tasks count
        for grid in range(min(4, len(self.tasks))):
            # there's only 4 empty grids, otherwise will trancate
            # display
            drawer.text((10, 120+50*grid), self.tasks[grid], font=font_task, fill=0)
        


    def _get_access_token(self):
        # get or refresh the access_token
        body = {
            "client_id": self.client_id,
            "grant_type": "refresh_token",
            "scope": "Tasks.ReadWrite",
            "refresh_token": self.refresh_token,
            "redirect_uri": "http://localhost",
            "client_secret": self.client_secret
        }
        self.access_token = requests.post(url=self.refresh_url, data=body).json()["access_token"]


if __name__ == '__main__':
    pass

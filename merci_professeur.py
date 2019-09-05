#!/usr/bin/env python3
from os import path
import json

# Waypoint 1: Write a Python Class Episode
class Episode:
    def __init__(self, title, page_url, image_url, broadcasting_date, duration):
        self.__title = title
        self.__page_url = page_url
        self.__image_url = image_url
        self.__broadcasting_date = broadcasting_date
        self.__duration = duration

    @property
    def title(self):
        return self.__title

    @property
    def page_url(self):
        return 'http://www.tv5monde.com' + self.__page_url

    @property
    def image_url(self):
        return self.__image_url

    @property
    def broadcasting_date(self):
        return self.__broadcasting_date

    @property
    def duration(self):
        return self.__duration
    
    @staticmethod
    def from_json(payload):
        title = payload['title']
        page_url = payload['url']
        image_url = payload['image']
        broadcasting_date = payload['date']
        duration = payload['duration']
        return Episode(title, page_url, image_url, broadcasting_date, duration)

    @staticmethod
    def __parse_episode_id(url):
        episode_id = path.basename(url).split('.')[0]
        return episode_id

    @property
    def episode_id(self):
        self.__episode_id = self.__parse_episode_id(self.__image_url)
        return self.__episode_id

with open('./merci-professeur.json','r') as f:
    content = f.read()
json_data = json.loads(content)
payloads = json_data['episodes']
payload = payloads[0]
episode = Episode.from_json(payload)
print(episode.title)
print(episode.page_url)
print(episode.image_url)
print(episode.broadcasting_date)
print(episode.duration)
print(episode.episode_id)

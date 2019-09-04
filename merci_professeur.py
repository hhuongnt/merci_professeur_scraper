#!/usr/bin/env python3
import json

# Waypoint 1: Write a Python Class Episode
class Episode:
    def __init__(self, title, page_url, image_url, broadcasting_date):
        self.__title = title
        self.__page_url = page_url
        self.__image_url = image_url
        self.__broadcasting_date = broadcasting_date

    @property
    def title(self):
        return self.__title

    @property
    def page_url(self):
        return self.__page_url

    @property
    def image_url(self):
        return self.__image_url

    @property
    def broadcasting_date(self):
        return self.__broadcasting_date

    @staticmethod
    def from_json(payload):
        title = payload['title']
        page_url = payload['url']
        image_url = payload['image']
        broadcasting_date = payload['date']
        return Episode(title, page_url, image_url, broadcasting_date)
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

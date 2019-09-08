#!/usr/bin/env python3
import os
import time
import json
from urllib import error, request
from urllib.parse import urlparse

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

# Waypoint 2: Retrieve the Identification of an Episode
    @staticmethod
    def __parse_episode_id(url):
        episode_id = os.path.basename(url).split('.')[0]
        return episode_id

    @property
    def episode_id(self):
        self.__episode_id = self.__parse_episode_id(self.__image_url)
        return self.__episode_id
# with open('./merci-professeur.json','r') as f:
#     content = f.read()
# json_data = json.loads(content)
# payloads = json_data['episodes']
# payload = payloads[0]
# episode = Episode.from_json(payload)
# print(episode.title)
# print(episode.page_url)
# print(episode.image_url)
# print(episode.broadcasting_date)
# print(episode.duration)
# print(episode.episode_id)


# Waypoint 3: Fetch the List of Episodes
def read_url(url, sleep_duration_between_attempts=1):
    """
    Return data fetched from a HTTP endpoint.


    @param url: A Uniform Resource Locator (URL) that references the
        endpoint to open and read data from.

    @param sleep_duration_between_attempts: Time in seconds during which
        the current thread is suspended after a failed attempt to fetch
         data from the specified URL, before a next attempt.


    @return: The data read from the specified URL.


    @raise HTTPError: If an error occurs when trying unsuccessfully
        several times to fetch data from the specified URL
    """
    try:
        user_agent = 'Mozilla/4.0 (compatible; MSIE 5.5; Windows NT)'
        headers = {'User-Agent': user_agent}
        req = request.Request(url, headers=headers)
        response = request.urlopen(req)
        html = response.read()
        # return bytes type
        return html
    except error.HTTPError as e:
        if e.code == 503:
            time.sleep(sleep_duration_between_attempts)
            print(e.code)
            print('continue')
            return read_url(url)
        else:
            return e
# url = 'http://www.tv5monde.com/emissions/episodes/merci-professeur.json'
# url = 'http://www.fakewebsite.blabla.com'
# print(type(read_url(url)))


def fetch_episodes(url):
    """
    Return a list of objects Episode from all pages
    """
    episodes = []
    if 'page' not in url:
        url = url + '?page={}'
    html = read_url(url.format(1))
    # decode bytes to string then load to json
    json_data = json.loads(html.decode('utf-8'))
    # Waypoint 4: Fetch the List of all the Episodes
    numpages = json_data['numPages']
    for i in range(1, numpages+1):
        new_url = url.format(i)
        html = read_url(new_url)
        json_data = json.loads(html.decode('utf-8'))
        episodes_data = json_data['episodes']
        for episode_data in episodes_data:
            episodes.append(Episode.from_json(episode_data))
    return episodes
# url = 'http://www.tv5monde.com/emissions/episodes/merci-professeur.json'
# episodes = fetch_episodes(url)
# print(len(episodes))
# for episode in episodes:
#     print(episode.title, episode.episode_id)


# Waypoint 5: Parse Broadcast Data of an Episode
def fetch_episode_html_page(episode):
    """
    Returns the textual HTML content of the episode page (cf. page_url).
    This function calls the function read_url to read data (bytes) from
    the specified URL, and converts these data (encoded in UTF-8) to a string
    """
    url = episode.page_url
    html = read_url(url)
    return html.decode('utf-8')


def parse_broadcast_data_attribute(html_page):
    for line in html_page.split('\n'):
        if 'hlstv5mplus-vh.akamaihd.net' in line:
            broadcast_data_line = line
    broadcast_data_line = broadcast_data_line.split("data-broadcast='")[1]
    broadcast_attribute = broadcast_data_line.split("' data-duration")[0]
    return json.loads(broadcast_attribute)
# url = 'http://www.tv5monde.com/emissions/episodes/merci-professeur.json'
# episodes = fetch_episodes(url)
# episode = episodes[0]
# html_page = fetch_episode_html_page(episode)
# print(parse_broadcast_data_attribute(html_page))


# Waypoint 6: Build a URL Pattern of the Video Segments of an Episode
def build_segment_url_pattern(broadcast_data):
    url_sample = broadcast_data['files'][0]['url']
    url = url_sample.split('master.m3u8')[0] + 'segment{}_3_av.ts?null=0'
    o = urlparse(url)
    return o.scheme + '://' + o.netloc + '/' + o.path
url = 'http://www.tv5monde.com/emissions/episodes/merci-professeur.json?page={}'
episodes = fetch_episodes(url)
print(len(episodes))
episode = episodes[0]
print(episode.page_url)
html_page = fetch_episode_html_page(episode)
broadcast_data = parse_broadcast_data_attribute(html_page)
segment_url_pattern = build_segment_url_pattern(broadcast_data)
print(segment_url_pattern)
print(segment_url_pattern.format('1'))


# Waypoint 7: Download the Video Segments of an Episode
def download_episode_video_segments(episode, path='./'):
    html_page = fetch_episode_html_page(episode)
    broadcast_data = parse_broadcast_data_attribute(html_page)
    dwn_link = build_segment_url_pattern(broadcast_data)
    episode_id = episode.episode_id
    file_name = 'segment_{}_{}.ts'
    segment = 1
    status_code = 200
    while status_code == 200:
        new_dwn_link = dwn_link.format(segment)
        req = request.urlopen(new_dwn_link)
        status_code = req.getcode()
        file_name = file_name.format(episode_id, segment)
        print(file_name)
        dump_dir = os.path.join(path, file_name)
        with open(dump_dir, 'wb') as f:
            f.write(req.read())
        segment += 1
    # while
url = 'http://www.tv5monde.com/emissions/episodes/merci-professeur.json?page={}'
episode = episodes[0]
download_episode_video_segments(episode)

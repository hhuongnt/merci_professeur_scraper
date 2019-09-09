#!/usr/bin/env python3
import os
import time
import json
from urllib import error, request
from urllib.parse import urlparse
from io import BytesIO

# Waypoint 1: Write a Python Class Episode
class Episode:
    """
    Object Episode with folowing attributes:

    @title: The title of the episode

    @page_url: The Uniform Resource Locator (URL) of the Web page
        dedicated to this episode

    @image_url: The Uniform Resource Locator (URL) of the image (poster)
        that is shown while the video of the episode is downloading or until
        the user hits the play button; this is the representative of the
        episode's video

    @broadcasting_date: The date when this episode has been broadcast
    """
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
        """
        Returns an object Episode


        @payload: a JSON expression contain episode data

        @return: object Episode
        """
        title = payload['title']
        page_url = payload['url']
        image_url = payload['image']
        broadcasting_date = payload['date']
        duration = payload['duration']
        return Episode(title, page_url, image_url, broadcasting_date, duration)

# Waypoint 2: Retrieve the Identification of an Episode
    @staticmethod
    def __parse_episode_id(url):
        """
        Returns the identification of the episode (a string)


        @url: representing the Uniform Resource Locator of the
            image of an episode

        @return: id of an episode (a string)
        """
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
def read_url(url, maximum_attempt_count=3, sleep_duration_between_attempts=1):
    """
    Return data fetched from a HTTP endpoint.


    @param url: A Uniform Resource Locator (URL) that references the
        endpoint to open and read data from.

    @param maximum_attempt_count: Maximal number of failed attempts to
        fetch data from the specified URL before the function raises an
        exception.

    @param sleep_duration_between_attempts: Time in seconds during which
        the current thread is suspended after a failed attempt to fetch
         data from the specified URL, before a next attempt.


    @return: The data read from the specified URL.


    @raise HTTPError: If an error occurs when trying unsuccessfully
        several times to fetch data from the specified URL, print HTTPError
    """
    attempt_count = 0
    while True:
        try:
            attempt_count += 1
            user_agent = 'Mozilla/4.0 (compatible; MSIE 5.5; Windows NT)'

            # set headers for request
            headers = {'User-Agent': user_agent}

            # make a request to server
            req = request.Request(url, headers=headers)
            response = request.urlopen(req)

            # return bytes type
            html = response.read()
            return html

        # catch exception HTTPError - Server side
        except error.HTTPError as e:

            # delay request attempt
            time.sleep(sleep_duration_between_attempts)
            print('continue after 1s..')

            # if attempt = maximum_attempt_count return HTTPError
            if attempt_count == maximum_attempt_count:
                return e
# url = 'http://www.tv5monde.com/emissions/episodes/merci-professeur.json'
# url = 'http://www.tv5monde.com/emissions/episodes/merci-professeur.json?page={}'
# url = 'http://www.fakewebsite.blabla.com'
# print(type(read_url(url))


def fetch_episodes(url):
    """
    Return a list of objects Episode from all pages.


    @url: A Uniform Resource Locator (URL) that references the
        endpoint to open and read data from.

    @return: a list of all objects Episode
    """
    # init list contain objects Episode
    episodes = []

    # check url format
    if 'page' not in url:
        url = url + '?page={}'

    # get numpages
    html = read_url(url.format(1))
    json_data = json.loads(html.decode('utf-8'))
    numpages = json_data['numPages']

# Waypoint 4: Fetch the List of all the Episodes
    # loop though url pages
    for i in range(1, numpages+1):

        # format url then read data returned
        new_url = url.format(i)
        html = read_url(new_url)

        # decode to string then convert to json
        json_data = json.loads(html.decode('utf-8'))
        episodes_data = json_data['episodes']

        # loop though episodes data in 1 page
        for episode_data in episodes_data:

            # append object Episode to list
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
    This function calls the function read_url to read data (bytes) from the
        specified URL, and converts these data (encoded in UTF-8) to a string


    @episode: an object Episode

    @return: HTML content (string) of the episode page
    """

    # read data(bytes) from url
    url = episode.page_url
    html = read_url(url)

    # convert to a string and return
    return html.decode('utf-8')


def parse_broadcast_data_attribute(html_page):
    """
    Returns a JSON expression corresponding to the string value of the
        attribute data-broadcast


    @html_page: a string corresponding to the source code of
        the HTML page of an episode

    @return: JSON expression corresponding to string attribute data-broadcast
    """

    # search line in html_page that contain attribute data-broadcast
    for line in html_page.split('\n'):
        if 'hlstv5mplus-vh.akamaihd.net' in line:
            broadcast_data_line = line

    # string processing to get string value of the attribute data-broadcast
    broadcast_data_line = broadcast_data_line.split("data-broadcast='")[1]
    broadcast_attribute = broadcast_data_line.split("' data-duration")[0]

    # return json expression of the string value
    return json.loads(broadcast_attribute)
# url = 'http://www.tv5monde.com/emissions/episodes/merci-professeur.json'
# episodes = fetch_episodes(url)
# episode = episodes[0]
# html_page = fetch_episode_html_page(episode)
# print(html_page)
# print(parse_broadcast_data_attribute(html_page))


# Waypoint 6: Build a URL Pattern of the Video Segments of an Episode
def build_segment_url_pattern(broadcast_data):
    url_sample = broadcast_data['files'][0]['url']
    url = url_sample.split('master.m3u8')[0] + 'segment{}_3_av.ts?null=0'
    o = urlparse(url)
    return o.scheme + '://' + o.netloc + '/' + o.path
# url = 'http://www.tv5monde.com/emissions/episodes/merci-professeur.json?page={}'
# episodes = fetch_episodes(url)
# print(len(episodes))
# episode = episodes[0]
# print(episode.page_url)
# html_page = fetch_episode_html_page(episode)
# broadcast_data = parse_broadcast_data_attribute(html_page)
# segment_url_pattern = build_segment_url_pattern(broadcast_data)
# print(segment_url_pattern)
# print(segment_url_pattern.format('1'))


# Waypoint 7: Download the Video Segments of an Episode
def download_episode_video_segments(episode, path='./'):
    html_page = fetch_episode_html_page(episode)
    broadcast_data = parse_broadcast_data_attribute(html_page)
    dwn_link = build_segment_url_pattern(broadcast_data)
    episode_id = episode.episode_id
    file_name = 'segment_{}_{}.ts'
    segment_names = []
    segment = 1
    try:
        while 1:
            new_dwn_link = dwn_link.format(segment)
            resp = request.urlopen(new_dwn_link)
            new_file_name = file_name.format(episode_id, segment)
            full_path = os.path.expanduser(path)
            if not os.path.exists(full_path):
                os.mkdir(full_path)
            dump_dir = os.path.join(full_path, new_file_name)
            segment_names.append(dump_dir)
            with open(dump_dir, 'wb') as f:
                f.write(resp.read())
            segment += 1
    except error.HTTPError as e:
        if e.code == 404:
            return segment_names
        else:
            return e
# url = 'http://www.tv5monde.com/emissions/episodes/merci-professeur.json?page={}'
# episodes = fetch_episodes(url)
# episode = episodes[0]
# segment_names = download_episode_video_segments(episode, '~/Music')


# Waypoint 8: Build the Final Video of an Episode
def build_episode_video(episode, segment_file_path_names, path=None):
    """
    """
    file_name = episode.episode_id + '.ts'
    if path is None:
        dirname = os.path.dirname(segment_file_path_names[0])
        dump_dir = os.path.join(dirname, file_name)
    else:
        full_path = os.path.expanduser(path)
        if not os.path.exists(full_path):
            os.mkdir(full_path)
        dump_dir = os.path.join(full_path, file_name)
    with open(dump_dir, 'wb') as f:
        for segment in segment_file_path_names:
            segment_data = open(segment, 'rb')
            content = segment_data.read()
            f.write(content)
    return dump_dir
# url = 'http://www.tv5monde.com/emissions/episodes/merci-professeur.json?page={}'
# episodes = fetch_episodes(url)
# episode = episodes[0]
# segment_names = download_episode_video_segments(episode, '~/Music')
# file_name = build_episode_video(episode, segment_names, path='~/Desktop')
# print(file_name)


# Waypoint 9: Implement a Cache Strategy

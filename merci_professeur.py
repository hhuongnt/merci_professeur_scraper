#!/usr/bin/env python3
import os
import time
import json
from urllib import error, request
from urllib.parse import urlparse

from hashlib import md5

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

    @duration: The duration of an Episode
    """
    def __init__(self, title, page_url, image_url, broadcasting_date, duration):
        """
        Initialize the attributes of an object Episode.
        """
        self.__title = title
        self.__page_url = page_url
        self.__image_url = image_url
        self.__broadcasting_date = broadcasting_date
        self.__duration = duration

        # update constructor and set value for episode id
        self.__episode_id = Episode.__parse_episode_id(self.__image_url)

        # update constructor and set value for episode key
        self.__key = Episode.__generate_key(self.page_url)

    @property
    def title(self):
        """
        Return the value of episode's title.
        """
        return self.__title

    @property
    def page_url(self):
        """
        Return the value of episode's page url
        """
        return 'http://www.tv5monde.com' + self.__page_url

    @property
    def image_url(self):
        """
        Return the value of episode's image url
        """
        return self.__image_url

    @property
    def broadcasting_date(self):
        """
        Return the value of episode's broadcast data
        """
        return self.__broadcasting_date

    @property
    def duration(self):
        """
        Return the value of episode's duration
        """
        return self.__duration

    @staticmethod
    def from_json(payload):
        """
        Returns an object Episode


        @payload: a JSON expression contain episode data

        @return: object Episode
        """

        # set value for episode's title
        title = payload['title']

        # set value for episode's page url
        page_url = payload['url']

        # set value for episode's image url
        image_url = payload['image']

        # set value for episode's broadcast data
        broadcasting_date = payload['date']

        # set value for episode's duration
        duration = payload['duration']

        # return object Episode
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

        # url string processing to get the episode id
        episode_id = os.path.basename(url).split('.')[0]

        # return string id of episode
        return episode_id

    @property
    def episode_id(self):
        """
        Return the value of episode id
        """
        return self.__episode_id

# Waypoint 11: Support Episodes with no Representative Image
    @staticmethod
    def __generate_key(s):
        """
        Returns a string representing the MD5 hexadecimal hash value
        of this argument s.


        @s: a string
        """

        # get the path of the page url
        s = s.split('.com')[1]

        # encode string to bytes and then hash the value
        hash_value = md5(s.encode())

        # return hexadecimal value of hash_value
        return hash_value.hexdigest()

    @property
    def key(self):
        """
        Return the value of episode's hash key
        """
        return self.__key
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
# print(episode.key)


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

    # init count of request attempts
    attempt_count = 0

    while True:
        try:

            # update value of attempt_count
            attempt_count += 1

            # set headers for request
            user_agent = 'Mozilla/4.0 (compatible; MSIE 5.5; Windows NT)'
            headers = {'User-Agent': user_agent}

            # make a request to server
            req = request.Request(url, headers=headers)
            response = request.urlopen(req)

            # return data read from server (bytes type)
            html = response.read()
            return html

        # catch exception HTTPError - Server side
        except error.HTTPError as e:

            # delay request attempt
            time.sleep(sleep_duration_between_attempts)
            print('retry after 1s..')

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

    # check url format and fix
    if 'page' not in url:
        url = url + '?page={}'

    # read the html content (bytes) from the first page
    html = read_url(url.format(1))

    # get json_data from attribute data-broadcast
    json_data = json.loads(html.decode('utf-8'))

    # get numpages from json_data
    numpages = json_data['numPages']

# Waypoint 4: Fetch the List of all the Episodes
    # loop through all url pages
    for i in range(1, numpages+1):

        # format download url
        new_url = url.format(i)

        # read data returned from url (bytes)
        html = read_url(new_url)

        # decode bytes to string and load to json
        json_data = json.loads(html.decode('utf-8'))

        # get data from of attribute 'episode' from json_data
        episodes_data = json_data['episodes']

        # loop through episodes data in 1 page
        for episode_data in episodes_data:

            # append object Episode to list
            episodes.append(Episode.from_json(episode_data))

    # return list of episodes
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

    # get page url from episode
    url = episode.page_url

    # read data (bytes) from url
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
        if 'data-broadcast' in line:
            broadcast_data_line = line

    # string processing to get string value of the attribute data-broadcast
    broadcast_data_line = broadcast_data_line.split("data-broadcast='")[1]
    broadcast_attribute = broadcast_data_line.split("' data-duration")[0]

    # return json expression of the string value
    return json.loads(broadcast_attribute)
# url = 'http://www.tv5monde.com/emissions/episodes/merci-professeur.json'
# episodes = fetch_episodes(url)
# # episode = episodes[0]
# for episode in episodes:
#     html_page = fetch_episode_html_page(episode)
#     # print(html_page)
#     broadcast_data = parse_broadcast_data_attribute(html_page)
#     if broadcast_data['files'][0]['format'] == 'mp4':
#         print(broadcast_data)
#         print(episodes.index(episode))


# Waypoint 6: Build a URL Pattern of the Video Segments of an Episode
def build_segment_url_pattern(broadcast_data):
    """
    Build an URL pattern for accessing the video segments of an episode.


    @broadcast_data: JSON expression corresponding to string value of the
        attribute data-broadcast

    @return: segment url pattern for accessing the video segments
    """

# Waypoint 10: Support Downloading of Old Episodes
    # check file format
    file_format = broadcast_data['files'][0]['format']

    # if format is mp4
    if file_format == 'mp4':

        # get the link to download mp4 video file
        url = broadcast_data['files'][0]['url']

    # if format is m3u8
    else:

        # url pattern get from attribute broadcast_data
        url_sample = broadcast_data['files'][0]['url']

        # create segment url accessing the video segments
        url = url_sample.split('master.m3u8')[0] + 'segment{}_3_av.ts?null=0'

    # parse url to ParseResult
    o = urlparse(url)

    # return url of object ParseResult
    return o.geturl()
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
def download_episode_video_segments(episode, path=os.getcwd()):
    """
    Downloads all the TS video segments of this episode, and
        returns the absolute path and file names of these video
        segments in the order of the segment indices.


    @episode: an object Episode

    @path: a string indicates in with directory the video segment files need
        to be saved into. If not defined, the function saves the video
        segment files in the current working directory.

    @return: a list of absolute path and file names of these video
        segments in the order of the segment indices
    """

    # get episode html page
    html_page = fetch_episode_html_page(episode)

    # get json data of attribute data-broadcast from html page
    broadcast_data = parse_broadcast_data_attribute(html_page)

    # get download pattern
    dwn_link = build_segment_url_pattern(broadcast_data)

    # get episode_id
    episode_id = episode.episode_id

# Waypoint 11: Support Episodes with no Representative Image
    if episode_id == '':
        episode_id = episode.key

    # init file_name pattern if format is m3u8
    file_name = 'segment_{}_{}.ts'

    # get full path
    full_path = os.path.expanduser(path)

    # check path exists if not create path
    if not os.path.isdir(full_path):
        os.mkdir(full_path)

    # init list of the absolute path and file names of these video segments
    segment_names = []

    # segment index
    segment_index = 1

# Waypoint 10: Support Downloading of Old Episodes
    # get file_format
    format = broadcast_data['files'][0]['format']

    # init file name if format is mp4
    if format == 'mp4':
        file_name = episode_id + '.mp4'

    try:
        while True:

            # format file_name according to segment_index
            new_file_name = file_name.format(episode_id, segment_index)

            # create destination directory to save the video segments
            dump_dir = os.path.join(full_path, new_file_name)

# Waypoint 9: Implement a Cache Strategy
            # if file downloaded pass
            if os.path.isfile(dump_dir):
                print(dump_dir + ' downloaded')

            # if file is not downloaded
            else:

                # format download link according to segment_index
                new_dwn_link = dwn_link.format(segment_index)

                # make a request
                resp = request.urlopen(new_dwn_link)

                # download the video segment by writing content (bytes) to file
                print('Downloading ' + dump_dir)
                with open(dump_dir, 'wb') as f:
                    f.write(resp.read())

            # append absolute path and file names of segments to list
            segment_names.append(dump_dir)

            # update value of segment_index
            segment_index += 1

# Waypoint 10: Support Downloading of Old Episodes
            # if format is mp4 return the video
            if format == 'mp4':
                return segment_names

    # handle HTTPError
    except error.HTTPError as e:

        # return list if there's no more video segment to download
        if e.code == 404:
            return segment_names
        # return HTTPError if there is problem downloading
        else:
            return e
# url = 'http://www.tv5monde.com/emissions/episodes/merci-professeur.json?page={}'
# episodes = fetch_episodes(url)
# episode = episodes[0]
# (wp10)
# episode = episodes[280]
# segment_names = download_episode_video_segments(episode, path='~/Movies')
# print(segment_names)


# Waypoint 8: Build the Final Video of an Episode
def build_episode_video(episode, segment_file_path_names, path=None):
    """
    The function assembles all these video segments in one video named
        after the identification of the episode and returns the
        absolute path and file name of the episode's video.


    @episode: an object Episode

    @segment_file_path_names: a list of strings corresponding to
        absolute path and file names of TS video segments in the
        order of their index.

    @path: a string indicates in with directory the episode's video file
        need to be saved into. If not defined, the function saves the
        episode video file in the path identified by the first video segment.

    @return: the absolute path and file name of the episode's video.
    """
    # get episode_id
    episode_id = episode.episode_id

# Waypoint 11: Support Episodes with no Representative Image
    if episode_id == '':
        episode_id = episode.key

    # init file_name if format is m3u8
    file_name = episode_id + '.ts'

# Waypoint 10: Support Downloading of Old Episodes
    # init file_name if format is mp4
    if len(segment_file_path_names) == 1:
        file_name = os.path.basename(segment_file_path_names[0])

    # if path is not input, set path = dirname of the first segment
    if path is None:
        path = os.path.dirname(segment_file_path_names[0])

    # if path is input
    else:

        # get the full path
        path = os.path.expanduser(path)

        # check path exists if not create path
        if not os.path.exists(path):
            os.mkdir(path)

    # combine path and file_name to create saved destination
    dump_dir = os.path.join(path, file_name)

    # if dump directory is the same as the folder contain mp4 video
    if dump_dir == segment_file_path_names[0]:

        # return the absolute path and file name of the episode's video
        return dump_dir

    # assembles all segments by writing file content (bytes) to a new file
    with open(dump_dir, 'wb') as f:

        # loop through each file in the list
        for segment in segment_file_path_names:

            # open file to read (bytes)
            segment_data = open(segment, 'rb')
            content = segment_data.read()

            # write content (bytes) to the new file
            f.write(content)

    # return the absolute path and file name of the episode's video
    return dump_dir
# url = 'http://www.tv5monde.com/emissions/episodes/merci-professeur.json?page={}'
# episodes = fetch_episodes(url)
# episode = episodes[0]
# episode = episodes[280]
# segment_names = download_episode_video_segments(episode, path='~/Music')
# file_name = build_episode_video(episode, segment_names, path='~/Desktop')
# print(file_name)

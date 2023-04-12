import os
from dotenv import load_dotenv
from googleapiclient.discovery import build
from urllib.parse import urlparse, parse_qs
import re

class YoutubeToolkit:
    def __init__(self):
        load_dotenv("api_keys.env")
        youtube_api_key = os.getenv("YOUTUBE_API_KEY")
        self.youtube = build('youtube', 'v3', developerKey='AIzaSyBT8_vAimPTyXuCT-Xlr4xutKzalEGm0Hg')
        
    def verify_comments_enabled(self, video_id):
        try:
            comment_response = self.youtube.commentThreads().list(
                part='snippet',
                videoId=video_id,
                maxResults=100
            ).execute()
            return True
        except:
            return False

    # Verifies the link provided is from YouTube
    def verify_url(self, url):
        """
        # Isolate the domain and verify youtube.com or youtu.be
        parsed_url = urlparse(url)
        domain = parsed_url.netloc
        if not (domain.endswith('youtube.com') or domain == 'youtu.be'):
            return False
        return True
        ----------------------------------------------------------------------------------------------------------------
        NOTES:
        print(urlparse('https://www.youtube.com/watch?v=3')) = ParseResult(scheme='https', netloc='www.youtube.com', path='/watch', params='', query='v=3', fragment='')
        print(urlparse('www.youtube.com/watch?v=p44HlRMSKf8')) = ParseResult(scheme='', netloc='', path='www.youtube.com/watch', params='', query='v=p44HlRMSKf8', fragment='')
        print(urlparse('youtube.com/watch?v=3')) = ParseResult(scheme='', netloc='', path='youtube.com/watch', params='', query='v=3', fragment='')
        print(urlparse('youtu.be/p44HlRMSKf8')) = ParseResult(scheme='', netloc='', path='youtu.be/p44HlRMSKf8', params='', query='', fragment='')

        * Does not pass the case where HTTPS is not present -> Thus, the link becomes stored in path instead of netloc
        * Does not verify that the link is properly formatted with the essential pieces
        EX:
        1. youtube.com/watch?v={11 random string)
        2. youtu.be/{11 random string}

        Is all we really need I believe
        """
        if re.search('(https:\/\/)?(www\.)?youtube\.com\/watch\?v=[a-zA-Z0-9\-\_]{11}$|(https:\/\/)?(www\.)?youtu\.be\/[a-zA-Z0-9\-\_]{11}', url):
            return True
        return False

    # Gets video name from video id
    def get_video_name(self, url):
        parsed_url = urlparse(url)
        video_id = self.get_video_id(parsed_url)
        video_response = self.youtube.videos().list(
            part='snippet',
            id=video_id
        ).execute()
        return video_response['items'][0]['snippet']['title']

    # Gets video ID from parsed URL
    def get_video_id(self, parsed_url):
        video_id = ''
        if parsed_url.netloc == 'youtu.be':
            video_id = parsed_url.path[1:]
        if parsed_url.netloc.endswith('youtube.com'):
            query = parse_qs(parsed_url.query)
            video_id = query['v'][0]
        return video_id

    # Returns a list of comments in array format

    """
    * API HERE: https://developers.google.com/youtube/v3/docs/search/list
    * The REQUEST and RESPONSE model acts similar to a page.
    * Therefore, the RESPONSE gives back it back in a format such that properties of the page search is listed initially
        and then the VIDEOS are contained in an ARRAY of the list items.
        
    * ASSUMES topic is a STRING
    * The 'q' parameter is determines search topic
    """

    def get_topic_list(self, topic):
        api_request = self.youtube.search().list(part='snippet', order='relevance', q=topic, type='video',
                                                 relevanceLanguage='en', maxResults=5)
        response_list = api_request.execute()

        # The INDEXES should correspond
        videos_title_arr = []
        videos_id_arr = []
        videos_link_arr = []
        for video in response_list['items']:
            videos_title_arr.append(video['snippet']['title'])  # Grabs the TITLE
            videos_id_arr.append(video['id']['videoId']) # Grabs the VID ID

        for video_id in videos_id_arr: # These are for the links
            videos_link_arr.append("https://www.youtube.com/watch?v="+video_id)
        #print(videos_title_arr)
        #print(videos_id_arr)
        #print(videos_link_arr)
        return videos_link_arr, videos_title_arr

    def comment_finder(self, url):
        # Parse the URL using URLParse
        parsed_url = urlparse(url)
        # Verify URL is YouTube link
        if not self.verify_url(url):
            print("Error trying to verify URL is YouTube link")
            return

        video_id = self.get_video_id(parsed_url)

        video_response = self.youtube.videos().list(
            part='snippet',
            id=video_id
        ).execute()

        # Verify that a video is found
        if video_response['pageInfo']['totalResults'] == 0 or video_response['items'][0]['kind'] != 'youtube#video':
            print("Video not found given ID")
            return

        try:
            comment_response = self.youtube.commentThreads().list(
                part='snippet',
                videoId=video_id,
                maxResults=100
            ).execute()
        except:
            print("Creator disabled comment scraping on this video")
            return



        # Verify that there are comments under video
        if comment_response['pageInfo']['totalResults'] == 0:
            print("No comments found")
            return

        comment_array = []

        for comment_thread in comment_response['items']:
            comment_array.append(comment_thread['snippet']['topLevelComment']['snippet']['textOriginal'])

        return comment_array


if __name__ == '__main__':
    print(urlparse('https://www.youtube.com/watch?v=3'))
    print(urlparse('www.youtube.com/watch?v=p44HlRMSKf8'))
    print(urlparse('youtube.com/watch?v=3'))
    print(urlparse('youtu.be/p44HlRMSKf8'))
    yt = YoutubeToolkit()
    yt.get_topic_list('dog')
    print(yt.get_video_name("https://www.youtube.com/watch?v=YCzgnzWK_r0"))
    print(urlparse('https://youtu.be/p44HlRMSKf8'))

import os
from dotenv import load_dotenv
from googleapiclient.discovery import build
from urllib.parse import urlparse, parse_qs

class CommentFinder:
    def __init__(self):
        load_dotenv()
        youtube_api_key = os.getenv("YOUTUBE_API_KEY")
        self.youtube = build('youtube', 'v3', developerKey=youtube_api_key)
    
    # Verifies the link provided is from YouTube
    def verify_url(self, parsed_url):        
        # Isolate the domain and verify youtube.com or youtu.be
        domain = parsed_url.netloc
        if not (domain.endswith('youtube.com') or domain == 'youtu.be'):
            return False
        return True
    
    # Gets video ID from parsed URL
    def get_video_id(self, parsed_url):
        video_id = ''
        if parsed_url.netloc == 'youtu.be':
            video_id = parsed_url.path[1:]
        if parsed_url.netloc.endswith('youtube.com'):
            query = parse_qs(parsed_url.query)
            video_id = query['v'][0]
        return video_id
        
    # Retruns a list of comments in array format
    def comment_finder(self, url):
        # Parse the URL using URLParse
        parsed_url = urlparse(url)
        
        # Verify URL is YouTube link
        if not self.verify_url(parsed_url):
            print("Error trying to verify URL is YouTube link")
            return
        
        video_id = self.get_video_id(parsed_url)
        
        video_response =  self.youtube.videos().list(
            part='snippet',
            id=video_id
        ).execute()
        
        # Verify that a video is found
        if video_response['pageInfo']['totalResults'] == 0 or video_response['items'][0]['kind'] != 'youtube#video':
            print("Video not found given ID")
            return
        
        comment_response = self.youtube.commentThreads().list(
            part='snippet',
            videoId=video_id,
            maxResults=100
        ).execute()
               
        # Verify that there are comments under video
        if comment_response['pageInfo']['totalResults'] == 0:
            print("No comments found")
            return
                
        comment_array = []
        
        for comment_thread in comment_response['items']:
            comment_array.append(comment_thread['snippet']['topLevelComment']['snippet']['textOriginal'])
            
        print(comment_array)
        return comment_array
        
if __name__ == '__main__':
    cf = CommentFinder()
    cf.comment_finder("https://www.youtube.com/watch?v=YUVf0AFkn1Y")
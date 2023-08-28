
import argparse
from googleapiclient.discovery import build
from googleapiclient.errors import HttpError
from config import config
from pprint import pprint
# Set DEVELOPER_KEY to the API key value from the APIs & auth > Registered apps
# tab of
#   https://cloud.google.com/console
# Please ensure that you have enabled the YouTube Data API for your project.
DEVELOPER_KEY =  config.get_api_key()
YOUTUBE_API_SERVICE_NAME = 'youtube'
YOUTUBE_API_VERSION = 'v3'

def youtube_search(options):
  youtube = build(YOUTUBE_API_SERVICE_NAME, YOUTUBE_API_VERSION,
    developerKey=DEVELOPER_KEY)

  # Call the search.list method to retrieve results matching the specified
  # query term.
  search_response = youtube.search().list(
    q=options.q,
    part='id,snippet',
    maxResults=options.max_results
  ).execute()

  videos = []
  channels = []
  playlists = []

  # Add each result to the appropriate list, and then display the lists of
  # matching videos, channels, and playlists.
  for search_result in search_response.get('items', []):
    if search_result['id']['kind'] == 'youtube#video':
      doc = {
        "videoTitle":search_result['snippet']['title'],
        "videoID":search_result['id']['videoId']
      }
      videos.append(doc)
      # videos.append('%s (%s)' % (search_result['snippet']['title'],
      #                            search_result['id']['videoId']))
    # pprint(search_result['snippet'])
  return videos
    

def get_description(video_list):
  youtube = build(YOUTUBE_API_SERVICE_NAME, YOUTUBE_API_VERSION,
    developerKey=DEVELOPER_KEY)
#   print('Videos:\n', '\n'.join(videos), '\n')
  response = youtube.videos().list(
    part='snippet',
    id=video_id
  ).execute()
  if 'items' in response and len(response['items']) > 0:
    video = response['items'][0]
    video_title = video['snippet']['title']
    video_description = video['snippet']['description']
    print('-'*30)
    print(video_title)
    print(video_description)


if __name__ == '__main__':
  parser = argparse.ArgumentParser()
  parser.add_argument('--q', help='Search term', default='kms tools download')
  parser.add_argument('--max-results', help='Max results', default=10)
  args = parser.parse_args()

  try:
    videos = youtube_search(args)
    
  except HttpError as e:
    print ('An HTTP error %d occurred:\n%s' % (e.resp.status, e.content))
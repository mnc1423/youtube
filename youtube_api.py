from config import config
import argparse
from googleapiclient.discovery import build
from googleapiclient.errors import HttpError
import re
from urlextract import URLExtract
import hashlib
from elastic_handler import esHandler


class Youtube_API:
    def __init__(self):
        DEVELOPER_KEY = config.get_api_key()
        YOUTUBE_API_SERVICE_NAME = "youtube"
        YOUTUBE_API_VERSION = "v3"
        self.youtube = build(
            YOUTUBE_API_SERVICE_NAME, YOUTUBE_API_VERSION, developerKey=DEVELOPER_KEY
        )
        parser = argparse.ArgumentParser()
        parser.add_argument("--q", help="Search term", default="vegas pro crack")
        parser.add_argument("--max-results", help="Max results", default=50)
        self.args = parser.parse_args()
        self.extractor = URLExtract()
        self.published_after_date = "2023-01-01T00:00:00Z"

        # self.url_regex = re.compile("^[-a-zA-Z0-9@:%._\\+~#=]{1,256}\\.[a-zA-Z0-9()]{1,6}\\b(?:[-a-zA-Z0-9()@:%_\\+.~#?&\\/=]*)$")

    def youtube_search(self):
        videos = []
        next_page_token = None
        total_res = 0
        while True:
            search_response = (
                self.youtube.search()
                .list(
                    q=self.args.q,
                    part="id,snippet",
                    maxResults=self.args.max_results,
                    publishedAfter=self.published_after_date,
                    pageToken=next_page_token,
                )
                .execute()
            )
            # matching videos, channels, and playlists.
            for search_result in search_response.get("items", []):
                if search_result["id"]["kind"] == "youtube#video":
                    doc = {
                        "vid_title": search_result["snippet"]["title"],
                        "videoID": search_result["id"]["videoId"],
                        "publishedAt": search_result["snippet"]["publishedAt"],
                        "channelTitle": search_result["snippet"]["channelTitle"],
                        "channelId": search_result["snippet"]["channelId"],
                    }
                    videos.append(doc)
            total_res += len(search_response.get("items", []))
            next_page_token = search_response.get("nextPageToken")

            if not next_page_token:
                break
        print(f"Total Videos:{total_res}")
        return videos

    def get_description(self, video_list):
        for docs in video_list:
            response = (
                self.youtube.videos().list(part="snippet", id=docs["videoID"]).execute()
            )
            if "items" in response and len(response["items"]) > 0:
                video = response["items"][0]
                video_description = video["snippet"]["description"]
                # docs["description"] = video_description
                url_list = self.get_url_pattern(video_description)
                docs["url_list"] = url_list

        return video_list

    def get_url_pattern(self, line):
        url_list = self.extractor.find_urls(line)
        return url_list


if __name__ == "__main__":
    a = Youtube_API()
    video_list = a.youtube_search()
    # Get description
    descp_list = a.get_description(video_list)
    es_handler = esHandler()
    es_inputList = []
    for docs in descp_list:
        _id = hashlib.sha1(docs["videoID"].encode()).hexdigest()
        docs["_id"] = _id
        es_inputList.append(es_handler.create_doc(docs))
    es_handler.esInput(es_inputList)

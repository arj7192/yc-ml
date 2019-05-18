#!/usr/bin/python

# Usage:
# python scraper.py --videoid='<video_id>'

from apiclient.errors import HttpError
# import argparser
from apiclient.discovery import build

YOUTUBE_API_SERVICE_NAME = "youtube"
YOUTUBE_API_VERSION = "v3"
DEVELOPER_KEY = 'AIzaSyDyq3nr2KjbFME9EeNpHy97AX87vk75H_Y'


def get_comment_threads(youtube, video_id, comments):
    threads = []
    results = youtube.commentThreads().list(
        part="snippet",
        videoId=video_id,
        textFormat="plainText",
    ).execute()

    # Get the first set of comments
    for item in results["items"]:
        threads.append(item)
        comment = item["snippet"]["topLevelComment"]
        text = comment["snippet"]["textDisplay"]
        comments.append(text)

    # Keep getting comments from the following pages
    while ("nextPageToken" in results):
        results = youtube.commentThreads().list(
            part="snippet",
            videoId=video_id,
            pageToken=results["nextPageToken"],
            textFormat="plainText",
        ).execute()
    for item in results["items"]:
        threads.append(item)
        comment = item["snippet"]["topLevelComment"]
        text = comment["snippet"]["textDisplay"]
        comments.append(text)

    print("Total threads: %d" % len(threads))
    return threads


def get_comments(youtube, parent_id, comments):
    results = youtube.comments().list(
        part="snippet",
        parentId=parent_id,
        textFormat="plainText"
    ).execute()

    for item in results["items"]:
        text = item["snippet"]["textDisplay"]
        comments.append(text)

    return results["items"]


if __name__ == "__main__":
    argparser.add_argument("--videoid", help="Required; ID for video for which the comment will be inserted.")
    args = argparser.parse_args()
    youtube = build(YOUTUBE_API_SERVICE_NAME, YOUTUBE_API_VERSION, developerKey=DEVELOPER_KEY)

    comments = []

    try:
        video_comment_threads = get_comment_threads(youtube, args.videoid, comments)
        for thread in video_comment_threads:
            get_comments(youtube, thread["id"], comments)
    except(HttpError, e):
        print("An HTTP error %d occurred:\n%s" % (e.resp.status, e.content))

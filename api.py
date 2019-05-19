import json

from flask import Flask, request, Response, send_file
from yc import *
from word_count import *
from topic_modelling import *
from sentiment_analysis import *

app = Flask(__name__)


@app.route('/comments/wc/<video_id>', methods=['GET'])
def get_wc_api(video_id):
    """
    """
    youtube = build(YOUTUBE_API_SERVICE_NAME, YOUTUBE_API_VERSION, developerKey=DEVELOPER_KEY)
    comments = []
    video_comment_threads = get_comment_threads(youtube, video_id, comments)
    for thread in video_comment_threads:
        get_comments(youtube, thread["id"], comments)

    return get_word_count(comments)


@app.route('/comments/tm/<video_id>', methods=['GET'], )
def get_tm_api(video_id):
    """
    """
    ngram = int(request.args.get('ngram', default=1))
    youtube = build(YOUTUBE_API_SERVICE_NAME, YOUTUBE_API_VERSION, developerKey=DEVELOPER_KEY)
    comments = []
    video_comment_threads = get_comment_threads(youtube, video_id, comments)
    for thread in video_comment_threads:
        get_comments(youtube, thread["id"], comments)

    return get_topics_ngram(comments, ngram=ngram)


@app.route('/comments/sa/<video_id>', methods=['GET'], )
def get_sa_api(video_id):
    """
    """
    youtube = build(YOUTUBE_API_SERVICE_NAME, YOUTUBE_API_VERSION, developerKey=DEVELOPER_KEY)
    comments = []
    video_comment_threads = get_comment_threads(youtube, video_id, comments)
    for thread in video_comment_threads:
        get_comments(youtube, thread["id"], comments)

    return get_sentiment_analysis(comments)


if __name__ == '__main__':
    app.run(
        host="0.0.0.0",
        port=int("8089"),
        debug=True
    )

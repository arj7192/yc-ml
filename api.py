import json

from flask import Flask, request, Response, send_file
from yc import *
from word_count import *

app = Flask(__name__)

@app.route('/comments/<video_id>', methods=['GET'])
def get_comments_api(video_id):
    """
    """
    youtube = build(YOUTUBE_API_SERVICE_NAME, YOUTUBE_API_VERSION, developerKey=DEVELOPER_KEY)
    comments = []
    video_comment_threads = get_comment_threads(youtube, video_id, comments)
    for thread in video_comment_threads:
        get_comments(youtube, thread["id"], comments)

    return get_word_count(comments)


if __name__ == '__main__':
    app.run(
        host="0.0.0.0",
        port=int("8089"),
        debug=True
    )

# http://www.nltk.org/howto/sentiment.html

from nltk.sentiment.vader import SentimentIntensityAnalyzer
from nltk import tokenize
import json
import numpy as np


def get_sentiment_analysis(list_of_comments):
    processed_list_of_comments = [tokenize.sent_tokenize(comment) for comment in list_of_comments]
    processed_list_of_comments = [k for j in processed_list_of_comments for k in j]
    sid = SentimentIntensityAnalyzer()
    scores = {'compound': [], 'neg': [], 'neu': [], 'pos': []}
    for sentence in processed_list_of_comments:
        print(sentence)
        ss = sid.polarity_scores(sentence)
        for k in sorted(ss):
            scores[k] += [ss[k]]
    for k in scores:
        scores[k] = {'mean': np.round(np.mean(scores[k]), 2), 'std': np.round(np.std(scores[k]), 2)}
    return json.dumps(scores)

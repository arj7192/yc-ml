import json
from nltk.stem import WordNetLemmatizer
from collections import Counter
from textblob import TextBlob


def get_word_count(list_of_comments, k=20):
    wordnet_lemmatizer = WordNetLemmatizer()
    comment_noun_phrases = [wordnet_lemmatizer.lemmatize(comment_word) for comment in list_of_comments
                            for comment_word in TextBlob(comment).noun_phrases]
    to_return = dict(sorted(dict(Counter(comment_noun_phrases)).items(),
                       key = lambda c: c[1], reverse=True)[:k])
    return json.dumps(to_return)

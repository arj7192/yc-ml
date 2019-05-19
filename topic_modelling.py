import json
import string

from spacy.lang.en import English
from sklearn.decomposition import NMF, LatentDirichletAllocation, TruncatedSVD
from sklearn.feature_extraction.text import CountVectorizer
from spacy.lang.en.stop_words import STOP_WORDS

# current limitation : only english language support
parser = English()
stopwords = list(STOP_WORDS)
punctuations = string.punctuation


# Functions for printing keywords for each topic
def selected_topics(model, vectorizer, num_topics=5):
    return [[(vectorizer.get_feature_names()[i], topic[i]) for i in topic.argsort()[:-num_topics - 1:-1]]
            for idx, topic in enumerate(model.components_)]


def spacy_tokenizer(sentence):
    # Parser for reviews
    mytokens = parser(sentence)
    mytokens = [word.lemma_.lower().strip() if word.lemma_ != "-PRON-" else word.lower_ for word in mytokens ]
    mytokens = [word for word in mytokens if word not in stopwords and word not in punctuations ]
    mytokens = " ".join([i for i in mytokens])
    return mytokens


def lsi(data_vectorized, topic_length=5):
    # Latent Semantic Indexing Model using Truncated SVD
    lsi = TruncatedSVD(n_components=topic_length)
    data_lsi = lsi.fit_transform(data_vectorized)
    return lsi


def lda(data_vectorized, topic_length=5):
    # Latent Dirichlet Allocation Model
    lda = LatentDirichletAllocation(n_components=topic_length, max_iter=10, learning_method='online', verbose=True)
    data_lda = lda.fit_transform(data_vectorized)
    return lda


def spacy_bigram_tokenizer(phrase):
    doc = parser(phrase)  # create spacy object
    token_not_noun = []
    notnoun_noun_list = []
    noun = ""

    for item in doc:
        if item.pos_ != "NOUN":  # separate nouns and not nouns
            token_not_noun.append(item.text)
        if item.pos_ == "NOUN":
            noun = item.text

        for notnoun in token_not_noun:
            notnoun_noun_list.append(notnoun + " " + noun)

    return " ".join([i for i in notnoun_noun_list])


def get_topics_ngram(list_of_comments, ngram=1, topic_length=5, num_topics=5):
    # Creating a vectorizer
    if ngram == 1:
        processed_list_of_comments = [spacy_tokenizer(comment) for comment in list_of_comments]
        vectorizer = CountVectorizer(stop_words='english', lowercase=True, token_pattern='[a-zA-Z\-][a-zA-Z\-]{2,}')
        data_vectorized = vectorizer.fit_transform(processed_list_of_comments)
    elif ngram == 2:
        processed_list_of_comments = [spacy_bigram_tokenizer(comment) for comment in list_of_comments]
        vectorizer = CountVectorizer(stop_words='english', lowercase=True, ngram_range=(1, 2))
        data_vectorized = vectorizer.fit_transform(processed_list_of_comments)
    # Choose topic model
    topic_model = lda(data_vectorized, topic_length)
    # topic_model = lsi(data_vectorized)
    to_return = selected_topics(topic_model, vectorizer, num_topics)
    return json.dumps(to_return)

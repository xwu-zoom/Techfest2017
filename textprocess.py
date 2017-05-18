#!/usr/bin/python

import nltk
# nltk.download('stopwords')
import json
import re
from nltk.tokenize import word_tokenize
import operator
from collections import Counter
from nltk.corpus import stopwords
import string
from nltk import bigrams

import vincent

# Regex
emoticons_str = r"""
    (?:
        [:=;] # Eyes
        [oO\-]? # Nose (optional)
        [D\)\]\(\]/\\OpP] # Mouth
    )"""

regex_str = [
    emoticons_str,
    r'<[^>]+>', # HTML tags
    r'(?:@[\w_]+)', # @-mentions
    r"(?:\#+[\w_]+[\w\'_\-]*[\w_]+)", # hash-tags
    r'http[s]?://(?:[a-z]|[0-9]|[$-_@.&amp;+]|[!*\(\),]|(?:%[0-9a-f][0-9a-f]))+', # URLs

    r'(?:(?:\d+,?)+(?:\.?\d+)?)', # numbers
    r"(?:[a-z][a-z'\-_]+[a-z])", # words with - and '
    r'(?:[\w_]+)', # other words
    r'(?:\S)' # anything else
]

tokens_re = re.compile(r'('+'|'.join(regex_str)+')', re.VERBOSE | re.IGNORECASE)
emoticon_re = re.compile(r'^'+emoticons_str+'$', re.VERBOSE | re.IGNORECASE)

# stopwords
punctuation = list(string.punctuation)
stop = stopwords.words('english') + punctuation + ['rt', 'via']

# functions
def tokenize(s):
    return tokens_re.findall(s)

def preprocess(s, lowercase=False):
    tokens = tokenize(s)
    if lowercase:
        tokens = [token if emoticon_re.search(token) else token.lower() for token in tokens]
    return tokens

# main
with open('data/crawl_Zoominfo.json', 'r') as f:
    count_all = Counter()
    for line in f:
        tweet = json.loads(line) # load it as Python dict
        terms_stop_filter = [term for term in preprocess(tweet['text']) if term not in stop]
        count_all.update(terms_stop_filter)
        # print(json.dumps(tweet["text"], indent=4)) # pretty-print
        # tokens = preprocess(tweet['text'])

        # Count terms only once, equivalent to Document Frequency
        terms_single = set(terms_stop_filter)
        # Count hashtags only
        terms_hash = [term for term in preprocess(tweet['text'])
                      if term.startswith('#')]
        terms_mention = [term for term in preprocess(tweet['text'])
                      if term.startswith('@')]
        # Count terms only (no hashtags, no mentions)
        terms_only = [term for term in preprocess(tweet['text'])
                      if term not in stop and
                      not term.startswith(('#', '@'))]
                      # mind the ((double brackets))
                      # startswith() takes a tuple (not a list) if
                      # we pass a list of inputs
        terms_bigram = bigrams(terms_stop_filter)

    print(count_all.most_common(5))
        # tweet = 'RT @marcobonzanini: just an example! :D http://example.com #NLP'
        # print(preprocess(tweet))

    # visualization
    word_freq = count_all.most_common(20)
    labels, freq = zip(*word_freq)
    data = {'data': freq, 'x': labels}
    bar = vincent.Bar(data, iter_idx='x')
    bar.to_json('term_freq.json', html_out=True, html_path='chart.html')

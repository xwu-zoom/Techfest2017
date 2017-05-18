#!/usr/bin/python


import tweepy
from tweepy import OAuthHandler
from tweepy import Stream
from tweepy.streaming import StreamListener

import time
import argparse
import string
import twauth
import json

# parser
def get_parser():

    parser = argparse.ArgumentParser(description="Twitter Downloader")
    parser.add_argument("-u",
                        "--user",
                        dest="user",
                        help="UID/Filter",
                        default='-')
    parser.add_argument("-d",
                        "--data-dir",
                        dest="data_dir",
                        help="Output/Data Directory")
    return parser


def process_or_store(tweet):
    # print(json.dumps(tweet))
    user_fname = format_filename(args.user)
    outfile = "%s/crawl_%s.json" % (args.data_dir, user_fname)
    # f.write(json.dumps(status._json)+"\n")

    with open(outfile, 'a') as f:
        f.write(json.dumps(tweet)+"\n")
        print(json.dumps(tweet)+"\n")


def format_filename(fname):
    """Convert file name into a safe string.
    Arguments:
        fname -- the file name to convert
    Return:
        String -- converted file name
    """
    return ''.join(convert_valid(one_char) for one_char in fname)


def convert_valid(one_char):
    """Convert a character into '_' if invalid.
    Arguments:
        one_char -- the char to convert
    Return:
        Character -- converted char
    """
    valid_chars = "-_.%s%s" % (string.ascii_letters, string.digits)
    if one_char in valid_chars:
        return one_char
    else:
        return '_'


@classmethod
def parse(cls, api, raw):
    status = cls.first_parse(api, raw)
    setattr(status, 'json', json.dumps(raw))
    return status

if __name__ == '__main__':
    parser = get_parser()
    args = parser.parse_args()
    auth = OAuthHandler(twauth.consumer_key, twauth.consumer_secret)
    auth.set_access_token(twauth.access_token, twauth.access_secret)
    api = tweepy.API(auth)
    # print("api auth succeed")

    for tweet in tweepy.Cursor(api.user_timeline, id=args.user).items(100):
        process_or_store(tweet._json)
    # print("ok")


# for status in tweepy.Cursor(api.home_timeline).items(10):
#     # Process a single status
#     process_or_store(status._json)
#
# for friend in tweepy.Cursor(api.friends).items():
#     process_or_store(friend._json)

# for tweet in tweepy.Cursor(api.user_timeline, id="Zoominfo").items():
#     process_or_store(tweet._json)

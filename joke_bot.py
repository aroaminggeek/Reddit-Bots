#!/usr/bin/env python
import praw
import time
import os
import requests

joke = requests.get(
    'http://api.icndb.com/jokes/random').json()['value']['joke']
REPLY_MESSAGE = ('Here\'s your Chuck Norris joke:\n\n'
                 '>' + joke +
                 '\n\nThis joke came from'
                 ' [The Internet Chuck Norris Database](http://www.icndb.com)'
                 )


def authenticate():
    print('Authenticating...')
    reddit = praw.Reddit('ARGbot')
    print('Authenticated as {}'.format(reddit.user.me()))

    return reddit


def get_saved_comments():
    if not os.path.isfile('comments_replied_to.txt'):
        comments_replied_to = []
    else:
        with open('comments_replied_to.txt', 'r') as f:
            comments_replied_to = f.read()
            comments_replied_to = comments_replied_to.split('\n')

    return comments_replied_to


def main():
    reddit = authenticate()
    comments_replied_to = get_saved_comments()

    while True:
        run_bot(reddit, comments_replied_to)


def run_bot(reddit, comments_replied_to):
    print('getting 10 comments')

    for comment in reddit.subreddit('ARGBot_test').comments(limit=50):
        if '!joke' in comment.body and comment.id not in comments_replied_to and comment.author != reddit.user.me():

            comment.reply(REPLY_MESSAGE)

            print('Replied to ' + comment.id)

            comments_replied_to.append(comment.id)

            with open('comments_replied_to.txt', 'a') as f:
                f.write(comment.id + '\n')

    print('Sleeping for 10 seconds')

    # sleep for 10 seconds
    time.sleep(10)


if __name__ == '__main__':
    main()

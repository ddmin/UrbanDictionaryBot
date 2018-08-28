from bs4 import BeautifulSoup
import requests
import praw
import config
import time
from UrbDicBot import *

def authenticate():
    print("Authenticating UrbanDictBot...")
    reddit = praw.Reddit(username = config.username,
                         password = config.password,
                         client_id = config.client_id,
                         client_secret = config.client_secret,
                         user_agent = "ddmin's UrbanDicBot v1.2")
    print("Authenticated!\n")
    return reddit

def run_bot(reddit, comment_id):
    print("Obtaining 25 comments...\n")
    for comment in reddit.subreddit('test').comments(limit=25):
        if "!UrbanDictBot " in comment.body and comment.id not in comment_id and str(comment.body)[0:13] == '!UrbanDictBot':
            word = str(comment.body)[14:]
            print(f'Found word "{word}" in {comment.id}')
            definition = word_lookup(word)
            source = 'https://www.urbandictionary.com/define.php?term='+word
            comment.reply(f"#**{word.capitalize()}**:\n\n**Definition**: *{definition}*\n\n[Source]({source})\n\n***\n\n^(Bleep-bloop, This action was performed by a bot.)")
            print("Replied to comment " + comment.id)

            with open("replied_to.txt", "a") as f:
                f.write(comment.id + "\n")
                
        if '!UrbanDictBot' in comment.body and comment.id not in comment_id and str(comment.body)[0:13] != '!UrbanDictBot' and comment.author != reddit.user.me():
            comment.reply('If you want to summon me make sure nothing comes before "!UrbanDictBot" in your comment. Blame my human for this inconvenience.\n\n***\n\n^(Bleep-bloop, This action was performed by a bot.)')
            print("Replied to comment " + comment.id)
            with open("replied_to.txt", "a") as f:
                f.write(comment.id + "\n")
                
def get_ids():
    with open("replied_to.txt", "r") as f:
        replied_to = f.read()
        replied_to = replied_to.split("\n")
    return replied_to

reddit = authenticate()

while True:
    try:
        comment_id = get_ids()
        run_bot(reddit, comment_id)
    except:
        print('Error. Sleeping for 30 seconds\n')
        time.sleep(30)
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
                         user_agent = "ddmin's UrbanDicBot v1.7")
    print("Authenticated!\n")
    return reddit

def run_bot(reddit, comment_id):
    print("Obtaining 25 comments...\n")
    for comment in reddit.subreddit('test').comments(limit=25):
                
        if "!UrbanDictBot " in comment.body and comment.id not in comment_id:
            word_list = str(comment.body).split()
            for n in range(len(word_list)):
                if word_list[n] == '!UrbanDictBot':
                    break
                
            word = ''
            for item in word_list[n+1:]:
                word += item
                if item != word_list[-1]:
                    word += ' '
            print(f'Found word "{word}" in {comment.id}')

            try:
                definition = word_lookup(word)
            except:
                comment.reply('I can\'t find that word on Urban Dictionary.\n\n***\n\n^(Bleep-bloop. I am a bot. | [Github](https://github.com/ddmin/UrbanDictionaryBot))')
                print("Replied to comment " + comment.id)
                with open("replied_to.txt", "a") as f:
                    f.write(comment.id + "\n")
                pass
            
            source = 'https://www.urbandictionary.com/define.php?term='+word
            comment.reply(f"#**{word.capitalize()}**:\n\n**Definition**: *{definition}*\n\n[Source]({source})\n\n***\n\n^(Bleep-bloop. I am a bot. | [Github](https://github.com/ddmin/UrbanDictionaryBot))")
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
        print('Error. Sleeping for 10 seconds\n')
        time.sleep(10)

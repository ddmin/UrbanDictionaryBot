from bs4 import BeautifulSoup
import requests
import praw
import config
import time
import random
from UrbDicBot import *
from UD_Popular import *

def authenticate():
    print("Authenticating UrbanDictBot...")
    reddit = praw.Reddit(username = config.username,
                         password = config.password,
                         client_id = config.client_id,
                         client_secret = config.client_secret,
                         user_agent = "ddmin's UrbanDicBot v2.8")
    print("Authenticated!\n")
    return reddit

def run_bot(reddit, comment_id, words):
    print("Obtaining comments...\n")
    for comment in reddit.subreddit("all").comments(limit=None):
                
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
                if word == '<random>':
                    rant = random.randint(0,len(words)-1)

                    definition = word_lookup(words[rant])
                    source = 'https://www.urbandictionary.com/define.php?term='+words[rant]
                    comment.reply(f'#{words[rant].capitalize()}:\n\n**Definition**: *{definition}*\n\n[Source]({source})\n\n***\n\n^(Bleep-bloop. I am a bot. |) [^(Github)](https://github.com/ddmin/UrbanDictionaryBot)')
                    print("Replied to comment " + comment.id)

                    with open("replied_to.txt", "a") as f:
                        f.write(comment.id + "\n")
                    
                elif word != '':
                    definition = word_lookup(word)
                    source = 'https://www.urbandictionary.com/define.php?term='+word
                    comment.reply(f'#{word.capitalize()}:\n\n**Definition**: *{definition}*\n\n[Source]({source})\n\n***\n\n^(Bleep-bloop. I am a bot. |) [^(Github)](https://github.com/ddmin/UrbanDictionaryBot)')
                    print("Replied to comment " + comment.id)

                    with open("replied_to.txt", "a") as f:
                        f.write(comment.id + "\n")

                    if word not in words:
                        with open("words.txt", "a") as f:
                            f.write(word + "\n")
                        
                else:
                    comment.reply('I can\'t find that word on Urban Dictionary.\n\n***\n\n^(Bleep-bloop. I am a bot. |) [^(Github)](https://github.com/ddmin/UrbanDictionaryBot)')
                    print("Replied to comment " + comment.id)
                    with open("replied_to.txt", "a") as f:
                        f.write(comment.id + "\n")
                
            except:
                comment.reply('I can\'t find that word on Urban Dictionary.\n\n***\n\n^(Bleep-bloop. I am a bot. |) [^(Github)](https://github.com/ddmin/UrbanDictionaryBot)')
                print("Replied to comment " + comment.id)
                with open("replied_to.txt", "a") as f:
                    f.write(comment.id + "\n")
            
            
                
       
                
def get_ids():
    with open("replied_to.txt", "r") as f:
        replied_to = f.read()
        replied_to = replied_to.split("\n")
    return replied_to

def get_words():
    f = open('popular_words.txt', 'w')
    f.close()
    scrape_words()
    with open("popular_words.txt", "r") as f:
        word_list = f.read()
        word_list = word_list.split("\n")
    return word_list

def main():
    reddit = authenticate()

    while True:
        try:
            comment_id = get_ids()
            word_list = get_words()[:-1]
            run_bot(reddit, comment_id, word_list)
        except:
            print('Error. Sleeping for 10 seconds\n')
            time.sleep(10)

if __name__ == '__main__':
    main()

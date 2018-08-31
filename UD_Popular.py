from bs4 import BeautifulSoup
import requests

def remove_html(string):
    copy = True
    copied_string = ''
    for char in string:
        if char == '<':
            copy = False
        if copy:
            copied_string += char
        if char == '>':
            copy = True
            copied_string += ' '
    return copied_string

def isolate_words(lst):
    number_lst = [str(n) + '.' for n in range(2,31)]
    
    copied_list = []
    copy = True
    copied_word = ''
    
    for item in lst:
        if item not in number_lst:
            copied_word += item + ' '
        if item in number_lst:
            copied_list.append(copied_word)
            copied_word = ''
        if item == lst[-1]:
            copied_list.append(copied_word)
    return copied_list
            
            

def scrape_words():
    website = 'https://www.urbandictionary.com/'
    
    source = requests.get(website).text
    soup = BeautifulSoup(source, 'lxml')
    popular_words = str(soup.find('div', class_='panel trending-words-panel'))
    
    popular_words = remove_html(popular_words)[34:].split()[1:]
    popular_words = isolate_words(popular_words)

    with open('popular_words.txt', 'a') as f:
        for x in popular_words:
            f.write(x)
            if x != popular_words[-1]:
                f.write('\n')

scrape_words()

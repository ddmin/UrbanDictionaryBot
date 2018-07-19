from bs4 import BeautifulSoup
import requests

def lineBreaks(defin):
    string = ''
    ignore = False
    for x in range(0, len(defin)-4):
        if defin[x] == '<':
            ignore = True
        if ignore == False:
            string += defin[x]
        if defin[x]+defin[x+1]+defin[x+2]+defin[x+3]+defin[x+4] == '<br/>':
            string += '\n'
        if defin[x] == '>':
            ignore = False
    return string

word = input('Word to look up: ')
website = 'https://www.urbandictionary.com/define.php?term='+word
source = requests.get(website).text

soup = BeautifulSoup(source, 'lxml')

section = soup.find('div', class_ = 'def-panel')
definition = section.find('div', class_ = 'meaning')

string = lineBreaks(str(definition))

print(f'\n{word.capitalize()}:\n\n{string}')

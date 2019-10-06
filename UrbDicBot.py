# UrbanDictionaryBot

from bs4 import BeautifulSoup
import requests


def caps(s):
    return ' '.join(list(map(lambda x: x.capitalize(), s.split())))

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

def word_lookup(word):
    website = 'https://www.urbandictionary.com/define.php?term='+word
    source = requests.get(website).text

    soup = BeautifulSoup(source, 'lxml')

    section = soup.find('div', class_ = 'def-panel')
    definition = section.find('div', class_ = 'meaning')

    string = lineBreaks(str(definition))

    return string.strip()

def main():
    print("== UrbanDictionaryBot ==")
    print()
    print("Word to look up:")
    word = input("\t> ")
    print()

    try:
        definition = word_lookup(word)
        print(caps(word) + ':')
        print('\t' + definition)
        print()
        print(f'(Information from https://www.urbandictionary.com/define.php?term={word})')
    except:
        print("I can't find a definition for that word.")


if __name__ == "__main__":
    main()

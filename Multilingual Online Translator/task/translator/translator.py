import requests
from bs4 import BeautifulSoup
import sys

args = sys.argv

full_lang = ('Arabic', 'German', 'English', 'Spanish', 'French', 'Hebrew', 'Japanese', 'Dutch', 'Polish', 'Portuguese',
             'Romanian', 'Russian', 'Turkish')

if args[1].capitalize() not in full_lang:
    print(f"Sorry, the program doesn't support {args[1]}")
    exit()
if args[2].capitalize() not in full_lang and args[2] != 'all':
    print(f"Sorry, the program doesn't support {args[2]}")
    exit()
if requests.get(f'https://context.reverso.net/translation/english-german/{args[3]}', headers={'User-Agent': 'Mozilla/5.0'}).status_code == 404:
    print(f"Sorry, unable to find {args[3]}")
    exit()
if requests.get('https://context.reverso.net/translation/', headers={'User-Agent': 'Mozilla/5.0'}).status_code != 200:
    print("Something wrong with your internet connection")
    exit()


print('Hello, welcome to the translator. Translator supports: ')
for n, l in enumerate(full_lang):
    print(f"{n + 1}. {l}")

# lang = int(input('Type the number of your language:')) - 1
# lang_s = int(input("Type the number of a language you want to translate to or '0' to translate to all languages:"))
# lang_x = lang_s - 1

lang = full_lang.index(args[1].capitalize())
lang_s = args[2]
if lang_s != 'all':
    lang_x = full_lang.index(args[2].capitalize())
# message = input('Type the word you want to translate:').lower()
message = args[3]

with open(f'{message}.txt', 'w+', encoding='utf-8') as file:
    pass
if lang_s != 'all':
    url = f"https://context.reverso.net/translation/{full_lang[lang].lower()}-{full_lang[lang_x].lower()}/{message}"

    headers = {'User-Agent': 'Mozilla/5.0'}
    page = requests.get(url, headers=headers)
    soup = BeautifulSoup(page.content, 'html.parser')
    # print(page.status_code, 'OK')
    translations = list(x.text for x in soup.find_all('span', {"class": "display-term"}))

    examp_list = []
    examples = soup.find_all('div', {"class": "example"})
    for example in examples:
        ex = example.find_all('span', {'class': "text"})
        for x in ex:
            examp_list.append(x.text.strip())
    with open(f'{message}.txt', 'a', encoding='utf-8') as file:
        print(f'\n{full_lang[lang_x]} Translations:')
        file.write(f'\n{full_lang[lang_x]} Translations:\n')
        for trans in range(2):
            print(translations[trans])
            file.write(translations[trans]+'\n')

        print(f'\n{full_lang[lang_x]} Examples:')
        file.write(f'\n{full_lang[lang_x]} Examples:\n')
        for examp in range(4):
            print(examp_list[examp])
            file.write(examp_list[examp]+'\n')
            if examp % 2 != 0:
                print()
                file.write('\n')

else:
    for lan in full_lang:
        if lan == full_lang[lang]:
            continue
        url = f"https://context.reverso.net/translation/{full_lang[lang].lower()}-{lan.lower()}/{message}"

        headers = {'User-Agent': 'Mozilla/5.0'}
        page = requests.get(url, headers=headers)
        soup = BeautifulSoup(page.content, 'html.parser')
        # print(page.status_code, 'OK')
        translations = list(x.text for x in soup.find_all('span', {"class": "display-term"}))

        examp_list = []
        examples = soup.find_all('div', {"class": "example"})
        for example in examples:
            ex = example.find_all('span', {'class': "text"})
            for x in ex:
                examp_list.append(x.text.strip())

        with open(f'{message}.txt', 'a', encoding='utf-8') as file:
            print(f'\n{lan} Translations:')
            file.write(f'\n{lan} Translations:\n')
            for trans in range(min(len(translations), 20)):
                print(translations[trans])
                file.write(translations[trans] + '\n')

            print(f'\n{lan} Examples:')
            file.write(f'\n{lan} Examples:\n')
            for examp in range(min(len(examp_list), 40)):
                print(examp_list[examp])
                file.write(examp_list[examp] + '\n')
                if examp % 2 != 0:
                    print()
                    file.write('\n')
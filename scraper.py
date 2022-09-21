from cgi import print_directory
from urllib import response
import requests
import lxml.html as html
import os
import datetime

XPATH_LINK_TO_ARTICLE = '//h2[@class="spotlightPrincipalContentHeadlineSecond spotlightPrincipalContentSecond"]/a/@href'
XPATH_TITLE = '//h1[@class="DefaultTitle"]/text()'
XPATH_SUB_TITLE = '//h2[@class="DefaultSubtitle"]/text()'
XPATH_BODY = '//section[@class="section-visibility"]/p[@class]/text()'

HOME_URL = 'https://larepublica.pe/'

def parse_notice(link, today):
    try:
        response = requests.get(link)
        if response.status_code == 200:
            notice = response.content.decode('utf-8')
            parsed = html.fromstring(notice)

            try:
                title = parsed.xpath(XPATH_TITLE)[0]
                title = title.replace('\"', '')
                summary = parsed.xpath(XPATH_SUB_TITLE)[0]
                body = parsed.xpath(XPATH_BODY)
            except IndexError:
                return
            
            with open(f'{today}/{title}.txt', 'w', encoding='utf-8') as f:
                f.write(title)
                f.write('\n\n')
                f.write(summary)
                f.write('\n\n')

                for p in body:
                    f.write(p)
                    f.write('\n\n')
        else:
            raise ValueError(f'Error: {response.status_code}')
    except ValueError as ve:
        print(ve)

def parse_home():
    try:
        response = requests.get(HOME_URL) #me conecto a la url
        if response.status_code == 200: #debe darme un estado 200 representa exito
            home = response.content.decode('utf-8') #decodifico toda la pagina a utf-8
            parsed = html.fromstring(home) #se parsea la pagina a estructura entendible y aplicable XPATH
            links_to_notices = parsed.xpath(XPATH_LINK_TO_ARTICLE) # ejecutamos el xpath
            #print(links_to_notices)
            today = datetime.date.today().strftime('%d-%m.%Y')
            if not os.path.isdir(today):
                os.mkdir(today)
            
            for link in links_to_notices:
                parse_notice(link, today)
            else:
                pass
        else:
            raise ValueError(f'Error: {response.status_code}')
    except ValueError as ve:
        print(ve)

def run():
    parse_home()

if __name__ == '__main__':
    run()
import requests
import lxml.html as html # convierte un archivo de html a un archivo que se le aplica xpath
import os  # crear carpeta con la fecha de hoy
import datetime  # trae la fecha de hoy

HOME_URL = 'https://www.larepublica.co/'

XPATH_LINK_TO_ARTICLE = '//text-fill[not(@class)]/a/@href'   # '//h2/a/@href'
XPATH_TITLE = '//div[@class="mb-auto"]/text-fill/span/text()'  #'//h2/a/text()'
XPATH_SUMMARY = '//div[@class="lead"]/p/text()'  #'//div[@class="lead"]/p/text()'
XPATH_BODY = '//div[@class="html-content"]/p[not(@class)]/text()' #'//div[@class="html-content'


def parse_notice(link, today):
    try:
        response = requests.get(link)
        if response.status_code == 200:
            notice = response.content.decode('utf-8')
            parsed = html.fromstring(notice)

            try:
                title = parsed.xpath(XPATH_TITLE)[0]
                title = title.replace('\"', '')
                title = title.replace('¿', '')
                title = title.replace('?', '')
                title = title.replace(':', '')
                print(title)
                summary = parsed.xpath(XPATH_SUMMARY)[0]
                body = parsed.xpath(XPATH_BODY)
            except IndexError:
                return  # salgo de la función

            # with es unmanejador contextual de python
            with open(f'descargas/{today}-la-republica/{title}.txt', 'w', encoding='utf-8') as f:
                f.write(title)
                f.write('\n\n')
                f.write(summary)
                f.write('\n\n')
                for p in body:
                    f.write(p)
                    f.write('\n')
        else:
            raise ValueError(f'Error: {response.status_code}')
    except ValueError as ve:
        print(ve)


def parse_home():
    try:
        response = requests.get(HOME_URL)
        if response.status_code == 200:
            home = response.content.decode('utf-8')
            parsed = html.fromstring(home)
            links_to_notices = parsed.xpath(XPATH_LINK_TO_ARTICLE)
            # print(links_to_notices)

            today = datetime.date.today().strftime('%d-%m-%Y')
            # si no existe una carpeta con la fecha de hoy
            if not os.path.isdir("descargas/"+today+'-la-republica'):
                os.mkdir("descargas/"+today+'-la-republica')  # crea una carpeta con el nombre de hoy

            for link in links_to_notices:
                parse_notice(link, today)
        else:
            raise ValueError(f'Error: {response.status_code}')
    except ValueError as ve:
        print(ve)


def run():
    parse_home()


if __name__ == '__main__':
    run()

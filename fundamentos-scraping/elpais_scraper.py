import requests
import lxml.html as html # convierte un archivo de html a un archivo que se le aplica xpath
import os  # crear carpeta con la fecha de hoy
import datetime  # trae la fecha de hoy
import time

HOME_URL = 'https://elpais.com/'

XPATH_LINK_TO_ARTICLE = '//h2/a/@href'   # '//h2/a/@href'
XPATH_TITLE = '//h1[@class="a_t"]/text()'  #'//h1[@class="a_t"]/text()'
XPATH_SUMMARY = '//h2[@class="a_st"]/text()'  #'//h2[@class="a_st"]/text()'
XPATH_BODY = '//div[@class="a_c clearfix"]/p/text()' #'//div[@class="a_c clearfix"]/p/text()'


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
                summary = parsed.xpath(XPATH_SUMMARY)[0]
                body = parsed.xpath(XPATH_BODY)
            except IndexError:
                return  # salgo de la función

            # with es unmanejador contextual de python
            with open(f'descargas/{today}-el-pais/{title}.txt', 'w+', encoding='utf-8') as f:
                f.write(title)
                f.write('\n\n')
                f.write(summary)
                f.write('\n\n')
                for p in body:
                    f.write(p)
                    f.write('\n')
                f.close()
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
            # print(links_to_notices[0])

            today = datetime.date.today().strftime('%d-%m-%Y')
            # si no existe una carpeta con la fecha de hoy
            if not os.path.isdir("descargas/"+today+"-el-pais"):
                os.mkdir("descargas/"+today+"-el-pais")  # crea una carpeta con el nombre de hoy

            for link in links_to_notices:
                parse_notice("https://elpais.com"+link, today) # todas las noticias
                time.sleep(5)
            # parse_notice("https://elpais.com"+links_to_notices[0], today) # solo una noticia
        else:
            raise ValueError(f'Error: {response.status_code}')
    except ValueError as ve:
        print(ve)


def run():
    parse_home()


if __name__ == '__main__':
    run()

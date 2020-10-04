from bs4 import BeautifulSoup
import requests
import datetime

from crawlers.Crawler import Crawler


class CSUBBCrawler(Crawler):

    def __init__(self):
        super().__init__('http://www.cs.ubbcluj.ro/robots.txt', False)
        self.__url = 'http://www.cs.ubbcluj.ro/'

    def crawl(self):
        if self.polite and not self.robots.can_fetch('me', self.__url):
            print('I am not allowed to fetch page: ' + self.__url)
            return []

        articles_published_today = []

        html = requests.get(self.__url).text
        soup = BeautifulSoup(html, features="html.parser")

        articles = soup.findAll("div", {"class": "post"})

        for article in articles:
            img = '' if article.findChild('img') is None else article.findChild('img')['src']
            title = ''.join(map(lambda tag: str(tag), article.find_next('h2').find_next('a').contents))
            url = article.find_next('h2').find_next('a')['href']
            time = datetime.datetime.strptime(article.find_next('span', {'class': 'meta_date'}).contents[0], '%d.%m.%Y')
            description = str(article.find_next('div', {'class': 'entry'}).contents[2]).strip()

            if datetime.date.today() == time.date():
                articles_published_today.append({
                    'img': img,
                    'title': title,
                    'description': description,
                    'url': url
                })


        return articles_published_today

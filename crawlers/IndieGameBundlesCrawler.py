from bs4 import BeautifulSoup
import requests
import datetime

from crawlers.Crawler import Crawler


class IndieGameBundlesCrawler(Crawler):

    def __init__(self):
        super().__init__('https://www.indiegamebundles.com/robots.txt', False)
        self.__url = 'https://www.indiegamebundles.com/category/free/'

    def crawl(self):
        if self.polite and not self.robots.can_fetch('me', self.__url):
            print('I am not allowed to fetch page: ' + self.__url)
            return []

        articles_published_today = []

        html = requests.get(self.__url).text
        soup = BeautifulSoup(html, features="html.parser")

        articles = soup.findAll("div", {"class": "td_module_10"})

        for article in articles:
            img = article.find_next("img")['data-img-url']
            title = article.find_next('h3').find_next('a')
            time = datetime.datetime.strptime(article.find_next('time').contents[0], '%B %d, %Y');
            description = str(article.find_next('div', {'class': 'td-excerpt'}).contents[0]).strip()

            if datetime.date.today() == time.date():
                articles_published_today.append({
                    'img': img,
                    'title': title,
                    'description': description,
                    'url': title['href']
                })

        return articles_published_today

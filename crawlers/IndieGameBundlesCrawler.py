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


        print("Looking for articles..")

        articles_published_today = []

        html = requests.get(self.__url).text

        soup = BeautifulSoup(html, features="html.parser")

        articles = soup.findAll("div", {"class": "td-module-container"})

        print("Found {} articles".format(len(articles)))

        for article in articles:
            img = article.find_next("a").find_next("span")
            title = article.find_next("h3").find_next("a")["title"]
            url = article.find_next("h3").find_next("a")["href"]

            time_container = article.find_next('time')
            if time_container is None:
              continue
            time = datetime.datetime.strptime(time_container.contents[0], '%B %d, %Y')

            if True or datetime.date.today() == time.date():
                articles_published_today.append({
                    'img': img,
                    'title': title,
                    'description': title,
                    'url': url
                })

        return articles_published_today

from common.Bot import Bot
from common.Email import Email
from crawlers.CSUBBCrawler import CSUBBCrawler


def get_receivers():
    receivers = []
    with open('receivers.txt', 'r') as file:
        receivers.append(file.readline())

    return receivers


if __name__ == '__main__':
    bot = Bot()
    bot.add_receivers(get_receivers())

    crawler = CSUBBCrawler()
    articles_published_today = crawler.crawl()

    email = Email()

    for article in articles_published_today:
        imgTag = '<img style="width:100%;"src={}>'.format(article['img']) if article['img'] != '' else ''
        email.html_content = '''
            <html>
                <body>
                    {imgTag}
                    <div> <a href={url}> {desc} </a></div>
                </body>
            </html>
        '''.format(
            imgTag=imgTag,
            desc=article['description'],
            url=article['url']
        )

        email.plain_content = article['description']
        bot.send_email(article['title'], email)

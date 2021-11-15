import sys
sys.path.append('../')
from common.Bot import Bot
from common.Email import Email
from crawlers.IndieGameBundlesCrawler import IndieGameBundlesCrawler


def get_receivers():
    receivers = []
    with open('receivers.txt', 'r') as file:
        receivers.append(file.readline())

    return receivers


if __name__ == '__main__':
    bot = Bot()
    bot.add_receivers(get_receivers())

    crawler = IndieGameBundlesCrawler()
    articles_published_today = crawler.crawl()
    
    if len(articles_published_today) == 0:
        print('No articles were published today.')
    else: 
        print(articles_published_today)

    email = Email()

    for article in articles_published_today:
        email.html_content = '''
            <html>
                <body>
                    <img style="width:100%;"src={img}>
                    <div> <a href={url}> {desc} </a></div>
                </body>
            </html>
        '''.format(
            img=article['img'],
            desc=article['description'],
            url=article['url']
        )

        with open('html_message.html', 'w') as file:
            file.write(email.html_content)

        email.plain_content = article['description']
        bot.send_email(article['title'], email)


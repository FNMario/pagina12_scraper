import requests
import lxml.html as html
import os
import datetime

HOME_URL = 'https://www.pagina12.com.ar/'

XPATH_LINKS_TO_ARTICLES = '//h2/a/@href[contains(.,"pagina12") and not(contains(.,"suplementos"))]'
XPATH_TITLE = '//h1/text()'
XPATH_SUBHEADING = '//h2[@class="h4"]/text()'
XPATH_LEAD = '//h2[@class="h3"]/text()'
XPATH_AUTHOR = '//div[@class="author-name"]/text()'
XPATH_BODY = '//text()[ancestor::h2[parent::div[@class="article-main-content article-text "]]| ancestor::p[parent::div[@class="article-main-content article-text "]]]'
XPATH_TAGS = '//div[@class="article-tags"]/a/text()'

def parse_article(link, folder):
    try:
        response = requests.get(link)
        if response.status_code == 200:
            article = response.content.decode('utf-8')
            parsed = html.fromstring(article)
            try:
                title = parsed.xpath(XPATH_TITLE)[0]
                print(title)
                subheading = parsed.xpath(XPATH_SUBHEADING)[0]
                lead = parsed.xpath(XPATH_LEAD)[0]
                author = parsed.xpath(XPATH_AUTHOR)
                tags = parsed.xpath(XPATH_TAGS)
                body = parsed.xpath(XPATH_BODY)
            except IndexError:
                return
            
            with open(folder+'/'+title.replace('\"','')+'.md', "w") as f:
                f.write('## ' + subheading +
                        '\n\n# ' + title +
                        '\n\n### ' + lead + '\n\n' +
                        '\n'.join([p.replace('\\','') for p in body]) +
                        '\n\n**'+ ', '.join([x.strip() for x in author]) + '**' +
                        '\n\nTags: ***'+ '***, ***'.join([t.strip() for t in tags]) + '***' +
                        '\n\n[link](' + link + ')'
                )
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
            links_to_articles = parsed.xpath(XPATH_LINKS_TO_ARTICLES)
            today = datetime.datetime.today().strftime('%Y-%m-%d')
            folder = r'./historical_archive/' + today
            if not os.path.isdir(folder):
                os.mkdir(folder)
            for link in links_to_articles:
                parse_article(link, folder)
        else:
            raise ValueError(f'Error: {response.status_code}')
    except ValueError as ve:
        print(ve)

print()
def run():
    parse_home()



if __name__ == '__main__':
    run()
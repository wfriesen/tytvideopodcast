import requests, json
from bs4 import BeautifulSoup
from fake_useragent import UserAgent
from datetime import datetime
from lxml import etree

from voucher import voucher

feedUrls = {
    'MainShowHour1': 'https://www.tytnetwork.com/category/membership/main-show-hour-1/feed',
    'MainShowHour2': 'https://www.tytnetwork.com/category/membership/main-show-hour-2/feed',
    'PostGame': 'https://www.tytnetwork.com/category/membership/post-game/feed/'
}

headers = {'User-Agent': UserAgent().chrome}

def get_cache_contents(name):
    try:
        with open(name, 'r') as file:
            cache = json.loads(file.read())
    except IOError:
        with open(name, 'w+') as file:
            cache = {}
            file.write(json.dumps(cache))
    return cache

def trim_cache(cache, itemstokeep):
    if len(cache) <= itemstokeep:
        return cache
    else:
        return sorted(d.iteritems(), key=lambda (key, value): value['timeAdded'])[:itemstokeep]

def get_download_link(link, cache):
    if link not in cache:
        html_doc = requests.get(link, headers=headers).text
        soup = BeautifulSoup(html_doc, 'html.parser')

        data_widget_id = soup.find('div', class_='gbox-download-buttons').attrs['data-widget-id']
        download_link = 'https://widgets-cdn-p1.gbox.com/download/' + data_widget_id + '/720p?voucher=' + voucher

        cache[link] = download_link

    return cache[link]

def main():
    cache_name = 'cache.json'
    cache = get_cache_contents(cache_name)
    cache_count = len(cache)

    for name, url in feedUrls.iteritems():
        print 'Generating feed for: ' + name
        rss = requests.get(url, headers=headers).content
        xml = etree.fromstring(rss)

        for item in xml.xpath('/*/channel/item'):
            link = item.xpath('./link')[0]
            link.text = get_download_link(link.text, cache)

        if cache_count != len(cache):
            cache = trim_cache(cache, 100)
            with open(cache_name, 'w+') as cache_file:
                cache_file.write(json.dumps(cache))

        with open('feeds/' + name + '.rss', 'w+') as output:
            output.write(etree.tostring(xml))

if __name__ == '__main__':
    main()

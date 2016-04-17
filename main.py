import requests
from bs4 import BeautifulSoup
from fake_useragent import UserAgent
from feedgen.feed import FeedGenerator
import json

from voucher import voucher

hour1_url = 'https://www.tytnetwork.com/category/membership/main-show-hour-1'
headers = {'User-Agent': UserAgent().chrome}

def get_download_link(url):
    html_doc = requests.get(url, headers=headers).text
    soup = BeautifulSoup(html_doc, 'html.parser')

    data_widget_id = soup.find('div', class_='gbox-download-buttons').attrs['data-widget-id']

    return 'https://widgets-cdn-p1.gbox.com/download/' + data_widget_id + '/720p?voucher=' + voucher

def get_cache_contents(name):
    try:
        with open(name, 'r') as file:
            cache = json.loads(file.read())
    except IOError:
        with open(name, 'w+') as file:
            cache = {}
            file.write(json.dumps(cache))
    return cache

def get_hour1_links():
    cache_name = 'hour1.json'
    cache = get_cache_contents(cache_name)

    html_doc = requests.get(hour1_url, headers=headers).text
    soup = BeautifulSoup(html_doc, 'html.parser')

    cache_updated = False
    for entry in soup.find_all('h2', class_='entry-title'):
        link = entry.find('a')
        if link.text not in cache:
            cache_updated = True
            download_link = get_download_link(link.attrs['href'])
            cache[link.text] = download_link

    if cache_updated:
        with open(cache_name, 'w+') as cache_file:
            cache_file.write(json.dumps(cache))

    return cache

def setup_feedgen():
    fg = FeedGenerator()
    fg.load_extension('podcast')
    fg.podcast.itunes_category('Technology', 'Podcasting')
    fg.id('TYT Hour 1')
    fg.title('TYT Hour 1')
    fg.link(href=hour1_url)
    fg.description('TYT Hour 1')
    return fg

def main():
    fg = setup_feedgen()

    links = get_hour1_links()
    for link in links:
        fe = fg.add_entry()
        fe.id(links[link])
        fe.title(link)
        fe.description(link)
        fe.enclosure(links[link], 0, 'video/mp4')

    fg.rss_file('hour1.xml', pretty=True)

if __name__ == '__main__':
    main()

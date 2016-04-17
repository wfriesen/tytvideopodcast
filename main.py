import requests
from bs4 import BeautifulSoup
from fake_useragent import UserAgent
from feedgen.feed import FeedGenerator
from voucher import voucher

hour1_url = 'https://www.tytnetwork.com/category/membership/main-show-hour-1'
headers = {'User-Agent': UserAgent().chrome}

def get_download_link(url):
    html_doc = requests.get(url, headers=headers).text
    soup = BeautifulSoup(html_doc, 'html.parser')

    data_widget_id = soup.find('div', class_='gbox-download-buttons').attrs['data-widget-id']

    return 'https://widgets-cdn-p1.gbox.com/download/' + data_widget_id + '/720p?voucher=' + voucher

def get_hour1_links():
    html_doc = requests.get(hour1_url, headers=headers).text
    soup = BeautifulSoup(html_doc, 'html.parser')

    for entry in soup.find_all('h2', class_='entry-title'):
        link = entry.find('a')
        download_link = get_download_link(link.attrs['href'])
        yield {'name': link.text, 'link': download_link}

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

    for link in get_hour1_links():
        fe = fg.add_entry()
        fe.id(link['link'])
        fe.title(link['name'])
        fe.description(link['name'])
        fe.enclosure(link['link'], 0, 'video/mp4')

    fg.rss_file('podcast.xml', pretty=True)

if __name__ == '__main__':
    main()

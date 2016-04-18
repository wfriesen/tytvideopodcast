# TYT Video Podcasts
Generate podcast feeds for video content from http://tytnetwork.com/

## Installation
- Install libxml2. In FreeBSD, this is done with:
```
portsnap fetch extract
cd /usr/ports/devel/py-lxml/
make install clean
```
and accept the defaults.
- Install requirements with `pip install -r requirements.txt`

## Setup
- Login to the TYT website, and go to the page to view a video (e.g.: https://www.tytnetwork.com/2016/04/15/tyt-hour-1-april-15-2016/)
- Right-click on one of the "Download" links below the video, copy the URL and paste it somewhere. The URL will end with something like `?voucher=XXXXXXXXX`, where the XXXXXXXXX is your "voucher" code, used by Gbox for authentication.
- Replace the value in `voucher.py` with your own voucher.

## Usage
Running `main.py` will generate RSS feeds for the Main Show Hour 1, 2, and Post Game, and place them in `./feeds`
. This command can be run from cron to re-generate the feeds on a set schedule, and then point your podcast client to these files.

Note that when running from cron you will need to specify the full path to both python and this script. A crontab entry to run every half hour might look like this:

`0,30 * * * * /usr/local/bin/python /root/tytvideopodcast/main.py`

## Flexget
I use [Flexget](http://flexget.com/) to automatically download these feeds. A sample config.yml is below:
```
tasks:
  tyt task:
    rss: file:///home/somebody/tytvideopodcast/feeds/MainShowHour1.rss
    series:
      - TYT Hour One
    download: /tmp/tyt
    accept_all: yes
```

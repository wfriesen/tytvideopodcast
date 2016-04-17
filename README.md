# TYT Video Podcasts
Generate podcast feeds for video content from http://tytnetwork.com/

## Setup
- Login to the TYT website, and go to the page to view a video (e.g.: https://www.tytnetwork.com/2016/04/15/tyt-hour-1-april-15-2016/)
- Right-click on one of the "Download" links below the video, copy the URL and paste it somewhere. The URL will end with something like `?voucher=XXXXXXXXX`, where the XXXXXXXXX is your "voucher" code, used by Gbox for authentication.
- Replace the value in `voucher.py` with your own voucher.

## Usage
Running `python main.py` will generate RSS feeds for the Main Show Hour 1, 2, and Post Game, and place them in `./feeds`
. This command can be run from cron to re-generate the feeds on a set schedule, and then point your podcast client to these files.

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

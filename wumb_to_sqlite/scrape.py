"""
Python API for scraping WUMB Playlists
"""
import datetime
import os
import time
from pathlib import Path

import httpx
from bs4 import BeautifulSoup
from sqlite_utils import Database

try:
    import lxml

    parser = "lxml"
except ImportError:
    parser = "html.parser"

BASE_URL = "http://wumb.org/cgi-bin/playlist1.pl"
DATE_FORMAT = "%y%m%d"  # http://wumb.org/cgi-bin/playlist1.pl?date=201010
TIME_FORMAT = "%I:%M %p"  # 11:56 pm
CACHE = Path.home() / ".wumb-to-sqlite"


def playlist(db, table="playlist", *, date=None, since=None, until=None, delay=1):
    """
    Download daily playlists, for a date or a range
    """

    if not any([date, since, until]):
        dates = [datetime.date.today()]

    elif date:
        dates = [date]

    elif since and until:
        dates = day_range(since, until)

    elif since or until:
        raise ValueError(
            "Invalid dates. Please provide either a single date, or both since and until arguments."
        )

    if not isinstance(db, Database):
        db = Database(db)

    table = db[table]

    for date in dates:
        songs = scrape(date)
        table.upsert_all(songs, pk="time")
        if len(dates) > 1:  # no need to delay a single download
            time.sleep(delay)


# _html is used for testing
def scrape(date, refresh=False, _html=None):
    """
    Extract playlist info for a single date, yielding song info
    """
    html = _html or fetch(date, refresh)
    soup = BeautifulSoup(html, parser)

    # every row is a table
    tables = soup.select("#MainContentTextOnly > table")
    for table in tables:
        artist = table.find("font", color="#000000").string.strip()
        title = table.find("font", size="+1").string.strip()
        playtime = datetime.datetime.strptime(
            table.find("font", size="-1").string.strip(), TIME_FORMAT
        ).time()

        yield {
            "artist": artist,
            "title": title,
            "time": datetime.datetime(
                date.year, date.month, date.day, playtime.hour, playtime.minute
            ),
        }


def fetch(date, refresh=False):
    """
    Download a playlist page for a given date, using the cache if possible, unless refresh,
    and return the HTML of the page.
    """
    if date > datetime.date.today():
        raise ValueError(f"{date} is in the future")
    datestring = date.strftime(DATE_FORMAT)
    cache = CACHE / f"{datestring}.html"

    if cache.exists() and not refresh:
        return cache.open().read()

    r = httpx.get(BASE_URL, params={"date": datestring})
    r.raise_for_status()

    with cache.open("w") as f:
        f.write(r.text)

    return r.text


def day_range(start, end):
    "One day at a time"
    current = start
    while current <= end:
        yield current
        current += datetime.timedelta(days=1)

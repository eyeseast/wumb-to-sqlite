"""
Python API for scraping WUMB Playlists
"""
import datetime
import os
import time
from pathlib import Path

import httpx
import pytz
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
TIMEZONE = pytz.timezone("US/Eastern")  # WUMB is in Boston


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

        if not all([artist, title]):
            continue

        yield {
            "artist": artist,
            "title": title,
            "time": datetime.datetime(
                date.year,
                date.month,
                date.day,
                playtime.hour,
                playtime.minute,
                tzinfo=TIMEZONE,
            ),
        }


def fetch(date, refresh=False):
    """
    Download a playlist page for a given date, using the cache if possible, unless refresh,
    and return the HTML of the page.
    """
    if isinstance(date, datetime.datetime):
        date = date.date()

    if date > datetime.date.today():
        raise ValueError(f"{date} is in the future")
    datestring = date.strftime(DATE_FORMAT)

    if not CACHE.exists():
        CACHE.mkdir()

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

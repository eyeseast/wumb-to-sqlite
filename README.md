# wumb-to-sqlite

[![PyPI](https://img.shields.io/pypi/v/wumb-to-sqlite.svg)](https://pypi.org/project/wumb-to-sqlite/)
[![Changelog](https://img.shields.io/github/v/release/eyeseast/wumb-to-sqlite?include_prereleases&label=changelog)](https://github.com/eyeseast/wumb-to-sqlite/releases)
[![Tests](https://github.com/eyeseast/wumb-to-sqlite/workflows/Test/badge.svg)](https://github.com/eyeseast/wumb-to-sqlite/actions?query=workflow%3ATest)
[![License](https://img.shields.io/badge/license-Apache%202.0-blue.svg)](https://github.com/eyeseast/wumb-to-sqlite/blob/master/LICENSE)

Scrape [WUMB playlists](http://wumb.org/cgi-bin/playlist1.pl) to SQLite.

WUMB is a public radio station based at UMass Boston. It's awesome and [you should support it](http://www.wumb.org/members/donate/) if you like great music with no ads. This is a personal project, however, and not associated with WUMB or UMass Boston in any way.

The station puts its daily playlist online here: http://wumb.org/cgi-bin/playlist1.pl. I often want to look up a song I heard in the car, or remember something that played last week. I'm also just curious about the music mix. So this is a tool to scratch that itch.

## Installation

Install this tool using `pip`:

    pip install wumb-to-sqlite

Or install globally with `pipx`:

    pipx install wumb-to-sqlite

## Usage

Scrape today's playlist:

    wumb-to-sqlite playlist wumb.db

That will use (or create) a SQLIte database called `wumb.db` and a table called `playlist`. Change the table name by passing a `--table` option.

Scrape a specific date, with a custom table name:

    wumb-to-sqlite playlist wumb.db --table songs --date 2020-09-01

That will get songs from [Sept. 1, 2020](http://wumb.org/cgi-bin/playlist1.pl?date=200901), and use a table called `songs`.

Scrape all daily playlists from Oct. 1 to Oct. 11, 2020:

    wumb-to-sqlite playlist wumb.db --since 2020-10-01 --until 2020-10-01 --delay 1

That will pull down playlists for each day between Oct. 1 and 11, inclusive. It adds a one second delay (which is the default) between days, as a courtesy to WUMB's servers.

Downloaded pages are cached locally, so subsequent runs don't keep re-fetching the same data. By default, it's located at `$HOME/.wumb-to-sqlite/`.

## Development

To contribute to this tool, first checkout the code. Then create a new virtual environment:

    cd wumb-to-sqlite
    python -mvenv venv
    source venv/bin/activate

Or if you are using `pipenv`:

    pipenv shell

Now install the dependencies and tests:

    pip install -e '.[test]'

To run the tests:

    pytest

Please note that scraping tests should be run against the included HTML file `tests/wumb-2020-10-10.html`, not against the live site. Again, this is a small public radio station. Please be nice.

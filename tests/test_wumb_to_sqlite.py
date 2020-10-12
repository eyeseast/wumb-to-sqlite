import datetime
import pathlib
import pytest
from click.testing import CliRunner
from wumb_to_sqlite.cli import cli
from wumb_to_sqlite.scrape import scrape, day_range

here = pathlib.Path(__file__).parent


@pytest.fixture
def page():
    return open(here / "wumb-2020-10-10.html").read()


def test_version():
    runner = CliRunner()
    with runner.isolated_filesystem():
        result = runner.invoke(cli, ["--version"])
        assert 0 == result.exit_code
        assert result.output.startswith("cli, version ")


def test_day_range():
    dates = [datetime.date(2020, 10, i) for i in range(1, 10)]

    assert dates == list(
        day_range(datetime.date(2020, 10, 1), datetime.date(2020, 10, 9))
    )


def test_scrape_date(page):
    date = datetime.date(2020, 10, 10)
    playlist = scrape(date, _html=page)
    playlist = list(playlist)

    assert len(playlist) == 258

    song = playlist[0]

    assert isinstance(song, dict)
    assert set(song.keys()) == {"artist", "time", "title"}

    assert song["artist"] == "Billy Strange"
